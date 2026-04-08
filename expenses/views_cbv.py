from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Expense
from .forms import ExpenseForm


class ExpenseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ExpenseForm()
        return render(request, 'expenses/create.html', {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expenses:list')

        return render(request, 'expenses/form.html', {'form': form})


class ExpenseListView(LoginRequiredMixin, View):
    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        return render(request, 'expenses/list.html', {'expenses': expenses})


class ExpenseUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        expense = get_object_or_404(
            Expense,
            pk=pk,
            user=request.user
        )

        form = ExpenseForm(instance=expense)
        return render(request, 'expenses/update.html', {'form': form})

    def post(self, request, pk):
        expense = get_object_or_404(
            Expense,
            pk=pk,
            user=request.user
        )

        form = ExpenseForm(request.POST, instance=expense)

        if form.is_valid():
            form.save()
            return redirect('expenses:list')

        return render(request, 'expenses/update.html', {'form': form})


class ExpenseDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        expense = get_object_or_404(
            Expense,
            pk=pk,
            user=request.user
        )

        return render(request, 'expenses/delete.html', {'expense': expense})

    def post(self, request, pk):
        expense = get_object_or_404(
            Expense,
            pk=pk,
            user=request.user
        )

        expense.delete()
        return redirect('expenses:list')