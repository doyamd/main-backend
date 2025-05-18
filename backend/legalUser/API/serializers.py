from random import randint
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from datetime import datetime, timedelta

from legalUser.models import OTP, User, Client, Attorney, Education, Experience, AttorneyExpertise

# User related serializers
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        # exclude = ["image"]
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "role"]
        extra_kwargs ={'password':{'write_only':True},}
    
    def validate(self, data):
        confirmPassword = data.get('confirm_password')
        password = data.get('password')
        print(password, confirmPassword)
        if password != confirmPassword:
            raise serializers.ValidationError("Passwords do not match")
        
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        
        return data
    
    def save(self):
        validated_data = self.validated_data
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        
        user = User.objects.create(**validated_data)
        
        if user.role == 'client':
            Client.objects.create(user=user)
        elif user.role == 'attorney':
            Attorney.objects.create(user=user)
            
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]
        extra_kwargs ={'password':{'write_only':True},}
    
    def validate(self, data):
        confirmPassword = data.get('confirm_password')
        password = data.get('password')
        if password != confirmPassword:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def save(self):
        validated_data = self.validated_data
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        validated_data['role'] = 'admin'
        print(validated_data)
        user = User.objects.create(**validated_data)
        
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password':{'write_only':True}}

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #exclude role
        
        extra_kwargs = {'password':{'write_only':True}}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email or password is incorrect")
        
        user = User.objects.get(email=email)
        if not check_password(password, user.password):
            raise serializers.ValidationError("Email or password is incorrect")
        
        if OTP.objects.filter(user=user).exists():
            raise serializers.ValidationError("User is not verified")
        
        if user.role == 'client':
            if not Client.objects.filter(user=user).exists():
                raise serializers.ValidationError("User is not a client")
        elif user.role == 'attorney':
            if not Attorney.objects.filter(user=user).exists():
                raise serializers.ValidationError("User is not an attorney")
        
        return data

class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
        
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        
        return email

# Attorney related serializers
class AttorneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = "__all__"

class AttorneyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = ["starting_price", "is_available", "offers_probono", "address", "expertise"]
        extra_kwargs = {
            'password': {'write_only': True},
            'expertise': {'required': False}
        }

    def validate_expertise(self, value):
        if value is None:
            return value
            
        if not isinstance(value, list):
            raise serializers.ValidationError("Expertise must be a list")
            
        valid_expertise = AttorneyExpertise.values()
        invalid_values = [e for e in value if e not in valid_expertise]
        
        if invalid_values:
            raise serializers.ValidationError({
                'invalid_values': invalid_values,
                'valid_values': valid_expertise
            })
            
        return value

class AttorneyUploadLicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = ["license_document"]
        extra_kwargs = {'license_document':{'write_only':True}}

# Client related serializers
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


# OTP related serializers
class OTPSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    class Meta:
        model = OTP
        fields = ['email', 'otp']
    
    def validate(self, data):
        email = data.get('email')
        
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email does not exist")
        
        return data