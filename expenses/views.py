from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense
from .forms import ExpenseForm


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/create.html'
    success_url = reverse_lazy('expenses:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/update.html'
    success_url = reverse_lazy('expenses:list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/delete.html'
    success_url = reverse_lazy('expenses:list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
