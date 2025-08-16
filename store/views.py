
from django.shortcuts import render, get_object_or_404
from carts.models import CartItem
from category.models import Category
from .models import Product, Variation
from carts.views import _cart_id 
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None 

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products,1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
        paginator = Paginator(products,2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products':  paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


from django.shortcuts import get_object_or_404

def product_detail(request, category_slug, product_slug):
    single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    colors = Variation.objects.colors().filter(product=single_product)
    sizes = Variation.objects.sizes().filter(product=single_product)
    return render(request, 'store/product_detail.html', {
        'single_product': single_product,
        'colors': colors,
        'sizes': sizes
    })

    
    context = {
        'single_product': single_product,
        'in_cart':in_cart,
        
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
 if 'keyword' in request.GET:
    keyword = request.GET['keyword']
    if keyword:
     products = Product.objects.order_by('-modified_date').filter(
    Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
     
     product_count = products.count()
    context ={
            'products':products,
            'product_count':product_count,
        }

    return render(request, 'store/store.html',context)