from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('adminControl-Panel/', views.custom_admin, name='admin_custom'),  # URL tùy chỉnh cho adminControl.html
    path('dashboard_user/', views.dashboard_user, name='dashboard_user'),
    path('dashboard_content_manager/', views.dashboard_content_manager, name='dashboard_content_manager'),
    path('edit_role/<int:id>/', views.edit_role, name='edit_role'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('add_user_route/', views.add_user_route, name='add_user_route'),
]
