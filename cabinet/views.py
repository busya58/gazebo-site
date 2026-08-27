from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ReviewForm
from django.shortcuts import render

from cabinet.models import Review


def home(request):
    reviews = Review.objects.filter(
        is_published=True,
    ).select_related("user")

    return render(
        request,
        "home.html",
        {
            "reviews": reviews,
        },
    )

@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.is_published = False
            review.save()

            messages.success(
                request,
                "Спасибо! Отзыв отправлен на проверку.",
            )

            return redirect("cabinet:dashboard")
    else:
        form = ReviewForm()

    return render(
        request,
        "cabinet/review_form.html",
        {
            "form": form,
        },
    )

from .forms import (
    ApplicationForm,
    ClientLoginForm,
    RegistrationForm,
)
from .models import Application


def register_view(request):
    if request.user.is_authenticated:
        return redirect("cabinet:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Регистрация завершена. Добро пожаловать!",
            )

            return redirect("cabinet:dashboard")
    else:
        form = RegistrationForm()

    return render(
        request,
        "cabinet/register.html",
        {"form": form},
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("cabinet:dashboard")

    if request.method == "POST":
        form = ClientLoginForm(
            request=request,
            data=request.POST,
        )

        if form.is_valid():
            login(request, form.get_user())

            next_url = request.POST.get("next")

            if next_url and next_url.startswith("/"):
                return redirect(next_url)

            return redirect("cabinet:dashboard")
    else:
        form = ClientLoginForm(request=request)

    return render(
        request,
        "cabinet/login.html",
        {
            "form": form,
            "next": request.GET.get("next", ""),
        },
    )


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Вы вышли из личного кабинета.")

    return redirect("cabinet:login")


@login_required
def dashboard_view(request):
    applications = Application.objects.filter(
        user=request.user
    )

    return render(
        request,
        "cabinet/dashboard.html",
        {"applications": applications},
    )


@login_required
def application_create_view(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            messages.success(
                request,
                "Заявка успешно отправлена.",
            )

            return redirect(application)
    else:
        form = ApplicationForm(
            initial={
                "name": request.user.first_name,
            }
        )

    return render(
        request,
        "cabinet/application_form.html",
        {"form": form},
    )


@login_required
def application_detail_view(request, pk):
    application = get_object_or_404(
        Application,
        pk=pk,
        user=request.user,
    )

    return render(
        request,
        "cabinet/application_detail.html",
        {"application": application},
    )