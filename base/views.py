from django.shortcuts import redirect, render
from django.contrib import messages

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
    menus = Item.objects.all()
    kriterias = Kriteria.objects.all()

    if request.method == 'POST':
        nama = request.POST.get('register-nama')
        kategori = request.POST.get('register-kategori')
        harga = request.POST.get('register-harga')
        stok = request.POST.get('register-stok')
        gambar = request.POST.get('register-gambar')

        list_subs = []
        for kriteria in kriterias:
            sub = request.POST.get(kriteria.nama_kriteria)
            list_subs.append(sub)

        cek_item = Item.objects.filter(nama_item=nama)
        if cek_item:
            messages.error(
                request=request, 
                message='Nama menu sudah terdaftar!', 
                extra_tags='danger'
            )
            return redirect('menu_page')

        alternatif = Item(nama_item=nama, kategori=kategori, harga=harga, stok=stok, gambar=gambar)

        list_obj_saw = []
        for subkriteria in list_subs:
            saw = Saw(
                alternatif=alternatif,
                subkriteria=Subkriteria.objects.get(nama_subkriteria=subkriteria),
            )
            list_obj_saw.append(saw)

        # save alternatif objects
        alternatif.save()
        # save saw objects
        for saw in list_obj_saw:
            saw.save()
        messages.error(
                request=request, 
                message='Succes menambahkan item baru!', 
                extra_tags='success'
        )
        return redirect('menu_page')

    list_kriteria = {}
    for kriteria in kriterias:
        subs = Subkriteria.objects.filter(kriteria=kriteria)
        list_subs = []
        for sub in subs:
            list_subs.append(sub.nama_subkriteria)
        list_kriteria.update({f'{kriteria.nama_kriteria}': list_subs})
    
    
    context = {
        'menus': menus,
        'list_kriteria': list_kriteria
    }
    return render(request, 'menu_page.html', context)

def delete_item(request):
    if request.method == 'POST':
        item_id = int(request.POST.get('id'))
        print(item_id)
        print(type(item_id))
        item = Item.objects.get(id=item_id)
        print(item)
        saws = Saw.objects.filter(alternatif=item)
        for saw in saws:
            saw.delete()
            print('saw terdelete')
        item.delete()
        print('item terdelete')
        messages.error(
                request=request, 
                message='Succes menghapus item!', 
                extra_tags='success'
        )
    return redirect('menu_page')

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



    