Django Excel Product File Importer
A Django application to import product data from Excel files in chunks with validation, logging, and analytics summary tracking.

#Installation
git clone https://github.com/Prasiddha7/importer.git

#create virtual environment
python -m venv env
source env/bin/activate

#Install requirements and dependencies
pip install -r requirements.txt

# Migrate data
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver

#API ENDPOINTS
Action	URL	Method
Upload Excel	http://127.0.0.1:8000//api/upload/	POST
View Summary	http://127.0.0.1:8000/api/summary/1/	GET
View Logs	http://127.0.0.1:8000/api/import-logs/	GET
if filter required use params status,filter by status http://127.0.0.1:8000/api/import-logs/?status=success
View Products	http://127.0.0.1:8000/api/products/	GET


 

#Features
Upload Excel files containing product data

Chunked processing (100 rows per batch) for memory efficiency

Row-level validation:

Mandatory and recommended fields

Numeric string checks for dimensions and weight

Duplicate ID detection

Import logs with success, warning, and error statuses

Summary of the import process (success/warning/error counts & duration)

#REST API for:

Uploading files

Viewing logs

Viewing summary

Listing imported products

