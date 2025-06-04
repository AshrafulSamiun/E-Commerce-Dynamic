from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch

from .forms import ReviewForm
from .models import Category, Product, ProductReview, ProductCategory,ColorSize
from django.db.models import Count
from collections import defaultdict
# Create your views here.

def home(request):
   # products = Product.objects.all()
    #categories = Category.objects.annotate(product_count=Count("products"))

    top_products = Product.objects.filter(
        product_categories__category__slug="top-selling"
    ).distinct()

    new_products = Product.objects.filter(
        product_categories__category__slug="new-arrival"
    ).distinct()

    categories = Category.objects.annotate(
        product_count=Count('product_categories__product')
    )
    context = {"top_products": top_products,"new_products": new_products, "categories": categories}

    return render(request, "products/home.html", context)

def all_products(request):

        
    product_category_qs = ProductCategory.objects.select_related('category')
    color_qs = ColorSize.objects.select_related('color').all()

    products = Product.objects.all().prefetch_related(
        'images',
        Prefetch('product_categories', queryset=product_category_qs, to_attr='category_links')
    )

    # Initialize count storage
    category_counts = {}
    rating_counts   = {}
    color_counts    = {}
    discount_counts ={}
    price_range_counts = {
        "$0 - $500": 0,
        "$500 - $1000": 0,
        "$1000 - $2000": 0,
        "$2000 - $3000": 0,
        "$3000+": 0
    }



    # counting color wise products
    for color_size in color_qs:
        color = color_size.color
        if color:
            color_counts[color.name] = color_counts.get(color.name, 0) + 1

    
    # Process each product

    for product in products:
        slugs  = [pc.category.slug for pc in product.category_links]
        names = [pc.category.name for pc in product.category_links]
        product.is_best_selling = "top-selling" in slugs
        product.is_new_arrival = "new-arrival" in slugs


        # calculating actural price
        if product.discount_percentage>0:
            product.actual_price = product.price - (product.price * (product.discount_percentage / 100))

            if product.discount_percentage<=10:
                discount_counts["5%-10%"] = discount_counts.get("5%-10%", 0) + 1
            elif product.discount_percentage<=20:   
                discount_counts["10%-20%"] = discount_counts.get("10%-20%", 0) + 1
            else:
                discount_counts["20%+"] = discount_counts.get("20%+", 0) + 1    

        else:
            product.actual_price = product.price

        #counting rating wise products
        
        if product.rating is not None:
            if product.rating <.5:
                rating_counts[0] = rating_counts.get(0, 0) + 1
            elif product.rating < 1.5:
                rating_counts[1] = rating_counts.get(1, 0) + 1
            elif product.rating < 2.5:
                rating_counts[2] = rating_counts.get(2, 0) + 1
            elif product.rating < 3.5:
                rating_counts[3] = rating_counts.get(3, 0) + 1
            elif product.rating < 4.5:
                rating_counts[4] = rating_counts.get(4, 0) + 1
            else:
                rating_counts[5] = rating_counts.get(5, 0) + 1
        
        rating_counts = dict(sorted(rating_counts.items(), reverse=True))


        #product rating processing
        product.full_star = int(product.rating)
        frating= product.rating - product.full_star
        if frating >= 0.5:
            product.half_star = 1
        else:
            product.half_star = 0

        #counting categoriy wise products
        
        for name in names:
            if name in category_counts:
                category_counts[name] += 1
            else:
                category_counts[name] = 1
            category_counts["All Products"] = category_counts.get("All Products", 0) + 1

        # Price range count
        if product.price is not None:
            if product.price <= 500:
                price_range_counts["$0 - $500"] += 1
            elif product.price <= 1000:
                price_range_counts["$500 - $1000"] += 1
            elif product.price <= 2000:
                price_range_counts["$1000 - $2000"] += 1
            elif product.price <= 3000:
                price_range_counts["$2000 - $3000"] += 1
            else:
                price_range_counts["$3000+"] += 1
       
    paginator = Paginator(products, 20)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)

    context = {
        "discount_counts": discount_counts,
        "color_counts": color_counts,
        "products": paged_products,
        "category_counts": category_counts,
        "rating_counts": rating_counts,
        "price_range_counts": price_range_counts,
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
