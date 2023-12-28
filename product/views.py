from django.shortcuts import render ,get_object_or_404,redirect

from .models import Category, Product,SuperCategory
from django.db.models import Q





def products(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    products = Product.objects.all()

    # Check if a category ID is provided
    if category_id:
        # Fetch the category based on the ID
        category = get_object_or_404(Category, id=category_id)
        
        # Breadcrumbs for the category search results
        breadcrumbs = [
            ('Home', '/'),
            ('Products', '/products/'),
            (category.name, f'/products/?category={category.id}'),
        ]

        # Filter products based on the category
        products = Product.objects.filter(category=category)

        return render(request, 'product/search_results.html', {
            'products': products,
            'categories': categories,
            'breadcrumbs': breadcrumbs,
            'query': f'Category: {category.name}',
        })

    # Breadcrumbs for the general products view
    breadcrumbs = [
        ('Home', '/'),
        ('Products', '/products/'),
    ]

    return render(request, 'product/products.html', {
        'products': products,
        'categories': categories,
        'breadcrumbs': breadcrumbs,
    })
    

    

def details(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # Example: Get the category and super category for the product
    category = product.category
    super_category = product.superCategory
    product_images = product.images.all()  # Use 'images.all()' to get all images for the product
    breadcrumbs = [
        ('Home', '/'),  # Link to the home page
        ('Products', '/products/'),  # Link to the products view
    ]

    # Add breadcrumbs for category if available
    if category:
        # Find all categories related to the product
        related_categories = Category.objects.filter(products=product).distinct()

        # Add breadcrumbs for unique related categories
        for related_category in related_categories:
            breadcrumbs.append((related_category.name, f'/products/?category={related_category.id}'))

    # Add breadcrumbs for super category if available
    if super_category:
        breadcrumbs.append((super_category.name, f'/products/{super_category.name.lower()}/'))

    # Add breadcrumb for the current product
    breadcrumbs.append((product.name, f'/products/{product.id}/'))

    return render(request, 'product/details.html', {
        'product': product,
        'product_images': product_images,
        'breadcrumbs': breadcrumbs,  # Pass breadcrumbs to the template context
    })

def woman(request):
    # Get the super category with the name 'Woman'
    woman_super_category = SuperCategory.objects.get(name='Woman')

    # Check if a category ID is provided in the query parameters
    category_id = request.GET.get('category')
    if category_id:
        # Redirect to search results with the specified category filter
        return redirect(f'/products/?category={category_id}')

    # Filter products based on the super category
    products = Product.objects.filter(superCategory=woman_super_category)

    # Breadcrumbs for the woman view
    breadcrumbs = [
        ('Home', '/'),
        ('Products', '/products/'),
        ('Woman', '/products/woman/'),
    ]

    return render(request, 'product/woman.html', {
        'products': products,
        'superCategory': woman_super_category,
        'breadcrumbs': breadcrumbs,
    })


def man(request):
    # Get the super category with the name 'Man'
    man_super_category = SuperCategory.objects.get(name='Man')

    # Check if a category ID is provided in the query parameters
    category_id = request.GET.get('category')
    if category_id:
        # Redirect to search results with the specified category filter
        return redirect(f'/products/?category={category_id}')

    # Filter products based on the super category
    products = Product.objects.filter(superCategory=man_super_category)

    # Breadcrumbs for the man view
    breadcrumbs = [
        ('Home', '/'),
        ('Products', '/products/'),
        ('Man', '/products/man/'),
    ]

    return render(request, 'product/man.html', {
        'products': products,
        'superCategory': man_super_category,
        'breadcrumbs': breadcrumbs,
    })
    
    

def search_results(request):
    query = request.GET.get('q', '')
    
    # Split the query into keywords
    keywords = query.split()

    # Create a Q object for each keyword to search for product name, category name, and super category name
    name_queries = [Q(name__icontains=keyword) for keyword in keywords]
    category_queries = [Q(category__name__iexact=keyword) for keyword in keywords]
    super_category_queries = [Q(superCategory__name__iexact=keyword) for keyword in keywords]

    # Combine the Q objects with OR to get results that match any of the keywords
    name_query = Q()
    category_query = Q()
    super_category_query = Q()

    for q in name_queries:
        name_query |= q

    for q in category_queries:
        category_query |= q

    for q in super_category_queries:
        super_category_query |= q

    # Get the products that match the search criteria
    products = Product.objects.filter(name_query | category_query | super_category_query)

    # Breadcrumbs for the search results view
    breadcrumbs = [
        ('Home', '/'),
        ('Products', '/products/'),
        ('Search Results', f'/products/search/?q={query}'),
    ]

    # Check if the search query includes the word "Jean"
    if "Jean" in keywords:
        # Add breadcrumb for "Jean"
        breadcrumbs.append(('Jean', f'/products/search/?q=Jean'))

    # Extract unique super categories from the search results
    super_categories = products.values_list('superCategory__name', flat=True).distinct()

    # Add breadcrumbs for each super category
    for super_category in super_categories:
        breadcrumbs.append((super_category, f'/products/?super_category={super_category}'))

    return render(request, 'product/search_results.html', {'products': products, 'query': query, 'breadcrumbs': breadcrumbs}) 