# Import some packages needed
from django.contrib import admin
from django.urls import path, include
from . import views

# Define app name and url patterns
app_name = 'math_solver_app'
urlpatterns = [
    path('', views.index, name = 'index'),
    # path('barang/<int:barang_id>', views.detail_barang, name='detail')
]