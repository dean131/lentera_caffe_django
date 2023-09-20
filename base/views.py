from django.shortcuts import render

from .models import Item, Saw, Kriteria, Subkriteria



def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def customers_page(request):
    return render(request, 'customers_page.html')

def cashier_page(request):
    return render(request, 'cashier_page.html')

def admin_page(request):
    return render(request, 'admin_page.html')

def menu_page(request):
    if request.method == 'POST':
        name = request.POST.get('register-name')
        category = request.POST.get('register-category')
        price = request.POST.get('register-price')
        stock = request.POST.get('register-stock')
        picture = request.POST.get('register-picture')

    menus = Item.objects.all()

    context = {
        'menus': menus
    }
    return render(request, 'menu_page.html', context)

def order_page(request):
    return render(request, 'order_page.html')

def cart_page(request):
    return render(request, 'cart_page.html')

def notification_page(request):
    return render(request, 'notification_page.html')

def saw_page(request):
    saws = Saw.objects.all()
    context = {
        'saws': saws
    }
    return render(request, 'saw_page.html', context)

def kriteria_page(request):
    if request.method == 'POST':
        subkriteria = str(request.POST.get('register-subkriteria'))
        substr = subkriteria.replace(' ', '').split(',')
        print(list(substr))

    kriterias = Kriteria.objects.all()
    context = {
        'kriterias': kriterias
    }
    return render(request, 'kriteria_page.html', context)

def subkriteria_page(request):
    subkriterias = Subkriteria.objects.all()
    context = {
        'subkriterias': subkriterias
    }
    return render(request, 'subkriteria_page.html', context)


    