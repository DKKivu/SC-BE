from django.urls import path,include
from . import views

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path('boards', views.BoardApiView.as_view()),
    path('todos', views.ToDoApiView.as_view()),
]
