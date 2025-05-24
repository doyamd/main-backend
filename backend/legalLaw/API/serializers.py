from rest_framework import serializers
from legalLaw.models import LegalDocument
from utils.upload import upload_file
from legalLaw.constants.category import LegalCategory
from legalLaw.constants.jurisdiction import Jurisdiction
from legalLaw.constants.language import Language

class LegalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocument
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'document_url']

class LegalDocumentCreateSerializer(serializers.ModelSerializer):
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
            'document',
        ]

    def validate_category(self, value):
        if value not in dict(LegalCategory.choices()).keys():
            raise serializers.ValidationError(
                f"Invalid category. Available options: {list(dict(LegalCategory.choices()).keys())}"
            )
        return value

    def validate_jurisdiction(self, value):
        if value not in dict(Jurisdiction.choices()).keys():
            raise serializers.ValidationError(
                f"Invalid jurisdiction. Available options: {list(dict(Jurisdiction.choices()).keys())}"
            )
        return value

    def validate_language(self, value):
        if value not in dict(Language.choices()).keys():
            raise serializers.ValidationError(
                f"Invalid language. Available options: {list(dict(Language.choices()).keys())}"
            )
        return value

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
        document_file = validated_data.pop('document')
        document_url, public_id = upload_file(document_file, folder="legal_documents")

        legal_doc = LegalDocument.objects.create(
            document_url=document_url,
            **validated_data
        )
        return legal_doc