from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.decorators.http import require_POST

from .forms import ReviewForm
from .models import Category, Product, ProductReview
from django.db.models import Count
# Create your views here.

def home(request):
   # products = Product.objects.all()
    #categories = Category.objects.annotate(product_count=Count("products"))

    top_products = Product.objects.filter(
        product_categories__category__slug="top-selling"
    ).distinct()

    new_products = Product.objects.filter(
        product_categories__category__slug="new-arival"
    ).distinct()

    categories = Category.objects.annotate(
        product_count=Count('product_categories__product')
    )
    context = {"top_products": top_products,"new_products": new_products, "categories": categories}

    return render(request, "products/home.html", context)

def all_products(request):
    products = Product.objects.all().prefetch_related('images')
    for product in products:
        product.full_star = int(product.rating)
        frating= product.rating - product.full_star
        if frating >= 0.5:
            product.half_star = 1
        else:
            product.half_star = 0
       
    paginator = Paginator(products, 20)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
    }
    return render(request, "products/products.html", context)


def product_wishlist(request, product_slug):
    pass

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

        
    products = Product.objects.filter(
        product_categories__category=category
    ).prefetch_related('images')
    
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "products": paged_products,
        "category": category,
    }
    return render(request, "products/category_products.html", context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    reviews = product.reviews.filter(is_active=True)

    rating_counts = {
        "5": product.reviews.filter(rating__gt=4.4, rating__lte=5.1).count(),
        "4": product.reviews.filter(rating__gt=3.4, rating__lte=4.1).count(),
        "3": product.reviews.filter(rating__gt=2.4, rating__lte=3.1).count(),
        "2": product.reviews.filter(rating__gt=1.4, rating__lte=2.1).count(),
        "1": product.reviews.filter(rating__gt=0.4, rating__lte=1.1).count(),
    }

    total_reviews = sum(rating_counts.values())

    rating_percentages = {
        "5": (rating_counts["5"] / total_reviews * 100) if total_reviews else 0,
        "4": (rating_counts["4"] / total_reviews * 100) if total_reviews else 0,
        "3": (rating_counts["3"] / total_reviews * 100) if total_reviews else 0,
        "2": (rating_counts["2"] / total_reviews * 100) if total_reviews else 0,
        "1": (rating_counts["1"] / total_reviews * 100) if total_reviews else 0,
    }

    context = {
        "product": product,
        "rating_counts": rating_counts,
        "rating_percentages": rating_percentages,
        "reviews": reviews,
    }
   # return render(request, "products/product_details.html", context)
    return render(request, "products/product-left-thumbnail.html", context)

@require_POST
@login_required
def submit_review(request, product_slug):
    url = request.META.get("HTTP_REFERER")
    try:
        review = ProductReview.objects.get(
            user__id=request.user.id, product__slug=product_slug
        )
        form = ReviewForm(request.POST, instance=review)
        form.save()
        messages.success(request, "Thank you! Your review has been updated.")
        return redirect(url)
    except ProductReview.DoesNotExist:
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = ProductReview()
            data.product = Product.objects.get(slug=product_slug)
            data.user_id = request.user.id
            data.rating = form.cleaned_data["rating"]
            data.review = form.cleaned_data["review"]
            data.save()
            messages.success(request, "Thank you! Your review has been submitted.")
            return redirect(url)
