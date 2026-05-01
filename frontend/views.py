from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from apps.integrations.models import AggregatedContent
from apps.users.models import User
import json


def home_view(request):
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    content_qs = AggregatedContent.objects.all()

    # filter by source if provided
    source = request.GET.get('source')
    if source:
        content_qs = content_qs.filter(source=source)

    # search functionality
    search = request.GET.get('search')
    if search:
        content_qs = content_qs.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    content_qs = content_qs.order_by('-published_date')

    # pagination - 12 items per page for nice grid layout
    paginator = Paginator(content_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # chart data for visualization
    chart_data = AggregatedContent.objects.values('source').annotate(count=Count('id'))
    chart_labels = [item['source'].upper() for item in chart_data]
    chart_counts = [item['count'] for item in chart_data]

    context = {
        'content_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_counts),
    }
    return render(request, 'dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'register.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
