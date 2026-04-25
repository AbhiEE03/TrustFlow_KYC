from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class KYCSubmission(models.Model):
    """
    Core state machine for KYC workflow.
    Valid transitions: draft -> submitted -> under_review -> [approved, rejected, more_info_requested]
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info_requested', 'More Info Requested'),
    )

    merchant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='kyc_submission')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    expected_monthly_volume = models.DecimalField(max_digits=12, decimal_places=2)
    pan_document = models.FileField(upload_to='kyc_documents/pan/')
    aadhaar_document = models.FileField(upload_to='kyc_documents/aadhaar/')
    bank_statement = models.FileField(upload_to='kyc_documents/bank_statements/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"KYC - {self.business_name} ({self.get_status_display()})"

    def transition_state(self, new_state):
        valid_transitions = {
            'draft': ['submitted'],
            'submitted': ['under_review'],
            'under_review': ['approved', 'rejected', 'more_info_requested'],
            'more_info_requested': ['submitted'],
            'approved': [],
            'rejected': [],
        }

        allowed_next_states = valid_transitions.get(self.status, [])
        if new_state not in allowed_next_states:
            raise ValidationError(f"Invalid state transition from '{self.status}' to '{new_state}'.")

        old_state = self.status
        self.status = new_state
        self.save()

        NotificationEvent.objects.create(
            merchant=self.merchant,
            event_type='status_change',
            old_state=old_state,
            new_state=new_state
        )

class NotificationEvent(models.Model):
    merchant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    event_type = models.CharField(max_length=100)
    old_state = models.CharField(max_length=50, blank=True, null=True)
    new_state = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event: {self.event_type} for {self.merchant.username}"
