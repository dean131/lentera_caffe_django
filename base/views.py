from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Item, Saw, Kriteria, Subkriteria

import json
from django.shortcuts import HttpResponse

def login(request):
    # if request.method == 'POST':
    #     username = request.POST["username"]
    #     password = request.POST["password"]
    #     user = 
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def customers_page(request):
    return render(request, 'customers_page.html')

def cashier_page(request):
    return render(request, 'cashier_page.html')

def admin_page(request):
    return render(request, 'admin_page.html')

def order_page(request):
    return render(request, 'order_page.html')

def cart_page(request):
    return render(request, 'cart_page.html')

def notification_page(request):
    return render(request, 'notification_page.html')


# ===== ITEM VIEWS =====
def menu_page(request):
    menus = Item.objects.all()
    kriterias = Kriteria.objects.all()

    list_kriteria = {}
    for kriteria in kriterias:
        subs = Subkriteria.objects.filter(kriteria=kriteria)
        list_subs = []
        for sub in subs:
            list_subs.append(sub.nama_subkriteria)
        list_kriteria.update({f'{kriteria.nama_kriteria}': list_subs})

    from .serializers import MenuModelSerializer
    menus_serializer = MenuModelSerializer(menus, many=True)

    # return HttpResponse(json.dumps(menus_serializer.data))
    
    context = {
        'menus': menus_serializer.data,
        'list_kriteria': list_kriteria
    }
    return render(request, 'menu_page.html', context)

def add_item(request):
    if request.method == 'POST':
        nama = request.POST.get('inputNamaItem')
        kategori = request.POST.get('inputKategoriItem')
        harga = request.POST.get('inputHargaItem')
        stok = request.POST.get('inputStokItem')
        gambar = request.POST.get('inputGambarItem')

        cek_item = Item.objects.filter(nama_item=nama)
        if cek_item:
            messages.error(
                request=request, 
                message='Nama menu sudah terdaftar!', 
            )
            return redirect('menu_page')

        item = Item(nama_item=nama, kategori=kategori, harga=harga, stok=stok, gambar=gambar)

        kriterias = Kriteria.objects.all()
        list_subs = []
        for kriteria in kriterias:
            sub = request.POST.get(kriteria.nama_kriteria)
            list_subs.append(sub)

        list_obj_saw = []
        for subkriteria in list_subs:
            saw = Saw(
                alternatif=item,
                subkriteria=Subkriteria.objects.get(nama_subkriteria=subkriteria),
            )
            list_obj_saw.append(saw)

        item.save()

        for saw in list_obj_saw:
            saw.save()
        messages.success(
                request=request, 
                message='Succes menambahkan item baru!', 
        )
        return redirect('menu_page')
    
def edit_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('inputIdItem')
        nama = request.POST.get('inputNamaItem')
        kategori = request.POST.get('inputKategoriItem')
        harga = request.POST.get('inputHargaItem')
        stok = request.POST.get('inputStokItem')
        gambar = request.FILES.get('inputGambarItem')

        cek_item = Item.objects.filter(nama_item=nama)
        if cek_item and (cek_item[0].id != int(item_id)):
            messages.error(
                request=request, 
                message='Nama menu sudah terdaftar!', 
            )
            return redirect('menu_page')

        item = Item.objects.get(id=item_id)
        item.nama_item = nama
        item.kategori = kategori
        item.harga = harga
        item.stok = stok
        item.gambar = gambar
        item.save()

        kriterias = Kriteria.objects.all()
        
        subs_dict = []
        for kriteria in kriterias:
            sub = request.POST.get(kriteria.nama_kriteria)
            subs_dict.append(sub)
        
        saws = item.saw_set.all()
        for i, saw in enumerate(saws):
            saw.subkriteria = Subkriteria.objects.get(nama_subkriteria=subs_dict[i])
            saw.save()
               
        messages.success(
                request=request, 
                message='Succes mengupdate item!', 
        )
        return redirect('menu_page')

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('id')
        item = Item.objects.get(id=int(item_id))
        saws = Saw.objects.filter(alternatif=item)
        for saw in saws:
            saw.delete()
        item.delete()
        messages.success(
                request=request, 
                message='Succes menghapus item!', 
        )
    return redirect('menu_page')


# ===== SAW VIEWS =====
def saw_page(request):
    saws = Saw.objects.all()
    context = {
        'saws': saws
    }
    return render(request, 'saw_page.html', context)

# ===== KRITERIA VIEWS =====
def kriteria_page(request):

    kriterias = Kriteria.objects.all()
    context = {
        'kriterias': kriterias
    }
    return render(request, 'kriteria_page.html', context)

def add_kriteria(request):
    nama_kriteria = request.POST.get('inputNamaKriteria')
    atribut = request.POST.get('inputAttribut')
    bobot = request.POST.get('inputBobot')
    pertanyaan = request.POST.get('inputPertanyaan')
    list_subs = str(request.POST.get('inputListSubkriteria')).replace(' ', '').split(',')

    kriteria = Kriteria(
        nama_kriteria = nama_kriteria,
        atribut = atribut,
        bobot = bobot,
        pertanyaan = pertanyaan
    )

    list_obj_subkriteria = []
    for subkriteria in list_subs:
        obj_subkriteria = Subkriteria(
            kriteria=kriteria,
            nama_subkriteria=subkriteria
        )
        list_obj_subkriteria.append(obj_subkriteria)

    alternatifs = Item.objects.all()
    list_obj_saw = []
    for alternatif in alternatifs:
        saw = Saw(
            alternatif=alternatif,
            subkriteria=None
        )
        list_obj_saw.append(saw)

    kriteria.save()
    for subkriteria in list_obj_subkriteria:
        subkriteria.save()

    for saw in list_obj_saw:
        saw.save()

    messages.success(
            request=request, 
            message='Succes mengupdate saw!', 
    )
    return redirect('kriteria_page')

def edit_kriteria(request):
    
    return redirect('kriteria_page')

def delete_kriteria(request):
    if request.method == 'POST':
        kriteria_id = request.POST.get('id')

        kriteria = Kriteria.objects.get(id=int(kriteria_id))
        subkriterias = kriteria.subkriteria_set.all()
        list_saw = []
        for sub in subkriterias:
            saws = sub.saw_set.all()
            for saw in saws:
                list_saw.append(saw)
        
        for saw in list_saw:
            saw.delete()

        for sub in subkriterias:
            sub.delete()
        
        kriteria.delete()

        messages.success(
                request=request, 
                message='Succes menghapus kriteria!', 
        )
    return redirect('kriteria_page')

# ===== SUBKRITERIA =====
def subkriteria_page(request):
    subkriterias = Subkriteria.objects.all()
    context = {
        'subkriterias': subkriterias
    }
    return render(request, 'subkriteria_page.html', context)



    