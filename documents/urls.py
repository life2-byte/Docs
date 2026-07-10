from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('document/new/', views.create_document, name='create_document'),
    path('document/<int:doc_id>/', views.edit_document, name='edit_document'),
    path('document/<int:doc_id>/share/', views.share_document, name='share_document'),
    path('upload/', views.upload_file, name='upload_file'),
    path('signup/', views.signup_view, name='signup'),
]