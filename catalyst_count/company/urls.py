from django.urls import path

from .views import (CompanyFilterView, CompanyListView, FileUploadView,
                    HomeView, LoginView, LogoutView, RegisterView,
                    TaskProgressView, UserListView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('companies-filter/', CompanyFilterView.as_view(), name='companies_filter'),
    path('companies/', CompanyListView.as_view(), name='companies'),
    path('file-upload/', FileUploadView.as_view(), name='file_upload'),
    path('progress/<task_id>/', TaskProgressView.as_view(), name='task_progress'),
]
