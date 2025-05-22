from rest_framework import serializers
from legalLaw.models import LegalDocument
from utils.upload import upload_file

class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'document_url']

class LegalDocumentCreateSerializer(serializers.ModelSerializer):
    # Add an extra field to handle the uploaded file
    document = serializers.FileField(write_only=True, required=True)

    class Meta:
        model = LegalDocument
        fields = [
            'title',
            'description',
            'category',
            'jurisdiction',
            'language',
            'proclamation_number',
            'publication_year',
            'document',  # only used for upload
        ]

    def validate(self, data):
        required_fields = [
            'title',
            'description',
            'category',
            'jurisdiction',
            'language',
            'proclamation_number',
            'publication_year',
            'document'
        ]
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError({field: "This field is required."})
        return data

    def create(self, validated_data):
        # Extract and upload the file
        document_file = validated_data.pop('document')
        document_url, public_id = upload_file(document_file, folder="legal_documents")

        # Create the LegalDocument instance
        legal_doc = LegalDocument.objects.create(
            document_url=document_url,
            **validated_data
        )
        return legal_doc