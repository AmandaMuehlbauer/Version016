# blog/urls.py

"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve





urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('apps.core.urls', 'core'), namespace='core')),    
    path('users/', include(('apps.users.urls', 'users'), namespace='users')),  
    path('', include(('apps.ContactUs.urls', 'ContactUs'), namespace='ContactUs')),
    path('', include(('apps.URLsub.urls', 'URLsub'), namespace='URLsub')),  
    path('', include(('apps.Search.urls', 'Search'), namespace='Search')),
    path('', include(('SubjectTags.urls', 'SubjectTags'), namespace='SubjectTags')),
    path('', include(('StripePayment.urls', 'StripePayment'), namespace='StripePayment')),
    path('legal/', include('apps.legal.urls')),  # Include legal app URLs


]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]

