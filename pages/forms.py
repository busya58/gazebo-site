from django import forms

from core.models import Application


class ApplicationForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label="Я согласен на обработку персональных данных",
    )

    class Meta:
        model = Application
        fields = (
            "name",
            "phone",
            "email",
            "project_type",
            "selected_model",
            "dimensions",
            "material",
            "roof_type",
            "options",
            "address",
            "comment",
            "attachment",
            "consent",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 999 000-00-00", "type": "tel"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "example@mail.ru"}
            ),
            "selected_model": forms.TextInput(
                attrs={"placeholder": "Название модели"}
            ),
            "dimensions": forms.TextInput(
                attrs={"placeholder": "Например: 3 × 4 м"}
            ),
            "material": forms.TextInput(
                attrs={"placeholder": "Дерево, металл и другое"}
            ),
            "roof_type": forms.TextInput(
                attrs={"placeholder": "Двускатная, односкатная и другая"}
            ),
            "options": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Дополнительные опции"}
            ),
            "address": forms.TextInput(
                attrs={"placeholder": "Адрес доставки и установки"}
            ),
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Комментарий"}
            ),
        }