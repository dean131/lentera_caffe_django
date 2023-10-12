from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include('base.urls')),
    path('api/', include('base.api.urls')),
    path('api/account/', include('account.api.urls')),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = 'Admin'
admin.site.site_title = 'Lentera Caffe'
admin.site.site_header = 'Lentera Caffe Admin'
