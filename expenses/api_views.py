from rest_framework import viewsets, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # User only sees own expenses
    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )

	# Automatically attach logged-in user on create
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)