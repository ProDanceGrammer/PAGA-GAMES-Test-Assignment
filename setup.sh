#!/bin/bash
# Quick setup script for local development

echo "Starting Django API Aggregator setup..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
source .venv/Scripts/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements/development.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update .env with your API keys!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your API keys"
echo "2. Start Docker services: docker-compose up -d"
echo "3. Create superuser: python manage.py createsuperuser"
echo "4. Fetch initial data: python manage.py fetch_data"
echo "5. Start server: python manage.py runserver"
