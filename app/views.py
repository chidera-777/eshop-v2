from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.http import HttpResponse
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import Category, Product, Newsletter
from cart.forms import CartAddProductForm
from .forms import NewsletterForm
#from .tasks import subscriber
#from .recommender import Recommender

# Create your views here.
def product_list(request, category_slug=None):
  category = None
  categories = Category.objects.all()  
  products = Product.objects.filter(available=True)
  product_deal = Product.objects.filter(deals=True)
  if category_slug:
    category = get_object_or_404(Category, slug=category_slug)
    products = products.filter(category=category)
    product_deal = product_deal.filter(category=category)
  return render(request, 'products/list.html', {'category': category, 'categories': categories, 'products': products, 'product_deal': product_deal})
  
def product_details(request, id, slug):
   product = get_object_or_404(Product, id=id, slug=slug)
   cart_product_form = CartAddProductForm()
   #r = Recommender()
   #recommended_products = r.suggest_products_for([product], 4)
   return render(request, 'products/detail.html',  {'product': product, 'cart_product_form': cart_product_form})

def search_list(request):
    search_post = request.GET['q']
    categories = Category.objects.all()
    if search_post:
        search_query = Product.objects.annotate(search=SearchVector('category__name', 'name')).filter(search=SearchQuery(search_post))
    else:
        messages.error(request, 'Sorry, We could not find any related item')
    return render(request, 'products/search.html', {'search_post':search_post, 'categories': categories, 'search_query': search_query})
    
def sm_search(request):
  return render(request, 'sm_search.html')
    
def newsletter(request):
  if request.method == 'POST':
      email = request.POST['email']
      try:
        old_subcriber = Newsletter.objects.get(email=email)
        messages.error(request, 'A subscription already exists for this email')
        return redirect('app:product_list')
      except:
        if email is not None:
            new_subscriber = Newsletter.objects.create(email=email)
            new_subscriber.save()
            #subscriber.delay(email)
            subject = 'Thanks for Subscribing'
            html_content = render_to_string('newsletter.html')
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except BadHeaderError:
               return HttpResponse('Invalid Header Found')
            messages.success(request, 'Thanks for subscribing!')
            return redirect('app:product_list')
  return render(request, 'base.html')