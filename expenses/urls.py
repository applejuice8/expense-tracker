from django.urls import path, include
from .views import ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView

from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register('expenses', api_views.ExpenseViewSet, basename='expenses')

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('create/', ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='delete'),

    # API
    path('api/', include(router.urls)),
]