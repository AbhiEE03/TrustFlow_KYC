#!/bin/bash
# setup.sh - Initial setup script for TrustFlow KYC Monorepo Backend

echo "Setting up TrustFlow KYC Backend..."
cd backend

# Ensure virtual environment is activated in the current shell
if [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
elif [ -d "venv/bin" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please ensure it is created in backend/venv."
    exit 1
fi

# Make migrations for the custom apps
echo "Making migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations kyc

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create a superuser
echo "Creating superuser (you will be prompted for details)..."
python manage.py createsuperuser

echo "TrustFlow KYC Backend initialization complete!"
