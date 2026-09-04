import os
import re
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.conf import settings
from .models import LibraryCatalog

from django.contrib import admin

# Change the admin site header
admin.site.site_header = "MOIST LMS"
admin.site.site_title = "MOIST LMS"
admin.site.index_title = "Welcome to MOIST LMS"

@admin.register(LibraryCatalog)
class LibraryCatalogAdmin(admin.ModelAdmin):
    list_display = (
        'control_no', 
        'title_statement', 
        'main_author', 
        'call_number', 
        'availability',
        'cover_preview',
        'date_time_stamp'
    )
    
    list_filter = (
        'availability', 
        'library_name', 
        'publication_year',
        'content_type',
        'media_type',
        'carrier_type'
    )
    
    search_fields = (
        'control_no', 
        'isbn', 
        'issn', 
        'main_author', 
        'title_statement', 
        'call_number',
        'barcode',
        'rfid'
    )
    
    readonly_fields = ('created_at', 'updated_at', 'cover_preview', 'cover_image_preview', 'book_preview')
    
    def get_expected_filename(self, obj):
        """Get the expected filename based on title"""
        if obj.title_statement:
            # Clean title: remove special characters, replace spaces with underscores
            title = obj.title_statement[:100]
            title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            title = title.replace(' ', '_')
            return f"{title}"
        return None
    
    def get_display_title(self, obj):
        """Get display title from filename (replace underscores with spaces)"""
        expected_filename = self.get_expected_filename(obj)
        if expected_filename:
            return expected_filename.replace('_', ' ')
        return "Cover Image"
    
    def cover_preview(self, obj):
        """Display cover image thumbnail in list view"""
        if obj.cover_image:
            try:
                display_name = self.get_display_title(obj).replace(' ', '_') + '_' + str(obj.control_no) + '.jpg'
                # Get the URL
                if hasattr(obj.cover_image, 'url'):
                    url = obj.cover_image.url
                elif isinstance(obj.cover_image, str):
                    if obj.cover_image.startswith('http'):
                        url = obj.cover_image
                    else:
                        # Remove 'covers/' if present to avoid duplication
                        image_path = obj.cover_image
                        if image_path.startswith('covers/'):
                            image_path = image_path[7:]
                        url = f"{settings.MEDIA_URL}covers/{display_name}"
                else:
                    url = str(obj.cover_image)
                
                return format_html(
                    '<img src="{}" width="50" height="70" style="object-fit:cover; border-radius:4px;" title="{}" />',
                    url,
                    display_name
                )
            except Exception as e:
                return f"Error: {str(e)}"
        return "No Image"
    cover_preview.short_description = "Cover"
    
    def cover_image_preview(self, obj):
        """Display cover image preview in detail view"""
        if obj.cover_image:
            try:
                display_name = self.get_display_title(obj)
                expected_filename = self.get_expected_filename(obj)
                
                # Get the URL
                if hasattr(obj.cover_image, 'url'):
                    url = obj.cover_image.url
                    actual_filename = os.path.basename(obj.cover_image.name) if hasattr(obj.cover_image, 'name') else "unknown"
                elif isinstance(obj.cover_image, str):
                    if obj.cover_image.startswith('http'):
                        url = obj.cover_image
                        actual_filename = os.path.basename(obj.cover_image)
                    else:
                        # Remove 'covers/' if present to avoid duplication
                        image_path = obj.cover_image
                        if image_path.startswith('covers/'):
                            image_path = image_path[7:]
                        url = f"{settings.MEDIA_URL}covers/{image_path}"
                        actual_filename = os.path.basename(image_path)
                else:
                    url = str(obj.cover_image)
                    actual_filename = os.path.basename(url)
                
                return format_html(
                    '<div style="text-align:center;">'
                    '<img src="{}" width="200" height="280" style="object-fit:cover; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2);" />'
                    '<div style="margin-top:10px; padding:10px; background:#f5f5f5; border-radius:4px; display:inline-block; text-align:left;">'
                    '<p style="margin:0; font-style:italic; color:#333; font-size:14px;">📖 <strong>Title:</strong> {}</p>'
                    '<p style="margin:5px 0 0 0; color:#555; font-size:13px;">📁 <strong>Expected:</strong> {}</p>'
                    '<p style="margin:2px 0 0 0; color:#888; font-size:12px; font-family:monospace;">📂 <strong>Actual:</strong> {}</p>'
                    '</div>'
                    '</div>',
                    url,
                    display_name,
                    expected_filename if expected_filename else "Not set",
                    actual_filename
                )
            except Exception as e:
                return f"Error loading image: {str(e)}"
        return '<div style="text-align:center; padding:30px; color:#999; font-style:italic;">No Cover Image Available</div>'
    cover_image_preview.short_description = "Cover Image Preview"
    
    def book_preview(self, obj):
        """Display complete book preview with all details"""
        # Cover image
        cover_html = ""
        if obj.cover_image:
            try:
                if hasattr(obj.cover_image, 'url'):
                    url = obj.cover_image.url
                elif isinstance(obj.cover_image, str):
                    if obj.cover_image.startswith('http'):
                        url = obj.cover_image
                    else:
                        image_path = obj.cover_image
                        if image_path.startswith('covers/'):
                            image_path = image_path[7:]
                        url = f"{settings.MEDIA_URL}covers/{image_path}"
                else:
                    url = str(obj.cover_image)
                cover_html = f'<img src="{url}" width="150" height="210" style="object-fit:cover; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2);" />'
            except Exception as e:
                cover_html = f'<div style="width:150px; height:210px; background:#f0f0f0; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#999;">No Cover</div>'
        else:
            cover_html = '<div style="width:150px; height:210px; background:#f0f0f0; border-radius:8px; display:flex; align-items:center; justify-content:center; color:#999;">No Cover</div>'
        
        # Build the preview HTML as a string
        preview_html = f"""
        <div style="display:flex; gap:20px; padding:15px; background:white; border-radius:8px; border:1px solid #e0e0e0; min-height:230px;">
            <div style="flex-shrink:0;">
                {cover_html}
            </div>
            <div style="flex:1; text-align:left;">
                <h3 style="margin:0 0 5px 0; color:#333; font-size:18px;">{obj.title_statement if obj.title_statement else 'No Title'}</h3>
                <p style="margin:3px 0; color:#555;"><strong>Author:</strong> {obj.main_author if obj.main_author else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Control No:</strong> {obj.control_no if obj.control_no else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Call Number:</strong> {obj.call_number if obj.call_number else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Publisher:</strong> {obj.publisher if obj.publisher else 'N/A'} ({obj.publication_year if obj.publication_year else 'N/A'})</p>
                <p style="margin:3px 0; color:#555;"><strong>ISBN:</strong> {obj.isbn if obj.isbn else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Library:</strong> {obj.library_name if obj.library_name else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Section:</strong> {obj.section if obj.section else 'N/A'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Availability:</strong> {'✅ Available' if obj.availability else '❌ Unavailable'}</p>
                <p style="margin:3px 0; color:#555;"><strong>Course:</strong> {obj.course if obj.course else 'N/A'}</p>
                {f'<p style="margin:3px 0; color:#555;"><strong>Summary:</strong> {obj.summary[:200]}{"..." if obj.summary and len(obj.summary) > 200 else ""}</p>' if obj.summary else ''}
            </div>
        </div>
        """
        return mark_safe(preview_html)
    book_preview.short_description = "📚 Book Preview"
    
    # Fieldsets organized by MARC field numbers
    fieldsets = (
        # 000 - Leader, Control & Codes
        ('000 - 099', {
            'fields': (
                'control_no',
                'date_time_stamp',
                'fixed_length_data',
                'leader',
                'control_number_identifier',
                'isbn',
                'issn',
                'price',
                'ddc_number'
            )
        }),
        
        # 100 - Main Entry
        ('100 - Main Entry', {
            'fields': (
                'main_author',
                'main_corporate_name'
            )
        }),
        
        # 200 - Title & Edition
        ('200 - Title & Edition', {
            'fields': (
                'title_statement',
                'title_author',
                'edition'
            )
        }),
        
        # 300 - Publication & Physical Description
        ('300 - Publication & Physical Description', {
            'fields': (
                'publication_place',
                'publisher',
                'publication_year',
                'publication_distribution',
                'pages',
                'illustrations',
                'size',
                'volume'
            )
        }),
        
        # 400 - Content Types
        ('400 - Content Types', {
            'fields': (
                'content_type',
                'content_code',
                'media_type',
                'media_code',
                'carrier_type',
                'carrier_code'
            )
        }),
        
        # 500 - Notes
        ('500 - Notes', {
            'fields': (
                'general_note',
                'bibliography_note',
                'summary'
            )
        }),
        
        # 600 - Subject Access Fields
        ('600 - Subject Access Fields', {
            'fields': (
                'subject_personal_name',
                'subject_corporate_name',
                'uniform_title',
                'chronological_term',
                'subject_topic',
                'topical_term',
                'faceted_topical_terms',
                'geographical_name',
                'subject_form',
                'genre',
                'genre_form'
            ),
            'classes': ('collapse',)
        }),
        
        # 700 - Added Entries
        ('700 - Added Entries', {
            'fields': (
                'personal_name',
                'corporate_name',
                'added_entry_elements'
            )
        }),
        
        # 800 - Series & Local Fields
        ('800 - Series & Local Fields', {
            'fields': (
                'series_title',
                'library_name',
                'section',
                'call_number',
                'accession_no',
                'barcode',
                'rfid'
            )
        }),
        
        # 900 - Cover Image & Preview
        ('900 - Cover Image & Preview', {
            'fields': (
                'cover_image',
                'cover_image_preview',
                'book_preview',
            ),
            'classes': ('wide',)
        }),
        
        # 901 - Availability & Course
        ('901 - Availability & Course', {
            'fields': (
                'availability',
                'year',
                'course',
                'programs'
            )
        }),
        
        # 902 - Source & Acquisition
        ('902 - Source & Acquisition', {
            'fields': (
                'source_vendor',
                'source_date',
                'acquisition_type_id',
                'acquisition_custom'
            ),
            'classes': ('collapse',)
        }),
        
        # 903 - Archival
        ('903 - Archival', {
            'fields': (
                'archived_at',
                'deleted_at'
            ),
            'classes': ('collapse',)
        }),
        
        # 905 - Cataloging Source
        ('905 - Cataloging Source', {
            'fields': (
                'cataloging_source_a',
                'cataloging_source_b',
                'cataloging_source_e'
            )
        }),
        
        # 999 - System Metadata
        ('999 - System Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom actions
    actions = ['mark_as_available', 'mark_as_unavailable']
    
    def mark_as_available(self, request, queryset):
        updated = queryset.update(availability=True)
        self.message_user(request, f'{updated} records marked as available.')
    mark_as_available.short_description = "Mark selected records as available"
    
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(availability=False)
        self.message_user(request, f'{updated} records marked as unavailable.')
    mark_as_unavailable.short_description = "Mark selected records as unavailable"
    
    save_on_top = True
    list_per_page = 25
    date_hierarchy = 'date_time_stamp'
    ordering = ['-date_time_stamp', 'control_no']