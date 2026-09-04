from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Subject, Syllabus, Module


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'subject_code',
        'subject_name',
        'units',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active',)
    search_fields = ('subject_code', 'subject_name', 'subject_description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'subject_code',
                'subject_name',
                'subject_description'
            )
        }),
        ('Academic Information', {
            'fields': (
                'units',
                'is_active'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    save_on_top = True
    ordering = ['subject_code']


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = (
        'module_number',
        'module_title',
        'module_type',
        'week_number',
        'is_published',
        'is_completed'
    )
    ordering = ['module_number']


@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'instructor_name',
        'school_year',
        'semester',
        'is_published',
        'created_at'
    )
    list_filter = ('is_published', 'school_year', 'semester')
    search_fields = (
        'subject__subject_code',
        'subject__subject_name',
        'instructor_name',
        'course_description'
    )
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ModuleInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'subject',
                'school_year',
                'semester',
                'is_published'
            )
        }),
        ('Course Information', {
            'fields': (
                'course_description',
                'course_objectives',
                'course_outcomes'
            )
        }),
        ('Grading & Policies', {
            'fields': (
                'grading_system',
                'grading_policy',
                'attendance_policy',
                'classroom_policies'
            )
        }),
        ('Textbooks & Resources', {
            'fields': (
                'required_textbooks',
                'recommended_readings'
            )
        }),
        ('Instructor Information', {
            'fields': (
                'instructor_name',
                'instructor_email',
                'instructor_contact',
                'consultation_hours'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    save_on_top = True
    ordering = ['subject__subject_code']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = (
        'week_number',
        'syllabus',
        'module_title',
        'module_type',
        'is_published',
        'is_completed',
        'view_module_button'
    )
    list_filter = (
        'module_type',
        'is_published',
        'is_completed',
        'week_number'
    )
    search_fields = (
        'module_title',
        'topics',
        'learning_objectives',
        'lessons',
        'syllabus__subject__subject_code',
        'syllabus__subject__subject_name'
    )
    list_editable = ('is_published', 'is_completed')
    readonly_fields = ('created_at', 'updated_at')
    
    def view_module_button(self, obj):
        """Add a button to view module in the same page"""
        url = reverse('admin:module_view', args=[obj.id])
        return format_html(
            '<a href="{}" class="button" style="background: #17a2b8; color: white; padding: 5px 12px; border-radius: 4px; text-decoration: none; font-weight: 600;">'
            '📖 View Content'
            '</a>',
            url
        )
    view_module_button.short_description = "View"    

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'syllabus',
                'module_number',
                'module_title',
                'module_type',
                'order'
            )
        }),
        ('Schedule', {
            'fields': (
                'week_number',
                'week_title',
                'duration',
                'start_date',
                'end_date'
            )
        }),
        ('Content', {
            'fields': (
                'topics',
                'learning_objectives',
                'learning_outcomes'
            )
        }),
        ('Lessons & Discussions', {
            'fields': (
                'lessons',
            ),
            'classes': ('wide',)
        }),
        ('Activities & Assessments', {
            'fields': (
                'activities',
                'assignments',
                'assessments'
            )
        }),
        ('Resources', {
            'fields': (
                'resources',
                'references'
            )
        }),
        ('Status', {
            'fields': (
                'is_published',
                'is_completed'
            )
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publish_modules', 'unpublish_modules', 'mark_as_completed']
    
    def publish_modules(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} modules published.')
    publish_modules.short_description = "Publish selected modules"
    
    def unpublish_modules(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} modules unpublished.')
    unpublish_modules.short_description = "Unpublish selected modules"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(is_completed=True)
        self.message_user(request, f'{updated} modules marked as completed.')
    mark_as_completed.short_description = "Mark as completed"
    
    def get_urls(self):
        """Add custom URLs for module views"""
        urls = super().get_urls()
        custom_urls = [
            path('<int:module_id>/view/', self.admin_site.admin_view(self.module_view_page), name='module_view'),
            path('<int:module_id>/print/', self.admin_site.admin_view(self.module_print_page), name='module_print'),
        ]
        return custom_urls + urls
    
    def module_view_page(self, request, module_id):
        """Custom view page for module"""
        module = get_object_or_404(Module, id=module_id)
        
        context = {
            'module': module,
            'syllabus': module.syllabus,
            'subject': module.syllabus.subject,
            'title': f"Module {module.module_number}: {module.module_title}",
            'opts': self.model._meta,
            'has_permission': self.has_view_permission(request, module),
            'app_label': self.model._meta.app_label,
            'model_name': self.model._meta.model_name,
        }
        
        return render(request, 'admin/module_view.html', context)
    
    def module_print_page(self, request, module_id):
        """Custom print page for module"""
        module = get_object_or_404(Module, id=module_id)
        
        context = {
            'module': module,
            'syllabus': module.syllabus,
            'subject': module.syllabus.subject,
            'title': f"Module {module.module_number}: {module.module_title}",
        }
        
        return render(request, 'admin/module_print.html', context)
    
    save_on_top = True
    ordering = ['syllabus', 'module_number']