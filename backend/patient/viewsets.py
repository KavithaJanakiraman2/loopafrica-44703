from rest_framework.viewsets import ModelViewSet
from users.models import Vitals
from .serializers import VitalsSerializer, PrescriptionSerializer, MedicationSerializer, MedicalRecordSerializer, TestResultSerializer, TestResultUploadSerializer
from hospital_operations.pharmacy.models import Prescription, Medication
from hospital_operations.emr.models import MedicalRecord, TestResult
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

class VitalsViewSet(ModelViewSet):
    """
    A viewset for handling Vitals data.

    This viewset provides CRUD operations for Vitals objects.
    """

    queryset = Vitals.objects.all()
    serializer_class = VitalsSerializer

    def get_queryset(self):
        """
        Get the queryset for Vitals objects.

        If a user_id is provided in the query parameters, filter the queryset
        to only include Vitals objects associated with that user. Otherwise,
        return all Vitals objects.

        Returns:
            QuerySet: The queryset for Vitals objects.
        """
        user = self.request.query_params.get('user_id')
        if user:
            return Vitals.objects.filter(user=user)
        return Vitals.objects.all()

class PrescriptionViewSet(ModelViewSet):
    """
    A viewset for handling Prescription related operations.

    Inherits from ModelViewSet which provides default CRUD operations.

    Attributes:
        queryset (QuerySet): The queryset of all Prescription objects.
        serializer_class (Serializer): The serializer class for Prescription objects.
    """

    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new Prescription and associated Medications.

        Args:
            request (Request): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object.

        Raises:
            HTTP 400 Bad Request: If the prescription data or medication data is invalid.
        """
        prescription_data = request.data.pop('prescription', None)
        medications_data = request.data.pop('medications', [])

        # Create Prescription
        prescription_serializer = self.get_serializer(data=prescription_data)
        if prescription_serializer.is_valid():
            prescription = prescription_serializer.save(user=request.user)
        else:
            return Response(prescription_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Medications
        medication_serializer = MedicationSerializer(data=medications_data, many=True)
        if medication_serializer.is_valid():
            medication_serializer.save(prescription=prescription)
        else:
            # If medication data is invalid, delete the prescription
            prescription.delete()
            return Response(medication_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Prescription and medications created successfully'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def medicationlist(self, request, user_id=None):
        """
        Retrieve the medications associated with the latest prescription of a specific user.

        Args:
            request (Request): The HTTP request object.
            user_id (int): The ID of the user.

        Returns:
            Response: The HTTP response object.

        Raises:
            HTTP 404 Not Found: If the prescription is not found.
        """
        prescription = Prescription.objects.filter(user=user_id).order_by("-id").first()                
        if prescription:
            medications = Medication.objects.filter(prescription_id=prescription.id)
            prescription_serializer = PrescriptionSerializer(prescription)
            medication_serializer = MedicationSerializer(medications, many=True)
            response_data = {
                "prescription": prescription_serializer.data,
                "medications": medication_serializer.data
            }
            return Response(response_data)
        else:
            return Response({"message": "Prescription not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def todo_medication(self, request, user_id=None):
        """
        Retrieve the medications that need to be taken today for a specific user.

        Args:
            request (Request): The HTTP request object.
            user_id (int): The ID of the user.

        Returns:
            Response: The HTTP response object.
        """
        today = datetime.now()
        todays_medications = Medication.objects.filter(prescription__user=user_id, frm__date__lte=today, to__date__gte=today)
        serializer = MedicationSerializer(todays_medications, many=True)
        return Response(serializer.data)

# class MedicalRecordViewSet(ModelViewSet):
#     queryset = MedicalRecord.objects.all()
#     serializer_class = MedicalRecordSerializer

class TestResultViewSet(ModelViewSet):
    """
    A viewset for handling test results.

    This viewset provides CRUD operations for the TestResult model.
    It requires authentication for all operations and supports parsing
    multipart and form data.

    Attributes:
        queryset (QuerySet): The queryset of TestResult objects.
        serializer_class (Serializer): The serializer class for TestResult objects.
        permission_classes (list): The list of permission classes for the viewset.
        parser_classes (tuple): The tuple of parser classes for the viewset.
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)
 
   
class TestResultUploadViewSet(ModelViewSet):
    """
    A viewset for handling test result uploads.

    This viewset provides the following actions:
    - create: Upload a new test result.
    - list: Retrieve a list of all test results.
    - delete: Delete a specific test result.

    Only authenticated users are allowed to perform these actions.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TestResult.objects.all()
    serializer_class = TestResultUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        """
        Upload a new test result.

        Parameters:
        - request: The HTTP request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - A Response object with the serialized data of the created test result.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Retrieve a list of all test results.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - A Response object with the serialized data of all test results.
        """
        queryset = TestResult.objects.all()
        serializer = TestResultUploadSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        """
        Delete a specific test result.

        Parameters:
        - request: The HTTP request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - A Response object with no content.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self):
        """
        Get the specific test result object.

        Returns:
        - The test result object.
        """
        obj = self.get_queryset().get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

class MedicalRecordViewSet(ModelViewSet):
    """
    A viewset for handling medical records.

    This viewset provides the following actions:
    - create: Create a new medical record.
    - list: Retrieve a list of medical records based on query parameters.

    Attributes:
        serializer_class (Serializer): The serializer class for the medical record model.
        permission_classes (list): The permission classes required for accessing the viewset.
        queryset (QuerySet): The queryset for retrieving medical records.
    """

    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]
    queryset = MedicalRecord.objects.all()
   
    def create(self, request):
        """
        Create a new medical record.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with the serialized data or error messages.
        """
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            # Extract user_id and patient_id from request data
            user_id = request.data.get('user')
            patient_id = request.data.get('patient')
           
            # Create the medical record object with user_id and patient_id
            medical_record = serializer.save(user_id=user_id, patient_id=patient_id)
           
            # Return success response with serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return error response if serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    def list(self, request):
        """
        Retrieve a list of medical records based on query parameters.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with the serialized data.
        """
        # Get the from_date and to_date from query parameters
        user_id = request.query_params.get('user_id')
        from_date_str = request.query_params.get('from_date')
        to_date_str = request.query_params.get('to_date')
       
        # Parse the date strings into datetime objects
        if from_date_str:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
        else:
            from_date = None
       
        if to_date_str:
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()
        else:
            to_date = None
        
        # Filter records based on user_id and date range if provided
        queryset = MedicalRecord.objects.all()
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if from_date and to_date:
            queryset = queryset.filter(frmdate__gte=from_date , todate__lte=to_date)
        
        # Serialize the queryset and return the response
        serializer = MedicalRecordSerializer(queryset, many=True)
        return Response(serializer.data)
    