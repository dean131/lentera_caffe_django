from django.shortcuts import render

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
    return render(request, 'menu_page.html')

def order_page(request):
    return render(request, 'order_page.html')

def cart_page(request):
    return render(request, 'cart_page.html')

def notification_page(request):
    return render(request, 'notification_page.html')