from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.deletion import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404

from finance_manager.forms import SignUpForm, CategoryForm, TransactionForm
from finance_manager.models import Transaction, Category, EXPENSE_CHOICES


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


@login_required(login_url='/')
def categories_page(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    context = {
        'categories': categories,
    }
    return render(request, 'categories-page.html', context)


@login_required(login_url='/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('categories-page')
        else:
            category = Category()
            category.category_name = request.POST.get('category_name')
            category.category_description = request.POST.get('category_description')
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


def get_user_object_or_404(model_class, request, pk):
    queryset = model_class.objects.filter(user=request.user)
    return get_object_or_404(queryset, pk=pk)


@login_required(login_url='/')
def edit_category(request, pk):
    category = get_user_object_or_404(Category, request, pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('categories-page')
        else:
            category.category_name = request.POST.get('category_name')
            category.category_description = request.POST.get('category_description')
            context = {
                'form': form,
                'category': category,
            }
            return render(request, 'edit-category-page.html', context)
    else:
        context = {
            'category': category,
        }
        return render(request, 'edit-category-page.html', context)


@login_required(login_url='/')
def delete_category(request, pk):
    category = get_user_object_or_404(Category, request, pk)

    try:
        category.delete()
    except ProtectedError:
        error_message = "You cannot delete [" + str(category.category_name) + "] category. " \
                                                                              "Please, first delete all transactions related to this category and then delete category."
        messages.error(request, error_message)
    return redirect('categories-page')


@login_required(login_url='/')
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('home')
        else:
            transaction = Transaction()
            transaction.category = request.POST.get('category_name')
            transaction.type_of_operation = request.POST.get('type_of_operation')
            transaction.amount = request.POST.get('amount')
            transaction.transaction_description = request.POST.get('transaction_description')

            categories = Category.objects.filter(user=request.user)
            context = {
                'form': form,
                'transaction': transaction,
                'categories': categories,
                'expense_choices': EXPENSE_CHOICES,
            }
            return render(request, 'add-transaction-page.html', context)
    else:
        form = TransactionForm()
        categories = Category.objects.filter(user=request.user)
        context = {
            'form': form,
            'categories': categories,
            'expense_choices': EXPENSE_CHOICES,
        }
    return render(request, 'add-transaction-page.html', context)


@login_required(login_url='/')
def edit_transaction(request, pk):
    transaction = get_user_object_or_404(Transaction, request, pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            return redirect('home')
        else:
            transaction.category = request.POST.get('category_name')
            transaction.type_of_operation = request.POST.get('type_of_operation')
            transaction.amount = request.POST.get('amount')
            transaction.transaction_description = request.POST.get('transaction_description')

            categories = Category.objects.filter(user=request.user)
            context = {
                'form': form,
                'transaction': transaction,
                'categories': categories,
                'expense_choices': EXPENSE_CHOICES,
            }
            return render(request, 'edit-transaction-page.html', context)
    else:

        categories = Category.objects.filter(user=request.user)
        context = {
            'transaction': transaction,
            'categories': categories,
            'expense_choices': EXPENSE_CHOICES,
        }
        return render(request, 'edit-transaction-page.html', context)


@login_required(login_url='/')
def delete_transaction(request, pk):
    get_user_object_or_404(Transaction, request, pk).delete()
    if request.get_full_path() == r'^categories/(?P<pk>\d+)/category-details/$':
        return redirect('categories-page')
    else:
        return redirect('home')


@login_required(login_url='/')
def delete_all_transactions(request):
    Transaction.objects.filter(user=request.user).delete()
    return redirect('home')


@login_required(login_url='/')
def delete_all_transaction_of_one_category(request, pk):
    get_user_object_or_404(Category, request, pk)
    Transaction.objects.filter(user=request.user).filter(category=pk).delete()
    return redirect('categories-page')


@login_required(login_url='/')
def category_details(request, pk):
    category = get_user_object_or_404(Category, request, pk)
    transactions = Transaction.objects.filter(user=request.user).filter(category=category.id)
    context = {
        'category': category,
        'transactions': transactions,
    }
    return render(request, 'category-details-page.html', context)


@login_required(login_url='/')
def amount_by_categories(request):
    type_of_operation = request.POST.get('type_of_operation')
    date_from = request.POST.get('from')
    date_to = request.POST.get('to')
    categories_amount = Transaction.objects \
        .filter(user=request.user) \
        .filter(type_of_operation=type_of_operation) \
        .filter(operation_date__range=[date_from, date_to]) \
        .values('category__category_name') \
        .annotate(category_total=Sum('amount'))
    context = {
        'categories_amount': categories_amount,
    }
    return render(request, 'category-total.html', context)


@login_required(login_url='/')
def amount_by_date(request):
    type_of_operation = request.POST.get('type_of_operation')
    date_from = request.POST.get('from')
    date_to = request.POST.get('to')
    transactions = Transaction.objects \
        .filter(user=request.user) \
        .filter(type_of_operation=type_of_operation) \
        .filter(operation_date__range=[date_from, date_to]) \
        .order_by('operation_date')

    context = {
        'transactions': transactions,
    }
    return render(request, 'date-amount.html', context)


@login_required(login_url='/')
def report_generator(request):
    if request.method == 'POST':
        chart = request.POST.get('chart')
        if chart == 'category-pie':
            return amount_by_categories(request)
        else:
            return amount_by_date(request)
    else:
        context = {
            'expense_choices': EXPENSE_CHOICES,
        }
        return render(request, 'report-generator.html', context)
