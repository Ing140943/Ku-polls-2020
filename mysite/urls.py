"""
Setting url to access the specific web page.

We can specific the url that we want to lead to the page that we want.

"""


from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
