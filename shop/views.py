from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from cart.forms import CartAddProductForm
from .models import Category, Product

# Vista para listar productos
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()  # Obtener todas las categorías
    products = Product.objects.filter(available=True)  # Filtrar productos disponibles
    cart_product_form = CartAddProductForm()  # Crear formulario para agregar productos al carrito
    search_query = request.GET.get('q', '')  # Obtener el término de búsqueda desde la barra de búsqueda

    if category_slug:
        # Obtener la categoría específica si se proporciona el slug
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # Filtrar productos por categoría

    # Si hay un término de búsqueda, filtrar productos por nombre o descripción
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Determinar si se debe mostrar el mensaje de no productos
    no_products = not products and search_query

    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
            'cart_product_form': cart_product_form,  # Pasar formulario al contexto
            'search_query': search_query,  # Pasar el término de búsqueda al contexto
            'no_products': no_products,  # Pasar el estado de no productos al contexto
        },
    )

# Vista para mostrar los detalles de un producto
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)  # Obtener el producto específico
    cart_product_form = CartAddProductForm()  # Crear formulario para agregar el producto al carrito

    return render(
        request,
        'shop/product/detail.html',
        {'product': product, 'cart_product_form': cart_product_form},  # Pasar producto y formulario al contexto
    )

# Vista para buscar productos
def search_products(request):
    query = request.GET.get('q', '')  # Obtener la consulta de búsqueda del usuario
    results = Product.objects.filter(name__icontains=query, available=True)  # Filtrar productos disponibles por nombre
    return render(request, 'shop/search_results.html', {'products': results, 'query': query})

# Vistas para información adicional
def ayuda(request):
    return render(request, 'info/ayuda.html')

def quienes_somos(request):
    return render(request, 'info/quienes_somos.html')

def politica_privacidad(request):
    return render(request, 'info/politica_privacidad.html')

def tyc(request):
    return render(request, 'info/terminos_condiciones.html')

def blog(request):
    return render(request, 'info/blog.html')
