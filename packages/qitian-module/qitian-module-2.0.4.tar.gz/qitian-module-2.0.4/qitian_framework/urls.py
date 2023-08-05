"""django_module URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.views.i18n import JavaScriptCatalog
import notifications.urls

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^chaining/', include('smart_selects.urls')),
    re_path(r'^simditor/', include('simditor.urls')),
    path('autopost/', include('autopost.urls')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # path('comment/', include('qt_comment.urls'), name='comment'),
    # path('uc/', include('usercenter.urls'), name='uc'),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# 生产环境使用nginx路由
if settings.ENV_CONFIG == 'dev':
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
