from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('flaws/', include('flaws.urls'))
]