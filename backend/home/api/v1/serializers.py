from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from rest_auth.serializers import PasswordResetSerializer
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth.tokens import PasswordResetTokenGenerator,default_token_generator
#from silent_sea_44703.utils import Util
from django.template.loader import render_to_string
import requests
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from users.models import User, UserProfile, PatientInfo, Doctor, Instructor, Feedback, Appointment, ToDoList, LikeDoctor
from modules.two_factor_authentication.twofactorauth.utils import Util
from modules.two_factor_authentication.twofactorauth.models import TwoFactorAuth
from meeting.zoom.models import Zoom


import os
import boto3
from urllib.parse import urlparse
import environ
 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_file = os.path.join(BASE_DIR, ".env")
env = environ.Env()
env.read_env(env_file)

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.

    This serializer is used to convert the UserProfile model instances into JSON
    representation and vice versa. It specifies the fields that should be included
    in the serialized output.

    Attributes:
        model (UserProfile): The UserProfile model class.
        fields (list): The list of fields to be included in the serialized output.
    """
    class Meta:
        model = UserProfile
        fields = ['user_type']

class PatientInfoSerializer(serializers.ModelSerializer):
    support_needed = serializers.MultipleChoiceField(choices=PatientInfo.SUPPORT_CHOICES, required=False, allow_blank=True, allow_null=True, write_only=True)
    
    class Meta:
        model = PatientInfo
        fields = ['patient_id', 'title', 'age', 'address', 'age_range', 'health_today', 'allergies', 'medications','family_health_history','occupation', 'physical_activity','habits','busy_schedule', 'blood_group', 'height', 'weight', 'blood_group', 'disability', 'genotype','support_needed','emergency_contact_name','emergency_contact','emergency_contact_email']

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['age', 'address', 'about_instructor', 'specialized', 'qualification']

class SignupWithEmailSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'confirm_password')
        
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(_("Password and Confirm Password don't match"))
        return attrs

    def create(self, validated_data):        

        user = User.objects.create(
            email=validated_data.get('email'),
            name=validated_data.get('name'),            
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        two_factor_auth = TwoFactorAuth.objects.create(user=user, email=validated_data.get('email'))
        two_factor_auth.save()            
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'first_name', 'last_name', 'dob','full_name','phone_number', 'gender', 'profile_picture']

class DoctorListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Doctor
        fields = ['age', 'address', 'about_doctor', 'specialized', 'qualification', 'available_time', 'working_days', 'working_hours', 'experience' ]
    

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    favourite = serializers.SerializerMethodField()
 
    class Meta:
        model = Doctor
        fields = ['user', 'id', 'age', 'address', 'about_doctor', 'specialized', 'qualification', 'available_time', 'working_days', 'working_hours', 'experience', 'favourite']
   
    def get_favourite(self, obj):
        # Assuming obj is a Doctor instance, retrieve its favourite status
        #like_doctor = LikeDoctor.objects.filter(doctor=obj, user=user).first()
        like_doctor = LikeDoctor.objects.filter(doctor=obj).first()
        if like_doctor:
            return like_doctor.favourite
        return None

class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer class for user signup.

    This serializer is used to validate and create a new user during the signup process.
    It includes fields for user information such as name, email, password, and additional profile information.

    Attributes:
        confirm_password (CharField): Field for confirming the password during signup.
        profile (UserProfileSerializer): Serializer for user profile information.
        patient_info (PatientInfoSerializer): Serializer for patient information.
        doctor_info (DoctorSerializer): Serializer for doctor information.
        instructor_info (InstructorSerializer): Serializer for instructor information.

    Meta:
        model (User): The User model to be used for creating a new user.
        fields (tuple): The fields to include in the serializer.
        extra_kwargs (dict): Additional keyword arguments for specific fields.

    Methods:
        validate_email: Custom validation method for the email field.
        validate: Custom validation method for the serializer as a whole.
        create: Method for creating a new user based on the validated data.
        _get_request: Internal method for getting the request object from the serializer context.
        save: Method for saving the serializer instance.
    """
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile = UserProfileSerializer()
    patient_info = PatientInfoSerializer(required=False)
    doctor_info = DoctorSerializer(required=False)
    instructor_info = InstructorSerializer(required=False)

    class Meta:
        model = User
        fields = ('name', "full_name", "first_name", 'last_name', 'email', 'gender', 'phone_number', 'dob', 'profile', 'patient_info', 'doctor_info', 'instructor_info', 'password', 'confirm_password')
        
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def validate_email(self, email):
        """
        Custom validation method for the email field.

        This method checks if the email is unique and raises a validation error if it is already registered.

        Args:
            email (str): The email address to validate.

        Returns:
            str: The validated email address.

        Raises:
            serializers.ValidationError: If a user is already registered with the provided email address.
        """
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(_("A user is already registered with this e-mail address."))
        return email

    def validate(self, attrs):
        """
        Custom validation method for the serializer as a whole.

        This method checks if the password and confirm_password fields match.

        Args:
            attrs (dict): The validated data for the serializer.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If the password and confirm_password fields don't match.
        """
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError(_("Password and Confirm Password don't match"))
        return attrs

    def create(self, validated_data):
        """
        Method for creating a new user based on the validated data.

        This method creates a new User instance with the provided data and saves it to the database.
        It also creates related profile, patient info, doctor info, and instructor info if provided.

        Args:
            validated_data (dict): The validated data for creating the user.

        Returns:
            User: The created user instance.
        """
        user_profile_data = validated_data.pop('profile', None)
        patient_info_data = validated_data.pop('patient_info', None)
        doctor_info_data = validated_data.pop('doctor_info', None)
        instructor_info_data = validated_data.pop('instructor_info', None)

        user = User.objects.create(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            full_name=validated_data.get('full_name'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            gender=validated_data.get('gender'),
            dob=validated_data.get('dob'),
            phone_number=validated_data.get('phone_number'),
            username=generate_unique_username([
                validated_data.get('name'),
                validated_data.get('email'),
                'user'
            ])
        )
        user.set_password(validated_data.get('password'))
        user.save()
        if user_profile_data:
            if user_profile_data['user_type']:
                user_type = user_profile_data.get('user_type')
                UserProfile.objects.create(user=user, user_type=user_type)
        
        if patient_info_data:
            PatientInfo.objects.create(user=user, **patient_info_data)

        if doctor_info_data:
            Doctor.objects.create(user=user, **doctor_info_data)

        if instructor_info_data:
            Instructor.objects.create(user=user, **instructor_info_data)
            
        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def _get_request(self):
        """
        Internal method for getting the request object from the serializer context.

        Returns:
            HttpRequest: The request object.
        """
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def save(self, request=None):
        """
        Method for saving the serializer instance.

        This method overrides the default save method to accept the request object.

        Args:
            request (HttpRequest, optional): The request object. Defaults to None.

        Returns:
            Any: The saved instance.
        """
        return super().save()

class AuthTokenByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Assuming the user model has an email field
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs             

class PasswordSerializer(PasswordResetSerializer):
    """Custom serializer for rest_auth to solve reset password error"""
    password_reset_form_class = ResetPasswordForm
     
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['email']
 
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            msg = render_to_string("email/resetpassword.txt", {'uid': uid, 'token': token, 'site_url': os.environ.get('SITE_URL')})
            data={'subject':'Reset Password', 'body':msg, 'to_email':email}
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError(_("You are not a registered user"))
            
class ChangePasswordSerializer(serializers.ModelSerializer):
 
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)
 
    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
 
        if attrs['old_password'] == attrs['password']:
            raise serializers.ValidationError({"error": "New password cannot be the same as the old password."})
 
        user = self.instance
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"error": "Old password is not correct"})
 
        return attrs
 
    def update(self, instance, validated_data):
 
        instance.set_password(validated_data['password'])
        instance.save()
 
        return instance  


class EditUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for updating user information.

    This serializer is used to update the fields of a User model instance, along with related models such as UserProfile,
    PatientInfo, Doctor, and Instructor.

    Attributes:
        profile (UserProfileSerializer): Serializer for the UserProfile model.
        patient_info (PatientInfoSerializer): Serializer for the PatientInfo model.
        doctor_info (DoctorListSerializer): Serializer for the Doctor model.
        instructor_info (InstructorSerializer): Serializer for the Instructor model.

    Meta:
        model (User): The User model class.
        fields (tuple): The fields to be included in the serialized representation.

    Methods:
        update(instance, validated_data): Updates the user instance with the provided validated data.

    """

    profile = UserProfileSerializer()
    patient_info = PatientInfoSerializer(required=False)
    doctor_info = DoctorListSerializer(required=False)
    instructor_info = InstructorSerializer(required=False)

    class Meta:
        model = User
        fields = ('name', "full_name", "first_name", 'last_name', 'email', 'gender', 'phone_number', 'dob', 'profile', 'patient_info', 'doctor_info', 'instructor_info')
   
    def update(self, instance, validated_data):
        """
        Updates the user instance with the provided validated data.

        Args:
            instance (User): The User model instance to be updated.
            validated_data (dict): The validated data containing the updated field values.

        Returns:
            User: The updated User model instance.

        """

        profile_data = validated_data.pop('profile', None)
        patient_info_data = validated_data.pop('patient_info', None)
        doctor_info_data = validated_data.pop('doctor_info', None)
        instructor_info_data = validated_data.pop('instructor_info', None)

        # Update user fields
        instance.name = validated_data.get('name', instance.name)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.save()

        # Update profile if provided
        if profile_data:
            profile_instance, _ = UserProfile.objects.get_or_create(user=instance)
            profile_serializer = UserProfileSerializer(profile_instance, data=profile_data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        # Update patient info if provided
        if patient_info_data:
            patient_info_instance, _ = PatientInfo.objects.get_or_create(user=instance)
            patient_info_serializer = PatientInfoSerializer(patient_info_instance, data=patient_info_data, partial=True)
            patient_info_serializer.is_valid(raise_exception=True)
            patient_info_serializer.save()

        # Update doctor info if provided
        if doctor_info_data:
            doctor_info_instance, _ = Doctor.objects.get_or_create(user=instance)
            doctor_info_serializer = DoctorListSerializer(doctor_info_instance, data=doctor_info_data, partial=True)
            doctor_info_serializer.is_valid(raise_exception=True)
            doctor_info_serializer.save()

        # Update instructor info if provided
        if instructor_info_data:
            instructor_info_instance, _ = Instructor.objects.get_or_create(user=instance)
            instructor_info_serializer = InstructorSerializer(instructor_info_instance, data=instructor_info_data, partial=True)
            instructor_info_serializer.is_valid(raise_exception=True)
            instructor_info_serializer.save()

        return instance
 
class AvatarSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ['avatar']
 
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance        

class UserDetailSerializer(serializers.ModelSerializer):
    avatar_signed_url = serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=['name', 'full_name', 'gender', 'email', 'phone_number', 'avatar', 'avatar_signed_url']
 
    def get_avatar_signed_url(self, obj):
            avatar_url = obj.avatar.url if obj.avatar else None
            # Extract the object key from the avatar URL
            if avatar_url:
                parsed_url = urlparse(avatar_url)
                object_key = parsed_url.path[1:]  # Remove the leading slash
                # Generate a signed URL using the extracted object key
                s3 = boto3.client('s3',
                                region_name=env.str("AWS_STORAGE_REGION", ""),
                                config=boto3.session.Config(signature_version='s3v4'))
                expiration_time = 3600  # URL expires after 1 hour
                signed_url = s3.generate_presigned_url(
                    'get_object', Params = {'Bucket': 'loopafrica-44703', 'Key': object_key},
                    ExpiresIn = expiration_time, HttpMethod='GET'
                )
                return signed_url
            else:
                return None
            
class UserProfilePicUpdateSerializer(serializers.ModelSerializer):
    profile_picture_signed_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'profile_picture', 'profile_picture_signed_url']
 
    def get_profile_picture_signed_url(self, obj):
        profile_picture_url = obj.profile_picture.url if obj.profile_picture else None
 
        if profile_picture_url:
            parsed_url = urlparse(profile_picture_url)
            object_key = parsed_url.path[1:]   # Remove the leading slash
            # Generate a signed URL using the extracted object key
            s3 = boto3.client('s3', region_name=env.str("AWS_STORAGE_REGION", ""),
                                config=boto3.session.Config(signature_version='s3v4'))
            #expiration_time = 3600    # URL expires after 1 hour
            signed_url = s3.generate_presigned_url(
                    'get_object', Params = {'Bucket': 'loopafrica-44703', 'Key': object_key},
                    HttpMethod='GET'
                )
            return signed_url
        else:
            return None
   
    def update(self, instance, validated_data):
        profile_picture = validated_data.get('profile_picture', None)
        instance = super().update(instance, validated_data)
        if profile_picture:
            instance.profile_picture = profile_picture
            instance.save()
        return instance
 

class FeedbackSerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='User'
    )
    email = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='User'
    )
    class Meta:
        model = Feedback
        fields = ['user_id', 'name', 'email', 'subject', 'message', 'replied', 'reply_message']

class ZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zoom
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    zoom = ZoomSerializer(many=True, required=False, allow_null=True, read_only=True, source='zoom_appointment')
    doctor_name = serializers.SerializerMethodField()
    specialization = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_doctor_name(self, obj):        
        return obj.doctor.user.name if obj.doctor else None

    def get_specialization(self, obj):
        return obj.doctor.specialized if obj.doctor else None

class UserProListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    patient_info = serializers.SerializerMethodField()
    doctor_info = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user', 'user_type', 'patient_info', 'doctor_info']

    def get_patient_info(self, obj):
        patient_info = PatientInfo.objects.filter(user=obj.user).first()
        if patient_info:
            return PatientInfoSerializer(patient_info).data
        return None

    def get_doctor_info(self, obj):
        doctor_info = Doctor.objects.filter(user=obj.user).first()
        if doctor_info:
            return DoctorListSerializer(doctor_info).data
        return None

class PatientProfileCompletionSerializer(serializers.ModelSerializer):
    """
    Serializer class for calculating the completion percentage of a patient's profile.
    """
    user_id = serializers.IntegerField(source='user.id')
    user_name = serializers.CharField(source='user.name')
    patient_profile_completion = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['user_id', 'user_name', 'user_type', 'patient_profile_completion']
    
    def get_patient_profile_completion(self, obj):
        """
        Method to calculate the completion percentage of a patient's profile.
        
        Args:
            obj: The instance of the UserProfile model.
        
        Returns:
            The completion percentage of the patient's profile as a float value.
        """
        patient_info = PatientInfo.objects.filter(user=obj.user).first()
        
        if patient_info:
            # Define required fields for profile completion
            required_fields = [
                obj.user.first_name,
                obj.user.last_name,
                obj.user.dob,
                obj.user.phone_number,
                obj.user.email,
                obj.user.gender,
                obj.user.phone_number,
                obj.user.profile_picture,
                patient_info.title,
                patient_info.age,
                patient_info.address,
                patient_info.health_today,
                patient_info.allergies,
                patient_info.medications,
                patient_info.family_health_history,
                patient_info.occupation,
                patient_info.physical_activity,
                patient_info.habits,
                patient_info.busy_schedule,
                patient_info.blood_group,
                patient_info.height,
                patient_info.weight,
                patient_info.blood_group,
                patient_info.disability,
                patient_info.genotype,
                patient_info.support_needed,
                patient_info.emergency_contact_name,
                patient_info.emergency_contact,
                patient_info.emergency_contact_email,                
                # Add more fields as per your requirement
            ]
            
            # Count how many fields are filled
            filled_fields = sum(field is not None for field in required_fields)
            
            # Calculate the percentage of completion
            total_fields = len(required_fields)
            completion_percentage = (filled_fields / total_fields) * 100
            
            completion_percentage = round(completion_percentage)

            return completion_percentage
        return 0  # Profile Not Available

class DoctorProfileCompletionSerializer(serializers.ModelSerializer):
    """
    Serializer class for calculating the profile completion percentage of a doctor's profile.
    """

    user_id = serializers.IntegerField(source='user.id')
    user_name = serializers.CharField(source='user.name')
    doctor_profile_completion = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user_id', 'user_name', 'user_type', 'doctor_profile_completion']

    def get_doctor_profile_completion(self, obj):
        """
        Calculates the profile completion percentage of a doctor's profile.

        Args:
            obj: The instance of the UserProfile model.

        Returns:
            The profile completion percentage as a float value.
        """
        doctor_info = Doctor.objects.filter(user=obj.user).first()
        if doctor_info:
            # Define required fields for profile completion
            required_fields = [
                obj.user.first_name,
                obj.user.last_name,
                obj.user.dob,
                obj.user.phone_number,
                obj.user.email,
                obj.user.gender,
                obj.user.phone_number,
                obj.user.profile_picture,
                doctor_info.age,
                doctor_info.address,
                doctor_info.about_doctor,
                doctor_info.specialized,
                doctor_info.qualification,
                doctor_info.available_time,
                doctor_info.working_days,
                doctor_info.working_hours,
                doctor_info.experience,
            ]

            # Count how many fields are filled
            filled_fields = sum(field is not None for field in required_fields)

            # Calculate the percentage of completion
            total_fields = len(required_fields)
            completion_percentage = (filled_fields / total_fields) * 100

            completion_percentage = round(completion_percentage)

            return completion_percentage
        return 0  # Profile Not Available
    
class ToDOListSerializer(serializers.ModelSerializer):
    """
    Serializer class for ToDOList model.
    """
    class Meta:
        model = ToDoList
        fields = '__all__'

class LikeDoctorSerializer(serializers.ModelSerializer):
    """
    Serializer class for LikeDoctor model.
    """
    class Meta:
        model = LikeDoctor
        fields = "__all__"
        
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
 
    class Meta:
        fields = ('email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }
 
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"error": "Password fields didn't match."})
 
        return attrs
 
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance