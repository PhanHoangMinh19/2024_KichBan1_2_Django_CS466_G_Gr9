from django.urls import path, include

urlpatterns = [
    path('', include('library.urls')),  # Bao gồm các URL từ ứng dụng library
]
