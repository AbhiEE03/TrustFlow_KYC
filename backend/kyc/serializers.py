from rest_framework import serializers

from kyc.models import KYCSubmission

class KYCSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCSubmission
        fields = '__all__'
        read_only_fields = ('merchant', 'status', 'created_at', 'updated_at')

    def validate_file_extension(self, file_obj, field_name):
        if not file_obj:
            return file_obj
        
        valid_extensions = ['.pdf', '.jpg', '.png']
        file_name = file_obj.name.lower()
        if not any(file_name.endswith(ext) for ext in valid_extensions):
            raise serializers.ValidationError(
                f"Invalid format for {field_name}. Only PDF, JPG, and PNG allowed."
            )
        return file_obj

    def validate_pan_document(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 5 MB.")
        return self.validate_file_extension(value, 'PAN Document')

    def validate_aadhaar_document(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 5 MB.")
        return self.validate_file_extension(value, 'Aadhaar Document')

    def validate_bank_statement(self, value):
        if value and value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 5 MB.")
        return self.validate_file_extension(value, 'Bank Statement')
