from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, 'home.html', {
        # using request.POST.get() instead of request.POST[]
        # causes '' to be returned when key doesn't exist
        'new_item_text': request.POST.get('item_text', ''),
        })