from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, filters
from rest_framework.mixins import UpdateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import User, Feedback, Appointment, UserProfile, Doctor, ToDoList, LikeDoctor
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from django.db.models import Case, When, Value, IntegerField


from home.api.v1.serializers import (
    SignupSerializer,
    SignupWithEmailSerializer,
    UserSerializer,
    EditUserSerializer,
    UserProfilePicUpdateSerializer,
    FeedbackSerializer,
    AppointmentSerializer,
    UserProListSerializer,
    PatientProfileCompletionSerializer,
    DoctorProfileCompletionSerializer,
    SendPasswordResetEmailSerializer,
    ChangePasswordSerializer,
    DoctorSerializer,
    ToDOListSerializer,
    ResetPasswordSerializer,
)


class SignupViewSet(ModelViewSet):
    """
    A viewset for handling user sign up requests.

    This viewset allows users to sign up by sending a POST request with their
    registration details. The `SignupSerializer` is used to validate and
    process the incoming data.

    Supported HTTP methods: POST
    """

    serializer_class = SignupSerializer
    http_method_names = ["post"]

class SignUpWithEmailView(CreateAPIView):
    serializer_class = SignupWithEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})

class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})
    
class EditUserView(RetrieveUpdateAPIView, UpdateModelMixin):
    """
    A view for editing user information.

    This view allows authenticated users to update their own user information.

    Inherits from:
        - RetrieveUpdateAPIView: Provides the default implementation for retrieving and updating a model instance.
        - UpdateModelMixin: Provides the default implementation for updating a model instance.

    Attributes:
        authentication_classes (list): A list of authentication classes applied to the view.
        permission_classes (list): A list of permission classes applied to the view.
        queryset (QuerySet): The queryset used for retrieving the user instance.
        serializer_class (Serializer): The serializer class used for serializing and deserializing user data.

    Methods:
        update(request, *args, **kwargs): Updates the user instance with the provided data.

    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = EditUserSerializer

    def update(self, request, *args, **kwargs):
        """
        Updates the user instance with the provided data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object containing the serialized user data.

        Raises:
            ValidationError: If the provided data is invalid.

        """
        instance = self.get_object()
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserProfilePicUpdateView(RetrieveUpdateAPIView, UpdateModelMixin):
    """
    View for updating the user profile picture.

    This view allows authenticated users to update their profile picture.
    The user must be authenticated and provide a valid image file in the request data.

    Inherits from:
        - RetrieveUpdateAPIView: Provides the default implementation for retrieving and updating a model instance.
        - UpdateModelMixin: Provides the default implementation for updating a model instance.

    Attributes:
        authentication_classes (list): The authentication classes required for this view.
        permission_classes (list): The permission classes required for this view.
        queryset (QuerySet): The queryset used to retrieve the user instance.
        serializer_class (Serializer): The serializer class used for serializing and deserializing the user instance.
        parser_classes (tuple): The parser classes used for parsing the request data.

    Methods:
        get_object: Retrieves the user instance.
        update: Updates the user instance with the provided data.

    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfilePicUpdateSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def get_object(self):
        """
        Retrieves the user instance.

        Returns:
            User: The user instance.

        """
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """
        Updates the user instance with the provided data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object containing the serialized user data.

        """
        instance = self.get_object()
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class FeedbackViewSet(ModelViewSet):
    """
    A viewset for handling feedback related operations.

    Inherits from ModelViewSet, which provides default CRUD operations.

    Attributes:
        queryset (QuerySet): The queryset of Feedback objects.
        serializer_class (Serializer): The serializer class for Feedback objects.
        permission_classes (list): The list of permission classes for the viewset.

    Methods:
        perform_create(serializer): Overrides the default perform_create method to save the user with the feedback.
    """

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Overrides the default perform_create method to save the user with the feedback.

        Args:
            serializer (Serializer): The serializer instance for the feedback object.

        Returns:
            None
        """
        serializer.save(user=self.request.user)

class AppointmentViewSet(ModelViewSet):
    """
    A viewset for managing appointments.

    This viewset provides the following actions:
    - create: Create a new appointment.
    - retrieve: Retrieve a specific appointment by ID.
    - list: List all appointments.
    - update_feedback: Update the feedback and ratings for an appointment.
    - todo_appointments: Get the list of appointments for a specific user on the current day.
    """

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """
        Create a new appointment.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the appointment is created successfully, returns the serialized appointment data with HTTP status 201.
        - If the appointment data is invalid, returns the validation errors with HTTP status 400.
        """
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific appointment by ID.

        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the appointment to retrieve.

        Returns:
        - If the appointment exists, returns the serialized appointment data with HTTP status 200.
        - If the appointment does not exist, returns an error message with HTTP status 404.
        """
        appointment = self.get_object()
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def list(self, request):
        """
        List all appointments.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Returns the serialized data of all appointments with HTTP status 200.
        """
        queryset = self.get_queryset()
        serializer = AppointmentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_feedback(self, request):
        """
        Update the feedback and ratings for an appointment.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the appointment is updated successfully, returns the serialized appointment data with HTTP status 200.
        - If any required fields are missing, returns an error message with HTTP status 400.
        - If the appointment does not exist, returns an error message with HTTP status 404.
        """
        data = request.data
        user_id = data.get('user')
        doctor_id = data.get('doctor')
        date = data.get('date')
        consult_time = data.get('consult_time')
        feedback = data.get('feedback')
        ratings = data.get('ratings')
        
        if not (user_id and doctor_id and date and consult_time and feedback):
            return Response({'error': 'User ID, doctor ID, date, consult time, and feedback are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = Appointment.objects.get(user_id=user_id, doctor_id=doctor_id, date=date, consult_time=consult_time)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)

        appointment.feedback = feedback
        appointment.ratings = ratings
        appointment.status = "Completed"
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def todo_appointments(self, request, user_id=None):
        """
        Get the list of appointments for a specific user on the current day.

        Parameters:
        - request: The HTTP request object.
        - user_id: The ID of the user.

        Returns:
        - Returns the serialized data of the appointments for the user on the current day with HTTP status 200.
        """
        today = datetime.now().date()
        today_appointments = Appointment.objects.filter(user=user_id, date=today)
        serializer = AppointmentSerializer(today_appointments, many=True)
        return Response(serializer.data)


class UserProfileViewSet(ModelViewSet):
    """
    A viewset for managing user profiles.

    This viewset provides the following actions:
    - `list`: Returns a list of all user profiles.
    - `retrieve`: Retrieves a specific user profile by ID.
    - `create`: Creates a new user profile.
    - `update`: Updates an existing user profile.
    - `partial_update`: Partially updates an existing user profile.
    - `destroy`: Deletes a user profile.

    Additionally, it provides the following custom actions:
    - `profile`: Retrieves the profile of the currently authenticated user.
    - `update_profile`: Updates the profile of the currently authenticated user.
    - `profile_completion`: Retrieves the profile completion status of the currently authenticated user.

    Note: Only authenticated users can perform these actions.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProListSerializer

    def get_queryset(self):
        """
        Returns the queryset of user profiles filtered by the currently authenticated user.

        Returns:
            QuerySet: The filtered queryset of user profiles.
        """
        user = self.request.user
        return UserProfile.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """
        Retrieves the profile of the currently authenticated user.

        Returns:
            Response: The serialized profile data.
        """
        user_profile = self.get_queryset().first()
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_profile(self, request):
        """
        Updates the profile of the currently authenticated user.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The serialized profile data.
        """
        user_profile = self.get_queryset().first()
        serializer = self.get_serializer(user_profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def profile_completion(self, request):
        """
        Retrieves the profile completion status of the currently authenticated user.

        Returns:
            Response: The serialized profile completion data.
        """
        user_profile = self.get_queryset().first()
        if user_profile.user_type == UserProfile.UserType.PATIENT:
            serializer_class = PatientProfileCompletionSerializer
        elif user_profile.user_type == UserProfile.UserType.DOCTOR:
            serializer_class = DoctorProfileCompletionSerializer
        else:
            return Response({'error': 'Profile completion is not applicable for this user type.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializer_class(user_profile)
        return Response(serializer.data)

class DoctorViewSet(ModelViewSet):
    """
    A viewset for managing Doctor objects.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__full_name','user__first_name','user__last_name','specialized', 'qualification']
    ordering_fields = ['user__full_name','user__firs_name','user__last_name','specialized']
    ordering = ['user__full_name','user__first_name','user__last_name','specialized']

    # Pagination
    pagination_class = LimitOffsetPagination
    
    @action(detail=False, methods=['get'])
    def patient_count(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response({'error': 'Doctor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        patient_count = doctor.appointment_set.filter(status='Completed').count()
        return Response({'patient_count': patient_count}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def doctor_specialized(self, request):
        specialized = request.query_params.get('specialization')
        if not specialized:
            return Response({'error': 'specialized param is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure Doctor queryset contains Doctor instances
        doctors = Doctor.objects.filter(specialized=specialized)
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def doctor_appointments(self, request, pk=None):
        """
        Retrieve appointments for a specific doctor on particular dates and list the appointment times.
 
        Parameters:
        - request: The HTTP request object.
        - pk: The ID of the doctor.
 
        Returns:
        - Returns the serialized data of appointments for the specific doctor on the specified dates or all scheduled dates with HTTP status 200.
        """
        doctor = self.get_object()
        date_param = request.query_params.get('date')
       
        # Parse date parameter
        if date_param:
            try:
                date = datetime.strptime(date_param, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
           
            appointments = doctor.appointment_set.filter(date=date)
        else:
            # If date parameter is not provided, retrieve all appointments for the doctor
            appointments = doctor.appointment_set.all()
       
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get', 'post'])
    def favourite(self, request, pk=None):
        user = request.user
        if request.method == 'GET':
            # Handle GET request for listing favourite doctors
            favorite_doctors = Doctor.objects.filter(like_doctor_doctor__user=user, like_doctor_doctor__favourite='1').annotate(
            favourite_order=Value(0, output_field=IntegerField())
            )
            # Get non-favorite doctors with annotation for ordering
            non_favorite_doctors = Doctor.objects.exclude(like_doctor_doctor__user=user, like_doctor_doctor__favourite='1').annotate(
                favourite_order=Value(1, output_field=IntegerField())
            )
            # Concatenate favorite and non-favorite doctors and order by the annotated field
            all_doctors = favorite_doctors.union(non_favorite_doctors).order_by('favourite_order', '-last_updated_date')
            serializer = self.get_serializer(all_doctors, many=True)
            return Response(serializer.data)
       
        elif request.method == 'POST':
            # Handle POST request for adding doctor to favourites
            doctor_id = request.data.get('doctor_id')
            favourite = request.data.get('favourite')
 
            # Ensure favourite and doctor_id are provided
            if not (favourite and doctor_id):
                return Response({'error': 'Both favourite and doctor_id parameters are required.'}, status=status.HTTP_400_BAD_REQUEST)
 
            # Ensure favourite is provided and is '1' (favorite)
            if favourite != '1':
                return Response({'error': 'Invalid favourite parameter. Use "1" for favourite.'}, status=status.HTTP_400_BAD_REQUEST)
           
            # Get the doctor based on the doctor_id sent in the request data
            doctor = get_object_or_404(Doctor, pk=doctor_id)
       
            # Check if the user has already favourited the doctor
            existing_like = LikeDoctor.objects.filter(doctor=doctor, user=user, favourite='1').first()
            if existing_like:
                return Response({'error': f'Doctor {doctor.user.username} is already added to your favourite list.'}, status=status.HTTP_400_BAD_REQUEST)
           
            # Create the LikeDoctor object
            LikeDoctor.objects.create(doctor=doctor, user=user, favourite=favourite)
            return Response({'detail': f'Doctor {doctor.user.username} added to your favourite list.'}, status=status.HTTP_200_OK)

    
class SendPasswordResetEmailView(APIView):
    """
        A view for sending password reset emails to users.
    """
    def post(self, request, format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Password reset link sent. Please check your email'}, status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    """
    A view for changing the password of a user.
    """
    permission_classes = [IsAuthenticated]
 
    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(instance=user, data=request.data)
 
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'msg': 'Password changed successfully',
                'data': serializer.data
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                'msg': 'Failed to change password',
                'errors': serializer.errors
            }
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ToDoListViewSet(ModelViewSet):
    """
    A viewset for managing ToDoList objects.

    This viewset provides CRUD operations for ToDoList objects,
    as well as a custom action to delete completed tasks.

    Attributes:
        queryset (QuerySet): The queryset of ToDoList objects.
        serializer_class (Serializer): The serializer class for ToDoList objects.
        permission_classes (list): The list of permission classes for this viewset.
    """

    queryset = ToDoList.objects.all().order_by('-created_at')
    serializer_class = ToDOListSerializer
    permission_classes = [IsAuthenticated]
 
    @action(detail=False, methods=['delete'])
    def delete_completed(self, request):
        """
        Custom action to delete completed tasks.

        This action deletes all the completed tasks from the database.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with status code 204 (No Content).
        """
        completed_tasks = ToDoList.objects.filter(completed=True)
        completed_tasks.delete()
        return Response(status=204)

class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = User.objects.filter(email=email).first()
            if user:
                user.set_password(password)
                user.save()
                return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
