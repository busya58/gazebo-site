from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from cabinet.models import Review
from core.models import Product, Project

from .forms import ApplicationForm


CATALOG_TYPE_GROUPS = {
    "gazebo": [
        {
            "title": "По конструкции",
            "items": [
                "Открытые",
                "Полуоткрытые",
                "Закрытые",
                "Беседки-перголы",
                "С хозяйственным блоком",
            ],
        },
        {
            "title": "По сезону и форме",
            "items": [
                "Летние",
                "Всесезонные утеплённые",
                "Прямоугольные",
                "Квадратные",
                "Круглые",
                "Шестигранные и восьмигранные",
            ],
        },
        {
            "title": "Материал и оснащение",
            "items": [
                "С мангалом или барбекю",
                "Деревянные",
                "Металлические",
                "Кирпичные",
                "Комбинированные",
                "Разные типы крыш",
            ],
        },
    ],
    "enclosure": [
        {
            "title": "По конструкции",
            "items": [
                "Открытые",
                "Полуоткрытые",
                "Закрытые",
                "Утеплённые зимние",
                "Разборные",
                "Стационарные",
                "Модульные",
            ],
        },
        {
            "title": "По комплектации",
            "items": [
                "С одной или несколькими секциями",
                "С будкой",
                "С зимником",
                "С выгульной зоной",
                "С хозяйственным отделением",
            ],
        },
        {
            "title": "Материал и назначение",
            "items": [
                "Деревянные",
                "Металлические",
                "Комбинированные",
                "Для одной или нескольких собак",
                "Для птиц и животных",
            ],
        },
    ],
}


def home(request):
    popular_products = (
        Product.objects.filter(
            is_available=True,
            is_popular=True,
        )
        .prefetch_related("images")[:6]
    )

    projects = Project.objects.filter(
        is_published=True,
    )[:6]

    reviews = (
        Review.objects.filter(is_published=True)
        .select_related("user")
        .order_by("-created_at")[:6]
    )

    context = {
        "popular_products": popular_products,
        "projects": projects,
        "reviews": reviews,
        "application_form": ApplicationForm(),
    }

    return render(request, "pages/index.html", context)


def catalog(request, kind):
    if kind not in {"gazebo", "enclosure"}:
        return redirect("home")

    products = (
        Product.objects.filter(
            kind=kind,
            is_available=True,
        )
        .select_related("category")
        .prefetch_related("images")
    )

    search = request.GET.get("q", "").strip()
    product_type = request.GET.get("type", "").strip()
    shape = request.GET.get("shape", "").strip()
    material = request.GET.get("material", "").strip()
    roof = request.GET.get("roof", "").strip()
    season = request.GET.get("season", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if search:
        products = products.filter(
            Q(title__icontains=search)
            | Q(short_description__icontains=search)
            | Q(product_type__icontains=search)
            | Q(frame_material__icontains=search)
        )

    if product_type:
        products = products.filter(
            product_type__icontains=product_type,
        )

    if shape:
        products = products.filter(
            shape__icontains=shape,
        )

    if material:
        products = products.filter(
            Q(frame_material__icontains=material)
            | Q(wall_material__icontains=material)
            | Q(floor_material__icontains=material)
        )

    if roof:
        products = products.filter(
            roof_type__icontains=roof,
        )

    if season:
        products = products.filter(
            season=season,
        )

    if min_price:
        try:
            products = products.filter(
                price__gte=float(min_price),
            )
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(
                price__lte=float(max_price),
            )
        except ValueError:
            pass

    if request.GET.get("grill") == "1":
        products = products.filter(
            has_grill=True,
        )

    if request.GET.get("glazing") == "1":
        products = products.filter(
            has_glazing=True,
        )

    if request.GET.get("booth") == "1":
        products = products.filter(
            has_booth=True,
        )

    if request.GET.get("winter_room") == "1":
        products = products.filter(
            has_winter_room=True,
        )

    sorting = request.GET.get("sort", "popular")

    sorting_options = {
        "popular": ("-is_popular", "-views_count"),
        "price_asc": ("price",),
        "price_desc": ("-price",),
        "new": ("-created_at",),
    }

    products = products.order_by(
        *sorting_options.get(
            sorting,
            sorting_options["popular"],
        )
    )

    context = {
        "products": products,
        "kind": kind,
        "page_title": (
            "Беседки"
            if kind == "gazebo"
            else "Вольеры"
        ),
        "catalog_type_groups": CATALOG_TYPE_GROUPS.get(kind, []),
    }

    return render(
        request,
        "pages/catalog.html",
        context,
    )


def winter_enclosures(request):
    products = (
        Product.objects.filter(
            kind="enclosure",
            is_available=True,
        )
        .filter(
            Q(season="winter")
            | Q(has_winter_room=True)
            | (
                Q(insulation_type__isnull=False)
                & ~Q(insulation_type="")
            )
        )
        .select_related("category")
        .prefetch_related("images")
        .distinct()
    )

    context = {
        "products": products,
        "kind": "enclosure",
        "page_title": "Зимние вольеры",
        "winter_page": True,
        "catalog_type_groups": CATALOG_TYPE_GROUPS.get(
            "enclosure",
            [],
        ),
    }

    return render(
        request,
        "pages/catalog.html",
        context,
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related("images"),
        slug=slug,
        is_available=True,
    )

    Product.objects.filter(
        pk=product.pk,
    ).update(
        views_count=product.views_count + 1,
    )

    related_products = (
        Product.objects.filter(
            kind=product.kind,
            is_available=True,
        )
        .exclude(pk=product.pk)
        .prefetch_related("images")[:4]
    )

    return render(
        request,
        "pages/product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )


def projects(request):
    project_list = Project.objects.filter(
        is_published=True,
    )

    selected_type = request.GET.get("type")

    if selected_type:
        project_list = project_list.filter(
            project_type=selected_type,
        )

    return render(
        request,
        "pages/projects.html",
        {
            "projects": project_list,
        },
    )


@require_http_methods(["POST"])
def application_create(request):
    form = ApplicationForm(
        request.POST,
        request.FILES,
    )

    if form.is_valid():
        form.save()

        messages.success(
            request,
            "Заявка отправлена. Менеджер свяжется с вами.",
        )

        return redirect("thanks")

    popular_products = (
        Product.objects.filter(
            is_available=True,
            is_popular=True,
        )
        .prefetch_related("images")[:6]
    )

    projects_list = Project.objects.filter(
        is_published=True,
    )[:6]

    reviews = (
        Review.objects.filter(is_published=True)
        .select_related("user")
        .order_by("-created_at")[:6]
    )

    return render(
        request,
        "pages/index.html",
        {
            "popular_products": popular_products,
            "projects": projects_list,
            "reviews": reviews,
            "application_form": form,
        },
        status=400,
    )


def thanks(request):
    return render(
        request,
        "pages/thanks.html",
    )