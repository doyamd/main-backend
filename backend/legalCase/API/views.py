from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from legalCase.models import Case, CaseRequest
from legalCase.API.serializers import CaseSerializer, CaseRequestSerializer, CaseRequestDecisionSerializer, AttorneyWithCaseStatsSerializer
from legalUser.API.permissions import IsClientOrAdmin, IsClientOrAdminOrAttorney, IsAttorneyOrAdmin, IsAdmin
from legalUser.common.commonresponse import BaseResponse
from utils.upload import upload_file
from legalUser.models import Attorney, User

class CaseListCreateAV(APIView):
    permission_classes = [IsClientOrAdminOrAttorney]

    def get(self, request):
        response = BaseResponse()
        user = request.user
        cases = Case.objects.filter(user=user)
        if user.role == 'attorney':
            caseRequests = CaseRequest.objects.filter(attorney=user)
            case_ids = caseRequests.values_list('case', flat=True)
            cases = Case.objects.filter(id__in=case_ids)
        serializer = CaseSerializer(cases, many=True)
        response.update(200, True, "Cases retrieved successfully", serializer.data)
        return Response(response.to_dict(), status=response.status_code)

    def post(self, request):
        response = BaseResponse()
        user = request.user

        if user.role != 'client':
            response.update(403, False, "Only clients can create cases")
            return Response(response.to_dict(), status=response.status_code)

        title = request.data.get('title')
        description = request.data.get('description')
        document_file = request.FILES.get('document')

        if not all([title, description, document_file]):
            response.update(400, False, "Title, description, and document are required")
            return Response(response.to_dict(), status=response.status_code)

        try:
            # Upload the document file
            file_url, public_id = upload_file(document_file, folder="case_documents")

            case = Case.objects.create(
                user=user,
                title=title,
                description=description,
                document=file_url
            )

            serializer = CaseSerializer(case)
            response.update(201, True, "Case created successfully", serializer.data)
        except Exception as e:
            response.update(500, False, f"Failed to create case: {str(e)}")

        return Response(response.to_dict(), status=response.status_code)
    
class CaseDetailAV(APIView):
    permission_classes = [IsClientOrAdminOrAttorney]

    def get_object(self, pk, user):
        try:
            case = Case.objects.get(id=pk, user=user)
            return case
        except Case.DoesNotExist:
            return None
        
    def get(self, request, pk):
        response = BaseResponse()

        try:
            case = Case.objects.get(id=pk)
        except Case.DoesNotExist:
            response.update(404, False, "Case not found")
            return Response(response.to_dict(), status=response.status_code)

        if case.user == request.user:
            pass  # client owns the case

        elif request.user.role == "attorney":
            case_request_exists = CaseRequest.objects.filter(
                case=case,
                attorney=request.user
            ).exists()

            if not case_request_exists:
                response.update(403, False, "Permission denied: no valid case request")
                return Response(response.to_dict(), status=response.status_code)
        else:
            response.update(403, False, "Permission denied")
            return Response(response.to_dict(), status=response.status_code)

        # Authorized
        serializer = CaseSerializer(case)
        response.update(200, True, "Case retrieved successfully", serializer.data)
        return Response(response.to_dict(), status=response.status_code)

    def patch(self, request, pk):
        response = BaseResponse()
        case = self.get_object(pk, request.user)
        if not case:
            response.update(404, False, "Case not found or permission denied")
            return Response(response.to_dict(), status=response.status_code)

        # Check if there's a new document file
        document_file = request.FILES.get('document')
        if document_file:
            try:
                # Upload the new document file
                file_url, public_id = upload_file(document_file, folder="case_documents")
                request.data['document'] = file_url
            except Exception as e:
                response.update(500, False, f"Failed to upload document: {str(e)}")
                return Response(response.to_dict(), status=response.status_code)

        serializer = CaseSerializer(case, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response.update(200, True, "Case updated successfully", serializer.data)
        else:
            response.update(400, False, "Invalid update data", serializer.errors)
        return Response(response.to_dict(), status=response.status_code)

    def delete(self, request, pk):
        response = BaseResponse()
        case = self.get_object(pk, request.user)
        if not case:
            response.update(404, False, "Case not found or permission denied")
            return Response(response.to_dict(), status=response.status_code)

        case.delete()
        response.update(200, True, "Case deleted successfully")
        return Response(response.to_dict(), status=response.status_code)
    
class CaseRequestListCreateAV(APIView):
    permission_classes = [IsClientOrAdminOrAttorney]

    def get(self, request):
        response = BaseResponse()
        user = request.user

        if user.role == 'client':
            case_ids = Case.objects.filter(user=user).values_list('id', flat=True)
            requests = CaseRequest.objects.filter(case__id__in=case_ids)
        elif user.role == 'attorney':
            requests = CaseRequest.objects.filter(attorney=user)
        else:  # admin sees all
            requests = CaseRequest.objects.all()

        serializer = CaseRequestSerializer(requests, many=True)
        response.update(200, True, "Case requests retrieved successfully", serializer.data)
        return Response(response.to_dict(), status=response.status_code)

    def post(self, request):
        response = BaseResponse()
        user = request.user

        if user.role != 'client':
            response.update(403, False, "Only clients can create case requests")
            return Response(response.to_dict(), status=response.status_code)
        
        serializer = CaseRequestSerializer(data=request.data)
        if not serializer.is_valid():
            response.update(400, False, "Invalid data", serializer.errors)
            return Response(response.to_dict(), status=response.status_code)

        case = serializer.validated_data['case']
        if user.role == 'client' and case.user != user:
            response.update(403, False, "You can only create requests for your own cases")
            return Response(response.to_dict(), status=response.status_code)

        case_request = serializer.save()
        response.update(201, True, "Case request created successfully", CaseRequestSerializer(case_request).data)
        return Response(response.to_dict(), status=response.status_code)
    
class CaseRequestDecisionView(APIView):
    permission_classes = [IsAttorneyOrAdmin]

    def patch(self, request, pk):
        try:
            case_request = CaseRequest.objects.get(pk=pk)
        except CaseRequest.DoesNotExist:
            return Response(BaseResponse(
                status_code=404,
                success=False,
                message="Case request not found"
            ).to_dict())

        # Attorney can only respond to their own requests
        if request.user.role == "attorney" and case_request.attorney != request.user:
            return Response(BaseResponse(
                status_code=403,
                success=False,
                message="You can only respond to your own case requests"
            ).to_dict())

        serializer = CaseRequestDecisionSerializer(case_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(BaseResponse(
                status_code=200,
                success=True,
                message=f"Case request {serializer.validated_data['status']} successfully",
                data=serializer.data
            ).to_dict())

        return Response(BaseResponse(
            status_code=400,
            success=False,
            message="Invalid data",
            data=serializer.errors
        ).to_dict())
    
class AttorneyWithCasesAPIView(APIView):
    permission_classes = [IsAdmin] 

    def get(self, request):
        attorneys = Attorney.objects.all().select_related('user')
        serializer = AttorneyWithCaseStatsSerializer(attorneys, many=True)
        return Response({'attorneys': serializer.data})