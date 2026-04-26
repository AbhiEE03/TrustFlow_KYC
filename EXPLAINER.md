Playto Pay KYC Module Explainer
This document outlines the architectural decisions and technical implementations for the Playto Pay KYC onboarding system.

1. The State Machine (Data Integrity)
   Our state machine logic acts as the single source of truth within the transition_state method inside backend/kyc/models.py. It defines a strict mapping of allowed transitions (e.g., draft -> submitted).

Why this approach? By handling transitions at the model layer, we guarantee database consistency. If a new_state is requested that isn't in the allowed map, the model raises a standard Django ValidationError. This blocks invalid transitions at the lowest data layer, preventing any upstream UI or API flaws from breaking business logic. Successful transitions also trigger an automatic NotificationEvent to keep the merchant informed in real-time.

2. Document Validation (Security)
   File uploads undergo robust verification via custom validation methods (validate_pan_document, validate_aadhaar_document, etc.) inside backend/kyc/serializers.py.

Verification: These functions inspect the file's name attribute and throw a DRF ValidationError if the extension is not exactly .pdf, .jpg, or .png. This prevents the execution of potentially malicious scripts through unsupported file types.

3. Priority Queue & SLA Tracking
   The reviewer's workflow is managed via the ReviewerQueueViewSet in backend/kyc/views.py.

Prioritization: To enforce our efficiency requirements, get_queryset returns only submissions with statuses of submitted, under_review, or more_info_requested, explicitly utilizing .order_by('created_at') to surface the oldest compliance tickets first.

Dynamic SLA: The frontend calculates the 24-hour SLA breach status dynamically using the created_at timestamp. This ensures that "At Risk" flags are always accurate to the current second without requiring expensive database updates or background cron jobs.

4. Authentication & Data Sovereignty
   Merchant data privacy is strictly preserved via the get_queryset method in MerchantKYCViewSet.

Prevention of Privilege Escalation: By returning KYCSubmission.objects.filter(merchant=self.request.user), the ORM explicitly scopes the database query to the currently authenticated session's user ID. This architectural pattern structurally prevents any merchant from executing a horizontal privilege escalation attack to access another entity's KYC data.

5. AI Audit & Manual Corrections
   During the initial boilerplate generation for the KYCSubmissionSerializer, the automated tools successfully implemented file extension validation but completely overlooked the 5MB file size limit requested in the project requirements.

The Fix: I identified this gap and manually implemented a value.size > max_size check within the serializer validation logic. This ensures that the system rejects oversized payloads (e.g., a 50MB PDF) at the API gateway level, protecting the server's storage and processing resources from being overwhelmed.
