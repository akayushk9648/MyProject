
from django.contrib import admin
from django.urls import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('',include('user.urls'))

]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
