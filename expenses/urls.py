from django.urls import path
from .views import ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView

app_name = 'expenses'

urlpatterns = [
    path('', ExpenseListView.as_view(), name='list'),
    path('create/', ExpenseCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ExpenseUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ExpenseDeleteView.as_view(), name='delete'),
]