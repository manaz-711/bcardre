from django.urls import path,re_path,include
from django.conf import settings
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index,name='index'),
    path('media/passdata', views.data, name='passdata'),
    path('image/save',views.save,name='save'),
    path('bcarddetails', views.bcarddetails, name='bcarddetails'),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    path('image_upload', views.imageupload, name = 'image_upload'),
    path('api_upload/',views.apiupload,name='api_upload')
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)