from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from random import randint
from datetime import datetime, timedelta, timezone
from rest_framework.permissions import IsAuthenticated
from legalUser.API.serializers import(
    UserSerializer, 
    UserDetailSerializer,
    UserLoginSerializer,
    UserEmailSerializer,
    OTPSerializer,
    AdminUserSerializer,
    ClientSerializer,
    AttorneyUpdateSerializer,
    AttorneySerializer,
    EducationSerializer,
    ExperienceSerializer
    
)
from legalUser.common.emailsender import send_email

from legalUser.API.permissions import IsOwnerorReadOnly, IsAdmin, IsAdminOrOwner, IsClientOrAdmin, IsAttorneyOrAdmin, IsClientOrAdminOrOwner
from legalUser.models import (
    Client,
    Attorney,
    User,
    Education,
    Experience,
    OTP)
from legalUser.common.commonresponse import BaseResponse
from legalUser.common.otpgenerator import verify_OTP_Template, createOTP
from utils.upload import upload_file


# user views
class UserCreateAV(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        response = BaseResponse()
        if serializer.is_valid():
            serializer.save()
            otpvalue = createOTP()
            user = User.objects.get(email = serializer.data.get('email', ''))
            otp = OTP.objects.create(user=user,otp = otpvalue, expired_at = datetime.now(tz=timezone.utc) + timedelta(minutes=5))
            # otp.save()
            html_content = verify_OTP_Template(otpvalue)
            send_email("OTP Verification",[user.email],"" ,html_content)
            response = BaseResponse(status_code=201,success=True, message="User created successfully", data={'user':serializer.data})
        else:
            response = BaseResponse(status_code=400, success=False, message="Invalid user details", data=serializer.errors)    
            
        return Response(response.to_dict(), status= response.status_code)
    
class AdminUserCreateAV(APIView):
    permission_classes = [IsAdmin]
    def post(self, request):
        serializer = AdminUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = BaseResponse(status_code=201, success=True, message="User created successfully", data={'user':serializer.data})
        else:
            response = BaseResponse(status_code=400, success=False, message="Invalid user details", data=serializer.errors)
        return Response(response.to_dict(), status= response.status_code)
    
class UserListAV(generics.ListAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserDetailSerializer
    
    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role', None)
        if role and role in ['admin', 'client', 'attorney']:
            queryset = queryset.filter(role=role)
        return queryset

class UserDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrOwner]
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # If admin, just return user data
        if instance.role == 'admin':
            return Response(data)

        # Add client data if user is a client
        if instance.role == 'client':
            try:
                client = Client.objects.get(user=instance)
                client_serializer = ClientSerializer(client)
                data['client_data'] = client_serializer.data
            except Client.DoesNotExist:
                data['client_data'] = None

        # Add attorney data if user is an attorney
        elif instance.role == 'attorney':
            try:
                attorney = Attorney.objects.get(user=instance)
                attorney_serializer = AttorneySerializer(attorney)
                data['attorney_data'] = attorney_serializer.data
            except Attorney.DoesNotExist:
                data['attorney_data'] = None

        return Response(data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        response = BaseResponse()

        if serializer.is_valid():
            # Update user data
            serializer.save()
            data = serializer.data
            if instance.role == 'attorney':
                try:
                    attorney = Attorney.objects.get(user=instance)
                    attorney_serializer = AttorneyUpdateSerializer(attorney, data=request.data, partial=True)
                    if attorney_serializer.is_valid():
                        # Handle expertise update
                        if 'expertise' in request.data:
                            attorney.expertise = request.data['expertise']
                        attorney_serializer.save()
                        data['attorney_data'] = attorney_serializer.data
                    else:
                        response = BaseResponse(
                            status_code=400,
                            success=False,
                            message="Invalid attorney data",
                            data=attorney_serializer.errors
                        )
                        return Response(response.to_dict(), status=response.status_code)
                except Attorney.DoesNotExist:
                    response = BaseResponse(
                        status_code=404,
                        success=False,
                        message="Attorney profile not found"
                    )
                    return Response(response.to_dict(), status=response.status_code)

            response = BaseResponse(
                status_code=200,
                success=True,
                message="User updated successfully",
                data=data
            )
        else:
            response = BaseResponse(
                status_code=400,
                success=False,
                message="Invalid user details",
                data=serializer.errors
            )

        return Response(response.to_dict(), status=response.status_code)
    
class UserUploadImageAV(APIView):
    permission_classes = [IsAdminOrOwner]
    
    def post(self, request):
        response = BaseResponse()
        user = request.user
        image = request.FILES.get('image')
        
        if not image:
            response = BaseResponse(
                status_code=400,
                success=False,
                message="No image provided"
            )
            return Response(response.to_dict(), status=response.status_code)
            
        try:
            file_url, public_id = upload_file(image, folder="user_images")
            user.image = file_url
            user.save()
            response = BaseResponse(
                status_code=200, 
                success=True, 
                message="Image uploaded successfully", 
                data={"image_url": file_url}
            )
        except Exception as e:
            response = BaseResponse(
                status_code=500, 
                success=False, 
                message=f"Failed to upload image: {str(e)}"
            )
            
        return Response(response.to_dict(), status=response.status_code)

class UserLoginAV(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data.get('email', ''))
            user_detail = UserDetailSerializer(user)
            tokens = RefreshToken.for_user(user=user)
            access_token = str(tokens.access_token)
            refresh_token = str(tokens)
            response = BaseResponse(
                status_code=200,data={"user":user_detail.data, "access_token":access_token, "refresh_token":refresh_token}
                , message="user logged in successfully", 
                success=True)
        else:
            response = BaseResponse(status_code=400, Error=serializer.errors, message="invalid credentials", success=False)
            
        return Response(response.to_dict(), status=response.status_code)
    
# attorney views 
class AttorneyUploadLicenseAV(APIView):
    permission_classes = [IsAdminOrOwner]

    def post(self, request):
        response = BaseResponse()
        
        # Check if user is an attorney
        if request.user.role != 'attorney':
            response = BaseResponse(
                status_code=403,
                success=False,
                message="Only attorneys can upload license documents"
            )
            return Response(response.to_dict(), status=response.status_code)

        # Get the file from request
        license_file = request.FILES.get('license_document')
        if not license_file:
            response = BaseResponse(
                status_code=400,
                success=False,
                message="No file provided"
            )
            return Response(response.to_dict(), status=response.status_code)

        try:
            # Upload file to Cloudinary
            file_url, public_id = upload_file(license_file, folder="attorney_licenses")

            # Get attorney profile or return error
            try:
                attorney = Attorney.objects.get(user=request.user)
            except Attorney.DoesNotExist:
                response = BaseResponse(
                    status_code=404,
                    success=False,
                    message="Attorney profile not found"
                )
                return Response(response.to_dict(), status=response.status_code)
            
            # Update license document URL
            attorney.license_document = file_url
            attorney.save()

            response = BaseResponse(
                status_code=200,
                success=True,
                message="License document uploaded successfully",
                data={"license_url": file_url}
            )
        except Exception as e:
            response = BaseResponse(
                status_code=500,
                success=False,
                message=f"Failed to upload license document: {str(e)}"
            )

        return Response(response.to_dict(), status=response.status_code)
    
class AttorneyListAV(generics.ListAPIView):
    permission_classes = [IsClientOrAdmin]
    serializer_class = AttorneySerializer
    queryset = Attorney.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # If user is client, only show available and approved attorneys with basic user info
        if self.request.user.role == 'client':
            queryset = queryset.filter(is_available=True, is_approved=True)
        # If user is admin, allow filtering by params and show all fields except password
        elif self.request.user.role == 'admin':
            is_available = self.request.query_params.get('is_available')
            is_approved = self.request.query_params.get('is_approved')
            
            if is_available is not None:
                queryset = queryset.filter(is_available=is_available.lower() == 'true')
            if is_approved is not None:
                queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
        
        # Always prefetch user data to avoid N+1 queries
        queryset = queryset.select_related('user')
        
        return queryset

class ToggleAttorneyApprovalAV(APIView):
    permission_classes = [IsAdmin]
    
    def post(self, request, pk):
        response = BaseResponse()
        try:
            user = User.objects.get(id=pk)
            if user.role != 'attorney':
                response = BaseResponse(
                    status_code=400,
                    success=False,
                    message="User is not an attorney"
                )
            attorney = Attorney.objects.get(user=user)
            attorney.is_approved = not attorney.is_approved
            attorney.save()
            
            response = BaseResponse(
                status_code=200,
                success=True,
                message="Attorney approval status updated successfully",
                data={
                    "is_approved": attorney.is_approved,
                    "attorney_id": str(attorney.id)
                }
            )
        except Attorney.DoesNotExist:
            response = BaseResponse(
                status_code=404,
                success=False,
                message="Attorney not found"
            )
        except ValueError:
            response = BaseResponse(
                status_code=400,
                success=False,
                message="Invalid attorney ID format"
            )
        return Response(response.to_dict(), status=response.status_code)

class AttorneyEducationExperienceAV(APIView):
    permission_classes = [IsClientOrAdminOrOwner]
    serializer_class = EducationSerializer
    experience_serializer_class = ExperienceSerializer
    queryset = Education.objects.all()

    #get all education of an attorney
    def get(self, request, pk):
        response = BaseResponse()
        try:
            user = User.objects.get(id=pk)
            if user.role != 'attorney':
                response = BaseResponse(status_code=400, success=False, message="User is not an attorney")
                return Response(response.to_dict(), status=response.status_code)
            attorney = Attorney.objects.get(user=user)
            education = Education.objects.filter(attorney=attorney)
            serializer = self.serializer_class(education, many=True)
            experience = Experience.objects.filter(attorney=attorney)
            experience_serializer = self.experience_serializer_class(experience, many=True)
            response = BaseResponse(status_code=200, success=True, message="Education and experience retrieved successfully", data={"education":serializer.data, "experience":experience_serializer.data})
        except Attorney.DoesNotExist:
            response = BaseResponse(status_code=404, success=False, message="Attorney not found")
        return Response(response.to_dict(), status=response.status_code)
    
    # update education and experience
    def patch(self, request, pk):
        response = BaseResponse()
        try:
            user = request.user
            if not hasattr(user, 'attorney'):
                response.update(400, False, "User is not an attorney")
                return Response(response.to_dict(), status=response.status_code)

            attorney = user.attorney
            data = request.data

            def handle_serializer(key, serializer_class, model_class):
                item_id = pk
                if not item_id:
                    response.update(400, False, f"{key.capitalize()} ID is required")
                    raise ValueError

                try:
                    item = model_class.objects.get(id=item_id)
                    if item.attorney != attorney:
                        response.update(403, False, f"You don't have permission to update this {key}")
                        raise ValueError

                    serializer = serializer_class(item, data=data.get(key, {}), partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        response.update(200, True, f"{key.capitalize()} updated successfully", serializer.data)
                        return True  # successful update
                    else:
                        response.update(400, False, f"Invalid {key} details", serializer.errors)
                        raise ValueError
                except model_class.DoesNotExist:
                    return False  # not found

            # Try education first
            if handle_serializer('education', EducationSerializer, Education):
                return Response(response.to_dict(), status=response.status_code)

            # If not found, try experience
            if handle_serializer('experience', ExperienceSerializer, Experience):
                return Response(response.to_dict(), status=response.status_code)

            # If neither found
            response.update(404, False, "Neither education nor experience record found with the given ID")

        except ValueError:
            pass  # response already updated
        except Exception as e:
            response.update(500, False, str(e))

        return Response(response.to_dict(), status=response.status_code)
                        
            
    
class AttorneyEducationExperienceCreateAV(APIView):
    permission_classes = [IsAttorneyOrAdmin]

    def post(self, request):
        response = BaseResponse()
        user = request.user

        if not hasattr(user, 'attorney'):
            response.update(400, False, "User is not an attorney")
            return Response(response.to_dict(), status=response.status_code)

        attorney = user.attorney
        data = request.data
        result_data = {}
        messages = []

        def handle_serializer(key, serializer_class):
            if key in data:
                serializer = serializer_class(data=data[key])
                if serializer.is_valid():
                    serializer.save(attorney=attorney)
                    result_data[key] = serializer.data
                    messages.append(f"{key.capitalize()} added successfully")
                else:
                    response.update(400, False, f"Invalid {key} details", serializer.errors)
                    raise ValueError  # Trigger early exit
       
        try:
            handle_serializer('education', EducationSerializer)
            handle_serializer('experience', ExperienceSerializer)

            if result_data:
                response.update(200, True, " and ".join(messages), result_data)
            else:
                response.update(400, False, "No valid education or experience data provided")

        except ValueError:
            pass  # response is already prepared with error inside handler

        return Response(response.to_dict(), status=response.status_code)
    
    

# otp views

class OTPVerifyAV(APIView):
    def post(self, request):
        try:
            serializer = OTPSerializer(data= request.data)
            response = BaseResponse()
            if serializer.is_valid():
                otp = serializer.validated_data.get('otp', '')
                user = User.objects.get(email=serializer.validated_data.get('email', ''))
                otp_obj = OTP.objects.get(user=user)
                
                if otp_obj.otp != otp:
                    response = BaseResponse(status_code=400, success=False, message="Invalid OTP or expired OTP")
                    
                elif  (datetime.now(timezone.utc) -  otp_obj.expired_at).total_seconds() > 0:
                    response = BaseResponse(status_code=400, success=False, message="OTP expired, sent a new OTP")
                    otpvalue = createOTP()
                    new_otp = OTP.objects.update(user=user,otp = otpvalue, expired_at = datetime.now(tz=timezone.utc) + timedelta(minutes=5))
                    new_otp.save()
                    html_content = verify_OTP_Template(otpvalue)
                    send_email("OTP Verification",[user.email],"" ,html_content)
                    
                else:
                    otp_obj.delete()
                    response = BaseResponse(status_code=200, success=True, message="OTP verified successfully")
                    
            else:
                response = BaseResponse(status_code=400, success=False, message="Invalid OTP details", data=serializer.errors)
        except User.DoesNotExist:
            response = BaseResponse(status_code=400, success=False, message="OTP verification failed")
        except OTP.DoesNotExist:
            response = BaseResponse(status_code=400, success=False, message="OTP verification failed")
            
        return Response(response.to_dict(), status=response.status_code)
    
class OTPCreateAV(APIView):
    def post(self, request):
        try:
            serializer = UserEmailSerializer(data= request.data)
            response = BaseResponse()
            if serializer.is_valid():
                user = User.objects.get(email=serializer.data.get('email', ""))
                otp_value = createOTP()
                otp = OTP.objects.get(user=user)
                OTP.objects.update(user=user, otp=otp_value, expired_at = datetime.now(tz=timezone.utc) + timedelta(minutes=5))
                html_content = verify_OTP_Template(otp_value)
                send_email("OTP Verification",[user.email],"",html_content)
                response = BaseResponse(status_code=200, success=True, message="OTP sent successfully")
            else:
                response = BaseResponse(status_code=400, success=False, message="Invalid user details", data=serializer.errors)
        except User.DoesNotExist:
            response = BaseResponse(status_code=400, success=False, message="User not found")
        except OTP.DoesNotExist:
            response = BaseResponse(status_code=400, success=False, message="Failed to send OTP")
        return Response(response.to_dict(), status=response.status_code)