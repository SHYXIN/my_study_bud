from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # api
    path('api/', include('base.api.urls')),
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    # 视图的分发
    path('', include('base.urls')),

)


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
# 可以进入static去参考
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)