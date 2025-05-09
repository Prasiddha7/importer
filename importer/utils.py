import os
import re
import pandas as pd
from django.db import transaction
from datetime import datetime
from .models import Product, ImportLog, ImportSummary

MANDATORY_FIELDS = ['id', 'title', 'image_link', 'description', 'link', 'price', 'availability', 'brand', 'gtin']
RECOMMENDED_FIELDS = ['sale_price', 'shipping', 'item_group_id', 'google_product_category', 'product_type',
                      'material', 'pattern', 'color', 'product_length', 'product_width', 'product_height',
                      'product_weight', 'size', 'lifestyle_image_link', 'max_handling_time', 'is_bundle',
                      'model', 'condition']

def is_valid_number_string(value):
    try:
        float(str(value).strip())
        return True
    except (ValueError, TypeError):
        return False

def validate_row(row, existing_ids=None):
    errors = []
    warnings = []

    for field in MANDATORY_FIELDS:
        if pd.isna(row.get(field)) or row.get(field) == "":
            errors.append(f"Missing required field: {field}")


    for field in RECOMMENDED_FIELDS:
        if pd.isna(row.get(field)) or row.get(field) == "":
            warnings.append(f"Missing recommended field: {field}")

    number_string_fields = ['product_length', 'product_width', 'product_height', 'product_weight']
    for field in number_string_fields:
        value = row.get(field)
        if value and not is_valid_number_string(value):
            errors.append(f"Field '{field}' expected a number but got '{value}'.")

    if existing_ids is not None:
        product_id = row.get('id')
        if product_id in existing_ids:
            errors.append(f"ID '{product_id}' already exists.")

    return errors, warnings

def import_excel_file(file_path):
    start_time = datetime.now()
    df = pd.read_excel(file_path)

    # Normalize column names
    df.columns = [col.strip().lower() for col in df.columns]
    
    chunk_size = 100
    success_count = 0
    warning_count = 0
    error_count = 0

    for chunk_start in range(0, len(df), chunk_size):
        chunk = df.iloc[chunk_start:chunk_start + chunk_size]
        logs = []

        # Preload existing IDs in DB for this chunk
        chunk_ids = chunk['id'].dropna().unique()
        existing_ids = set(Product.objects.filter(id__in=chunk_ids).values_list('id', flat=True))

        try:
            with transaction.atomic():
                for index, row in chunk.iterrows():
                    row = row.to_dict()
                    row_number = index + 2 

                    errors, warnings = validate_row(row, existing_ids)

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


                        product = Product.objects.create(**product_data)
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