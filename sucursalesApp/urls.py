from django.urls import path
from .views import SucursalesListView, SucursalCreateView, SucursalUpdateView, SucursalDeleteView

urlpatterns = [
    path('api/sucursales/', SucursalesListView.as_view(), name='api_sucursales'),
    path('sucursales/add/', SucursalCreateView.as_view(), name='sucursales_add'),
    path('sucursales/edit/<int:pk>/', SucursalUpdateView.as_view(), name='sucursales_edit'),
    path('sucursales/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursales_delete'),
]