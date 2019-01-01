from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from finance_manager.forms import SignUpForm, CategoryForm
from finance_manager.models import Transaction, Category


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.changed_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})


@login_required(login_url='login/')
def home(request):
    user = request.user

    categories = Category.objects.filter(user=user)
    category_name = request.GET.get('category')
    category_id = 0
    for category in categories:
        if category.category_name == category_name:
            category_id = category.id

    if category_id == 0:
        transactions = Transaction.objects.filter(user=user).select_related('category').order_by('operation_date')
    else:
        transactions = Transaction.objects.filter(user=user).filter(category=category_id).select_related(
            'category').order_by('operation_date')

    context = {
        'transactions': transactions,
        'categories': categories,
        'category_id': category_id,
    }

    return render(request, 'home-page.html', context)


@login_required(login_url='login/')
def categories_page(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    context = {
        'categories': categories,
    }
    return render(request, 'categories-page.html', context)


@login_required(login_url='login/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories-page', pk=category.pk)
        else:
            category = Category()
            category.category_name = request.POST['category_name']
            category.category_description = request.POST['category_description']
            context = {
                'form': form,
                'category': category,
            }
            return render(request, 'add-category-page.html', context)
    else:
        form = CategoryForm()
        context = {
            'form': form,
        }
        return render(request, 'add-category-page.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POSt':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories-page', pk=category.pk)
        else:
            category = Category()
            category.category_name = request.POST['category_name']
            category.category_description = request.POST['category_description']
            context = {
                'form': form,
                'category': category,
            }
            return render(request, 'edit-category-page.html', context)
