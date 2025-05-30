from random import randint
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from datetime import datetime, timedelta
from utils.upload import upload_file

from legalUser.models import OTP, User, Client, Attorney, Education, Experience, AttorneyExpertise

# User related serializers
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    document = serializers.FileField(required=False, write_only=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "role", "document"]
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate(self, data):
        confirmPassword = data.get('confirm_password')
        password = data.get('password')
        
        if password != confirmPassword:
            raise serializers.ValidationError("Passwords do not match")
        
        email = data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        
        return data
    
    def save(self):
        validated_data = self.validated_data.copy()
        role = validated_data.get("role")
        document = validated_data.pop("document", None)
        validated_data.pop("confirm_password")
        
        # Hash password
        password = validated_data.pop("password")
        validated_data["password"] = make_password(password)
        
        # Create the user
        user = User.objects.create(**validated_data)

        try:
            if role == "client":
                client = Client.objects.create(user=user)

                if document:
                    # Upload file
                    file_url, _ = upload_file(document, folder="probono_documents")
                    client.probono_document = file_url
                    client.probono_status = "pending"
                    client.save()

            elif role == "attorney":
                if not document:
                    raise serializers.ValidationError("License document is required for attorneys.")

                # Upload license document
                file_url, _ = upload_file(document, folder="attorney_licenses")
                Attorney.objects.create(user=user, license_document=file_url)

            # Admins don't require any document
        except Exception as e:
            # Optional: rollback user creation if necessary
            user.delete()
            raise serializers.ValidationError(f"Failed to create profile: {str(e)}")

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
    user = UserDetailSerializer(read_only=True)
    
    class Meta:
        model = Attorney
        fields = "__all__"
        depth = 1

class AttorneyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attorney
        fields = ["starting_price", "is_available", "offers_probono", "address", "expertise", "bio"]
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

## Attorney Education and Experience serializers
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'year']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'organization', 'title', 'years']

class AttorneyProfileSerializer(serializers.Serializer):
    education = EducationSerializer(many=True)
    experience = ExperienceSerializer(many=True)

class AttorneyDetailsSerializer(serializers.ModelSerializer):
    education = EducationSerializer(source='education_set', many=True, read_only=True)
    experience = ExperienceSerializer(source='experience_set', many=True, read_only=True)
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Attorney
        fields = [
            "id", "starting_price", "is_available", "offers_probono",
            "address", "rating", "profile_completion", "license_document",
            "is_approved", "expertise", "education", "experience", "user"
        ]

    def to_representation(self, instance):
        """Customize response based on requesting user's role."""
        representation = super().to_representation(instance)

        request = self.context.get('request')

        if request and request.user.role == 'client':
            if not instance.is_available:
                raise serializers.ValidationError("Attorney is not available.")
            
            if not instance.is_approved:
                raise serializers.ValidationError("Attorney is not approved.")
            
            client = Client.objects.get(user=request.user)
            if not client.probono_status == "approved" and not instance.offers_probono:
                raise serializers.ValidationError("Attorney does not offer probono services.")

            # Remove `user` from response for clients
            representation.pop('user', None)

        return representation

    
class UserAttorneyDetailsSerializer(serializers.ModelSerializer):
    attorney = AttorneyDetailsSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "role", "image", "attorney"]

# Client related serializers
class ClientSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Client
        fields = "__all__"
        depth = 1

class ClientProBonoRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['probono_document']

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