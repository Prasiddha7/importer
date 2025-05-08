# import os
# import pandas as pd
# from django.db import transaction
# from .models import Product, ImportLog, ImportSummary
# from datetime import datetime

# def validate_row(row):
#     mandatory_fields = ['id', 'title', 'description', 'link', 'image_link', 'availability', 'price', 'condition', 'brand', 'gtin']
#     errors = []
#     warnings = []
#     for field in mandatory_fields:
#         if pd.isna(row.get(field)):
#             errors.append(f"Missing required field: {field}")

#     recommended_fields = ['sale_price', 'item_group_id', 'google_product_category', 'product_type', 'shipping', 'additional_image_links', 'size', 'color', 'material', 'pattern', 'gender', 'model']
#     for field in recommended_fields:
#         if pd.isna(row.get(field)):
#             warnings.append(f"Missing recommended field: {field}")

#     return errors, warnings
 

# def import_excel_file(file_path):
#     start_time = datetime.now()
#     df = pd.read_excel(file_path)

#     chunk_size = 100
#     success_count = 0
#     warning_count = 0
#     error_count = 0

#     for chunk_start in range(0, len(df), chunk_size):
#         chunk = df.iloc[chunk_start:chunk_start + chunk_size]
#         logs = []

#         try:
#             with transaction.atomic():
#                 for index, row in chunk.iterrows():
#                     row_number = index + 2  # +2 since Excel headers start at 1

#                     errors, warnings = validate_row(row)

#                     if errors:
#                         logs.append(ImportLog(row_number=row_number, status='error', message='; '.join(errors)))
#                         error_count += 1
#                         continue

#                     try:
#                         Product.objects.create(**{
#                             f.name: row.get(f.name)
#                             for f in Product._meta.fields if f.name != 'id'
#                         })
#                         print(f"Inserted row {row_number} into Product")
#                         logs.append(ImportLog(row_number=row_number, status='success', message='Inserted successfully'))
#                         success_count += 1

#                         if warnings:
#                             logs.append(ImportLog(row_number=row_number, status='warning', message='; '.join(warnings)))
#                             warning_count += 1
#                     except Exception as e:
#                         logs.append(ImportLog(row_number=row_number, status='error', message=str(e)))
#                         error_count += 1
#         except Exception as e:
#             # If the entire chunk fails (e.g., DB-level error), log generic error per row
#             for index, row in chunk.iterrows():
#                 row_number = index + 2
#                 logs.append(ImportLog(row_number=row_number, status='error', message='Chunk-level failure: ' + str(e)))
#                 error_count += 1

#         # Bulk log after each chunk
#         ImportLog.objects.bulk_create(logs)

#     summary = ImportSummary.objects.create(
#         file_name=os.path.basename(file_path),
#         total=len(df),
#         success=success_count,
#         warnings=warning_count,
#         errors=error_count,
#         duration=datetime.now() - start_time
#     )

#     return summary


import os
import pandas as pd
from django.db import transaction
from .models import Product, ImportLog, ImportSummary
from datetime import datetime

MANDATORY_FIELDS = ['id', 'title', 'image_link', 'description', 'link', 'price', 'availability', 'brand', 'gtin']
RECOMMENDED_FIELDS = ['sale_price', 'shipping', 'item_group_id', 'google_product_category', 'product_type', 'material', 'pattern', 'color', 'product_length', 'product_width', 'product_height', 'product_weight', 'size', 'lifestyle_image_link', 'max_handling_time', 'is_bundle', 'model', 'condition']


import re

def is_valid_number_string(value):
    if pd.isna(value):
        return True 
    return bool(re.match(r'^\s*[\d\.]+', str(value)))

def validate_row(row):
    errors = []
    warnings = []

    for field in MANDATORY_FIELDS:
        if pd.isna(row.get(field)):
            errors.append(f"Missing required field: {field}")

    for field in RECOMMENDED_FIELDS:
        if pd.isna(row.get(field)):
            warnings.append(f"Missing recommended field: {field}")

    
    number_string_fields = ['product_length', 'product_width', 'product_height', 'product_weight']
    for field in number_string_fields:
        value = row.get(field)
        if not is_valid_number_string(value):
            errors.append(f"Field '{field}' expected a number but got '{value}'.")

    return errors, warnings

def import_excel_file(file_path):
    start_time = datetime.now()
    df = pd.read_excel(file_path)

    df.columns = [col.strip().lower() for col in df.columns]

    print("Excel Columns:", df.columns.tolist()) 

    chunk_size = 100
    success_count = 0
    warning_count = 0
    error_count = 0

    for chunk_start in range(0, len(df), chunk_size):
        chunk = df.iloc[chunk_start:chunk_start + chunk_size]
        logs = []

        try:
            with transaction.atomic():
                for index, row in chunk.iterrows():
                    row = row.to_dict()
                    row_number = index + 2

                    errors, warnings = validate_row(row)

                    if errors:
                        logs.append(ImportLog(row_number=row_number, status='error', message='; '.join(errors)))
                        error_count += 1
                        continue

                    try:
                        product_data = {
                            'id': row.get('id'),
                            'title': row.get('title'),
                            'image_link': row.get('image_link'),
                            'description': row.get('description'),
                            'link': row.get('link'),
                            'price': row.get('price'),
                            'sale_price': row.get('sale_price'),
                            'shipping': row.get('shipping(country:price)'),
                            'item_group_id': row.get('item_group_id'),
                            'availability': row.get('availability'),
                            'additional_image_links': row.get('additional_image_links'),
                            'brand': row.get('brand'),
                            'gtin': row.get('gtin'),
                            'gender': row.get('gender'),
                            'google_product_category': row.get('google_product_category'),
                            'product_type': row.get('product_type'),
                            'material': row.get('material'),
                            'pattern': row.get('pattern'),
                            'color': row.get('color'),
                            'product_length': row.get('product_length'),
                            'product_width': row.get('product_width'),
                            'product_height': row.get('product_height'),
                            'product_weight': row.get('product_weight'),
                            'size': row.get('size'),
                            'lifestyle_image_link': row.get('lifestyle_image_link'),
                            'max_handling_time': row.get('max_handling_time'),
                            'is_bundle': row.get('is_bundle'),
                            'model': row.get('model'),
                            'condition': row.get('condition'),
                        }
                        print('product_data', product_data)  

                        # Create and save the product instance
                        product = Product.objects.create(**product_data)
                        print('product', product)  
                        product.save()
                        logs.append(ImportLog(row_number=row_number, status='success', message='Inserted successfully'))
                        success_count += 1

                        if warnings:
                            logs.append(ImportLog(row_number=row_number, status='warning', message='; '.join(warnings)))
                            warning_count += 1
                    except Exception as e:
                        logs.append(ImportLog(row_number=row_number, status='error', message=str(e)))
                        error_count += 1
        except Exception as e:
            for index, row in chunk.iterrows():
                row_number = index + 2
                logs.append(ImportLog(row_number=row_number, status='error', message='Chunk-level failure: ' + str(e)))
                error_count += 1

        ImportLog.objects.bulk_create(logs)

    summary = ImportSummary.objects.create(
        file_name=os.path.basename(file_path),
        total=len(df),
        success=success_count,
        warnings=warning_count,
        errors=error_count,
        duration=datetime.now() - start_time
    )

    return summary

