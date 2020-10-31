"""
Setting url to access the specific web page.

We can specific the url that we want to lead to the page that we want.

"""


from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name="main_index_page"),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
