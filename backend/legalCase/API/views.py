from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from legalCase.models import Case
from legalCase.API.serializers import CaseSerializer
from legalUser.API.permissions import IsClientOrAdmin
from legalUser.common.commonresponse import BaseResponse
from utils.upload import upload_file


class CaseListCreateAV(APIView):
    permission_classes = [IsClientOrAdmin]

    def get(self, request):
        response = BaseResponse()
        user = request.user
        cases = Case.objects.filter(user=user)
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
    permission_classes = [IsClientOrAdmin]

    def get_object(self, pk, user):
        try:
            case = Case.objects.get(id=pk, user=user)
            return case
        except Case.DoesNotExist:
            return None

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