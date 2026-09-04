from django.shortcuts import render

# Create your views here.
def module_view_page(self, request, module_id):
    """Custom view page for module with Jazzmin template"""
    from .models import Module
    module = Module.objects.get(id=module_id)
    
    # Get module details
    context = {
        'module': module,
        'syllabus': module.syllabus,
        'subject': module.syllabus.subject,
        'title': f"Module {module.module_number}: {module.module_title}",
        'opts': self.model._meta,
        'has_permission': self.has_view_permission(request, module),
        'site_header': self.admin_site.site_header,
        'site_title': self.admin_site.site_title,
        'index_title': self.admin_site.index_title,
    }
    
    # If using Jazzmin, use its base template
    return render(request, 'admin/module_view.html', context)