from django.urls import path, include
from django.contrib import admin

import core.urls
import user.urls
import requirements.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include(user.urls,namespace='user')),
    path('requirements/',include(requirements.urls,namespace='requirements')),
    path('', include(core.urls, namespace='core')),
]

