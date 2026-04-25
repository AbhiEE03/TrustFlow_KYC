from django.contrib import admin
from .models import KYCSubmission, NotificationEvent

@admin.register(KYCSubmission)
class KYCSubmissionAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'business_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('business_name', 'merchant__username', 'email')

@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'event_type', 'old_state', 'new_state', 'timestamp')
    list_filter = ('event_type', 'timestamp')
    search_fields = ('merchant__username',)
