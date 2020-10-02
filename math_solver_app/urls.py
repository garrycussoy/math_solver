# Import some packages needed
from django.contrib import admin
from django.urls import path, include
from . import views

# Define app name and url patterns
app_name = 'math_solver_app'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('scanning-problem', views.upload_image, name = 'upload_image'),
    path('solving-problem', views.extract_problem, name = 'extract_problem'),
    path('solution', views.solve, name = 'solve')
]