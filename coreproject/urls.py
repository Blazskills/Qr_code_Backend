from qrcodeapp import views
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions
from rest_framework import authentication


from drf_yasg.generators import OpenAPISchemaGenerator
from django.conf import settings
from django.conf.urls.static import static

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "account",
                "description": "everything about your Account"
            },
            {
                "name": "qrcodeapp",
                "description": "everything about your Qrcode app"
            },
        ]

        return swagger
    
schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Blesify Api',
        default_version='1.0.0',
        description="API Documentation of Blesify Application",
        contact=openapi.Contact(email="info@toismart.com"),
    ),

    public=True,
    authentication_classes=[authentication.SessionAuthentication],
    permission_classes=[permissions.IsAuthenticated],
    generator_class=CustomOpenAPISchemaGenerator,

)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.TestApi.as_view(), name="index"),
    
    
    path('api/v1/',

         include([
             path('account/', include('account.urls')),
             path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
             path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

         ])

         ),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)