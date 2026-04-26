from django.contrib.auth import get_user_model
from kyc.models import KYCSubmission

User = get_user_model()

def seed():
    # 1. Create Reviewer
    reviewer, created = User.objects.get_or_create(
        username='reviewer_1',
        email='reviewer@example.com',
        role='reviewer'
    )
    if created:
        reviewer.set_password('pass1234')
        reviewer.save()
        print("Created Reviewer: reviewer_1")

    # 2. Create Merchant 1 (draft)
    merchant_draft, created = User.objects.get_or_create(
        username='merchant_draft',
        email='draft@example.com',
        role='merchant'
    )
    if created:
        merchant_draft.set_password('pass1234')
        merchant_draft.save()
        print("Created Merchant: merchant_draft")

    submission1, created = KYCSubmission.objects.get_or_create(
        merchant=merchant_draft,
        defaults={
            'status': 'draft',
            'full_name': 'Alice Draft',
            'business_name': 'Alice Retail',
            'business_type': 'Retail',
            'expected_monthly_volume': 1000.00
        }
    )
    if created:
        print("Created KYCSubmission (draft) for merchant_draft")

    # 3. Create Merchant 2 (under_review)
    merchant_review, created = User.objects.get_or_create(
        username='merchant_review',
        email='review@example.com',
        role='merchant'
    )
    if created:
        merchant_review.set_password('pass1234')
        merchant_review.save()
        print("Created Merchant: merchant_review")

    submission2, created = KYCSubmission.objects.get_or_create(
        merchant=merchant_review,
        defaults={
            'status': 'under_review',
            'full_name': 'Bob Review',
            'business_name': 'Bob Services',
            'business_type': 'Services',
            'expected_monthly_volume': 5000.00
        }
    )
    if created:
        print("Created KYCSubmission (under_review) for merchant_review")

if __name__ == '__main__':
    seed()
