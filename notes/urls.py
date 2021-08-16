from django.conf.urls import url
from django.urls.conf import re_path
from . import views
from django.urls import path

urlpatterns = [
    # Accounts & Auth
    path('accounts/login', views.login_view, name='login'),
    path('accounts/logout', views.logout_view, name='logout'),
    path('accounts/register', views.register, name='register'),

    # API Views
    path('api/', views.api_overview),
    path('api/notes', views.list_notes),
    path('api/note/<int:id>', views.note),
    path('api/create-note', views.create_note),

    # This path catches all urls, essentially letting react-router handle urls
    url(r'^(?:.*)/?$', views.index),
]
