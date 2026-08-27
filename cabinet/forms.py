from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Application
from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "text"]

        labels = {
            "rating": "Ваша оценка",
            "text": "Ваш отзыв",
        }

        widgets = {
            "rating": forms.Select(
                attrs={
                    "class": "cabinet-input",
                }
            ),
            "text": forms.Textarea(
                attrs={
                    "class": "cabinet-input",
                    "rows": 7,
                    "placeholder": "Расскажите о качестве работы и результате...",
                }
            ),
        }

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите имя",
            }
        ),
    )

    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@mail.ru",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "email",
            "username",
            "password1",
            "password2",
        )

        labels = {
            "username": "Логин",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Придумайте логин",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Придумайте пароль",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Повторите пароль",
            }
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "Пользователь с такой почтой уже зарегистрирован."
            )

        return email


class ClientLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите логин",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите пароль",
            }
        ),
    )


class ApplicationForm(forms.ModelForm):
    agreement = forms.BooleanField(
        label="Я согласен на обработку персональных данных",
        required=True,
    )

    class Meta:
        model = Application
        fields = (
            "project_type",
            "name",
            "phone",
            "description",
        )

        labels = {
            "project_type": "Выберите проект",
            "name": "Ваше имя",
            "phone": "Телефон",
            "description": "Описание и пожелания",
        }

        widgets = {
            "project_type": forms.Select(
                attrs={"class": "form-control"}
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите имя",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+7 (___) ___-__-__",
                    "type": "tel",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": (
                        "Укажите размеры, материалы и другие пожелания"
                    ),
                    "rows": 5,
                }
            ),
        }