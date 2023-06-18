"""Personal Loan backend URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger documentation
    path('api/openapi/', get_schema_view(
        title="Personal Loan Proposal Management API",
        description="Personal Loan Proposal API requests and descriptions",
        version="1.0.0",
        public=True,
        permission_classes=[],
    ), name='openapi-schema'),

    path('api/docs/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
