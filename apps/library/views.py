import chardet
import pandas as pd
import os
import io
import csv
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from django.db import models as django_models
from .models import LibraryCatalog
from .forms import CSVImportForm


@login_required
def import_csv(request):
    """Import CSV file with library catalog data"""
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file')
                return redirect('import_csv')
            
            # Save file temporarily
            file_path = os.path.join(settings.MEDIA_ROOT, 'temp', csv_file.name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)
            
            try:
                # Detect encoding automatically
                with open(file_path, 'rb') as f:
                    raw_data = f.read()
                    encoding_result = chardet.detect(raw_data)
                    detected_encoding = encoding_result['encoding']
                    confidence = encoding_result['confidence']
                    
                    messages.info(request, f'Detected encoding: {detected_encoding} (confidence: {confidence:.2%})')
                
                # Try multiple encodings
                encodings_to_try = [
                    detected_encoding,
                    'utf-8-sig',
                    'latin-1',
                    'iso-8859-1',
                    'cp1252',
                    'utf-16',
                    'utf-16le',
                    'utf-16be',
                    'mac_roman',
                    'ascii'
                ]
                
                df = None
                used_encoding = None
                
                for encoding in encodings_to_try:
                    try:
                        if encoding:
                            df = pd.read_csv(file_path, encoding=encoding, on_bad_lines='skip')
                            used_encoding = encoding
                            break
                    except Exception:
                        continue
                
                if df is None:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        decoded = content.decode('utf-8', errors='ignore')
                        df = pd.read_csv(io.StringIO(decoded))
                        used_encoding = 'utf-8 (with errors ignored)'
                
                messages.success(request, f'Successfully read CSV with encoding: {used_encoding}')
                messages.info(request, f'Found {len(df)} rows and {len(df.columns)} columns')
                
                # Process the data
                created_count = 0
                updated_count = 0
                error_count = 0
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        data = map_csv_to_model(row)
                        
                        if not data.get('control_no'):
                            error_count += 1
                            errors.append(f'Row {index + 2}: Missing control_no')
                            continue
                        
                        control_no = data['control_no']
                        
                        if LibraryCatalog.objects.filter(control_no=control_no).exists():
                            if form.cleaned_data.get('update_existing'):
                                LibraryCatalog.objects.filter(control_no=control_no).update(**data)
                                updated_count += 1
                            else:
                                continue
                        else:
                            LibraryCatalog.objects.create(**data)
                            created_count += 1
                    
                    except Exception as e:
                        error_count += 1
                        errors.append(f'Row {index + 2}: {str(e)}')
                
                os.remove(file_path)
                
                messages.success(request, f'✅ Import completed! Created: {created_count}, Updated: {updated_count}, Errors: {error_count}')
                
                if errors:
                    messages.warning(request, f'Errors occurred:\n' + '\n'.join(errors[:5]))
                    if len(errors) > 5:
                        messages.warning(request, f'... and {len(errors) - 5} more errors')
                
                return redirect('library:import_csv')
            
            except Exception as e:
                messages.error(request, f'Error processing CSV: {str(e)}')
                if os.path.exists(file_path):
                    os.remove(file_path)
                return redirect('library:import_csv')
    
    else:
        form = CSVImportForm()
    
    return render(request, 'import_csv.html', {'form': form})


def map_csv_to_model(row):
    """Map pandas row data to model fields"""
    data = {}
    
    def safe_get_value(value):
        if pd.isna(value) or value is None:
            return None
        if isinstance(value, (int, float)):
            return str(value)
        cleaned = str(value).strip()
        if cleaned and cleaned.lower() not in ['nan', 'none', 'null', '']:
            return cleaned
        return None
    
    field_mapping = {
        'ID': 'id',
        'Control No': 'control_no',
        'Date Time Stamp': 'date_time_stamp',
        'Fixed Length Data': 'fixed_length_data',
        'ISBN': 'isbn',
        'ISSN': 'issn',
        'Price': 'price',
        'Cataloging Source A': 'cataloging_source_a',
        'Cataloging Source B': 'cataloging_source_b',
        'Cataloging Source E': 'cataloging_source_e',
        'Main Author': 'main_author',
        'Title Statement': 'title_statement',
        'Title Author': 'title_author',
        'Edition': 'edition',
        'Publication Place': 'publication_place',
        'Publisher': 'publisher',
        'Publication Year': 'publication_year',
        'Pages': 'pages',
        'Illustrations': 'illustrations',
        'Size': 'size',
        'Volume': 'volume',
        'Content Type': 'content_type',
        'Content Code': 'content_code',
        'Media Type': 'media_type',
        'Media Code': 'media_code',
        'Carrier Type': 'carrier_type',
        'Carrier Code': 'carrier_code',
        'Series Title': 'series_title',
        'General Note': 'general_note',
        'Bibliography Note': 'bibliography_note',
        'Source Vendor': 'source_vendor',
        'Source Date': 'source_date',
        'Subject Topic': 'subject_topic',
        'Subject Form': 'subject_form',
        'Genre': 'genre',
        'Library Name': 'library_name',
        'Section': 'section',
        'Call Number': 'call_number',
        'Accession No': 'accession_no',
        'Barcode': 'barcode',
        'RFID': 'rfid',
        'Availability': 'availability',
        'Year': 'year',
        'Course': 'course',
        'Cover Image': 'cover_image',
        'Added Entry Elements': 'added_entry_elements',
        'Corporate Name': 'corporate_name',
        'Personal Name': 'personal_name',
        'Faceted Topical Terms': 'faceted_topical_terms',
        'Genre Form': 'genre_form',
        'Topical Term': 'topical_term',
        'Geographical Name': 'geographical_name',
        'Uniform Title': 'uniform_title',
        'Chronological Term': 'chronological_term',
        'Subject Corporate Name': 'subject_corporate_name',
        'Subject Personal Name': 'subject_personal_name',
        'Summary': 'summary',
        'Publication Distribution': 'publication_distribution',
        'Main Corporate Name': 'main_corporate_name',
        'DDC Number': 'ddc_number',
        'Leader': 'leader',
        'Control Number Identifier': 'control_number_identifier',
        'Acquisition Type ID': 'acquisition_type_id',
        'Acquisition Custom': 'acquisition_custom',
        'Programs': 'programs',
        'Archived At': 'archived_at',
        'Deleted At': 'deleted_at',
        'Created At': 'created_at',
        'Updated At': 'updated_at',
    }
    
    for csv_field, model_field in field_mapping.items():
        if csv_field in row.index:
            value = safe_get_value(row[csv_field])
            if value is not None:
                data[model_field] = value
    
    # Handle special fields
    if 'Date Time Stamp' in row.index and pd.notna(row['Date Time Stamp']):
        try:
            data['date_time_stamp'] = pd.to_datetime(row['Date Time Stamp'])
        except:
            pass
    
    if 'Source Date' in row.index and pd.notna(row['Source Date']):
        try:
            data['source_date'] = pd.to_datetime(row['Source Date']).date()
        except:
            pass
    
    if 'Archived At' in row.index and pd.notna(row['Archived At']):
        try:
            data['archived_at'] = pd.to_datetime(row['Archived At'])
        except:
            pass
    
    if 'Deleted At' in row.index and pd.notna(row['Deleted At']):
        try:
            data['deleted_at'] = pd.to_datetime(row['Deleted At'])
        except:
            pass
    
    if 'Created At' in row.index and pd.notna(row['Created At']):
        try:
            data['created_at'] = pd.to_datetime(row['Created At'])
        except:
            pass
    
    if 'Updated At' in row.index and pd.notna(row['Updated At']):
        try:
            data['updated_at'] = pd.to_datetime(row['Updated At'])
        except:
            pass
    
    if 'Price' in row.index and pd.notna(row['Price']):
        try:
            price_str = str(row['Price']).strip().replace('$', '').replace(',', '')
            data['price'] = float(price_str) if price_str else None
        except:
            pass
    
    if 'Availability' in row.index and pd.notna(row['Availability']):
        try:
            val = str(row['Availability']).strip().lower()
            data['availability'] = val in ['true', 'yes', '1', 'available', 't', 'y']
        except:
            data['availability'] = False
    
    if 'id' in data and data['id']:
        try:
            data['id'] = int(data['id'])
        except:
            pass
    
    if 'control_no' in data:
        data['control_no'] = str(data['control_no']).strip()
    
    return data


def download_sample_csv(request):
    """Download a sample CSV template with all fields"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_library_catalog.csv"'
    
    writer = csv.writer(response, quoting=csv.QUOTE_ALL)
    
    headers = [
        'ID', 'Control No', 'Date Time Stamp', 'Fixed Length Data', 'ISBN', 'ISSN',
        'Price', 'Cataloging Source A', 'Cataloging Source B', 'Cataloging Source E',
        'Main Author', 'Title Statement', 'Title Author', 'Edition', 'Publication Place',
        'Publisher', 'Publication Year', 'Pages', 'Illustrations', 'Size', 'Volume',
        'Content Type', 'Content Code', 'Media Type', 'Media Code', 'Carrier Type',
        'Carrier Code', 'Series Title', 'General Note', 'Bibliography Note',
        'Source Vendor', 'Source Date', 'Subject Topic', 'Subject Form', 'Genre',
        'Library Name', 'Section', 'Call Number', 'Accession No', 'Barcode', 'RFID',
        'Availability', 'Year', 'Course', 'Cover Image', 'Added Entry Elements',
        'Corporate Name', 'Personal Name', 'Faceted Topical Terms', 'Genre Form',
        'Topical Term', 'Geographical Name', 'Uniform Title', 'Chronological Term',
        'Subject Corporate Name', 'Subject Personal Name', 'Summary',
        'Publication Distribution', 'Main Corporate Name', 'DDC Number', 'Leader',
        'Control Number Identifier', 'Acquisition Type ID', 'Acquisition Custom',
        'Programs', 'Archived At', 'Deleted At', 'Created At', 'Updated At'
    ]
    writer.writerow(headers)
    
    sample_data = [
        '', 'LC001', '2024-01-15 10:30:00', '', '978-3-16-148410-0', '',
        '29.99', 'DLC', 'eng', 'rda', 'John Doe', 'The Art of Programming',
        'John Doe', '2nd ed.', 'New York', 'Tech Publishers', '2024', '350 p.',
        'ill.', '24 cm', '1', 'text', 'txt', 'unmediated', 'n', 'volume', 'nc',
        'Programming Series', 'Includes index', 'Includes bibliographic references',
        'Amazon', '2024-01-01', 'Programming', 'Textbooks', 'Non-fiction',
        'Main Library', 'Reference', 'QA76.73.P98 D64 2024', 'ACC001', 'BAR001',
        'RFID001', 'Available', '2024', 'CS101', 'https://example.com/cover.jpg',
        'Added entry 1', 'Tech Corp', 'Jane Smith', 'Programming', 'Handbooks',
        'Programming', 'United States', 'Python Cookbook', '21st century',
        'Computer Science Corp', 'Smith, John', 'A comprehensive guide',
        'Worldwide', 'Tech Corp', '005.133', 'nam a22 7a 4500', 'LC001-2024',
        '1', 'Custom info', 'BSHM, BSIT', '', '', '2024-01-15 10:30:00',
        '2024-01-15 10:30:00'
    ]
    writer.writerow(sample_data)
    
    return response


def catalog_list(request):
    """Display list of catalog records"""
    records = LibraryCatalog.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        records = records.filter(
            django_models.Q(control_no__icontains=search_query) |
            django_models.Q(title_statement__icontains=search_query) |
            django_models.Q(main_author__icontains=search_query) |
            django_models.Q(isbn__icontains=search_query) |
            django_models.Q(call_number__icontains=search_query)
        )
    
    paginator = Paginator(records, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_records': records.count(),
    }
    
    return render(request, 'catalog_list.html', context)


def catalog_detail(request, pk):
    """Display detail of a single catalog record"""
    record = get_object_or_404(LibraryCatalog, pk=pk)
    return render(request, 'catalog_detail.html', {'record': record})


def catalog_delete(request, pk):
    """Delete a catalog record"""
    if request.method == 'POST':
        record = get_object_or_404(LibraryCatalog, pk=pk)
        record.delete()
        messages.success(request, f'Record {record.control_no} deleted successfully!')
        return redirect('catalog_list')
    
    record = get_object_or_404(LibraryCatalog, pk=pk)
    return render(request, 'catalog_confirm_delete.html', {'record': record})