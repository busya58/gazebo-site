from django.conf import settings


def site_data(request):
    return {
        "site_name": getattr(settings, "SITE_NAME", "Беседки и Вольеры РФ"),
        "site_slogan": getattr(
            settings,
            "SITE_SLOGAN",
            "Беседки, вольеры и навесы по всей России",
        ),
        "site_phone": getattr(settings, "SITE_PHONE", "+7 (925) 055-98-88"),
        "site_phone_href": getattr(
            settings,
            "SITE_PHONE_HREF",
            "tel:+79250559888",
        ),
        "site_email": getattr(
            settings,
            "SITE_EMAIL",
            "hh8754905@gmail.com",
        ),
        "site_address": getattr(
            settings,
            "SITE_ADDRESS",
            "г. Москва и Московская область",
        ),
        "site_geography": getattr(
            settings,
            "SITE_GEOGRAPHY",
            "Вся Россия",
        ),
        "site_url": getattr(
            settings,
            "SITE_URL",
            "http://127.0.0.1:8000",
        ),
        "site_description": getattr(
            settings,
            "SITE_DESCRIPTION",
            (
                "Изготовление и установка беседок, вольеров, навесов "
                "и других конструкций на заказ по всей России."
            ),
        ),
    }