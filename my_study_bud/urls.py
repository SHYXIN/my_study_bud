from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # 视图的分发
    path('', include('base.urls')),
    # api
    path('api/', include('base.api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

# 可以进入static去参考
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)