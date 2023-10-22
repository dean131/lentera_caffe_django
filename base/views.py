from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .models import Item, Saw, Kriteria, Subkriteria, Order, OrderItem, Notifikasi
from account.models import User

def login_user(request):
    if request.method == 'POST':
        email = request.POST["inputEmail"]
        password = request.POST["inputPassword"]
        user = authenticate(email=email, password=password)
        if user and user.is_superuser == True:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

def register_customer(request):
    if request.method == 'POST':
        full_name = request.POST["inputNamaUser"]
        email = request.POST["inputEmailUser"]
        phone_number = request.POST["inputTeleponUser"]
        password = request.POST["inputPasswordUser"]
        password2 = request.POST["inputPassword2User"]
        profile_picture = request.FILES.get('inputGambarUser')

        if password != password2:
            messages.error(
                request=request, 
                message=f'Password tidak sama!', 
            )
            return redirect('customers_page')

        user = User.objects.create_user(
            email=email, 
            password=password, 
            full_name=full_name, 
            phone_number=phone_number,
            profile_picture=profile_picture,
        )

        messages.success(
            request=request, 
            message=f'User "{user.full_name}" berhasil ditambahkan.', 
        )

        return redirect('customers_page')

def register_cashier(request):
    if request.method == 'POST':
        full_name = request.POST["inputNamaUser"]
        email = request.POST["inputEmailUser"]
        phone_number = request.POST["inputTeleponUser"]
        password = request.POST["inputPasswordUser"]
        password2 = request.POST["inputPassword2User"]
        profile_picture = request.FILES.get('inputGambarUser')

        if password != password2:
            messages.error(
                request=request, 
                message=f'Password tidak sama!', 
            )
            return redirect('cashier_page')

        user = User.objects.create_user(
            email=email, 
            password=password, 
            full_name=full_name, 
            phone_number=phone_number,
            profile_picture=profile_picture,
            is_admin=True
        )

        messages.success(
            request=request, 
            message=f'User "{user.full_name}" berhasil ditambahkan.', 
        )

        return redirect('cashier_page')
    
def register_admin(request):
    if request.method == 'POST':
        full_name = request.POST["inputNamaUser"]
        email = request.POST["inputEmailUser"]
        phone_number = request.POST["inputTeleponUser"]
        password = request.POST["inputPasswordUser"]
        password2 = request.POST["inputPassword2User"]
        profile_picture = request.FILES.get('inputGambarUser')

        if password != password2:
            messages.error(
                request=request, 
                message=f'Password tidak sama!', 
            )
            return redirect('admin_page')

        user = User.objects.create_user(
            email=email, 
            password=password, 
            full_name=full_name, 
            phone_number=phone_number,
            profile_picture=profile_picture,
            is_admin=True,
            is_superuser=True,
        )

        messages.success(
            request=request, 
            message=f'User "{user.full_name}" berhasil ditambahkan.', 
        )

        return redirect('admin_page')
    
def edit_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('inputUserId')
        full_name = request.POST.get('inputNamaUser')
        email = request.POST.get('inputEmailUser')
        phone_number = request.POST.get('inputTeleponUser')
        password = request.POST.get('inputPasswordUser')
        password2 = request.POST.get('inputPassword2User')
        profile_picture = request.FILES.get('inputGambarUser')

        if password != password2:
            messages.error(
                request=request, 
                message=f'Password tidak sama!', 
            )
            return redirect('customers_page')

        user = User.objects.get(id=int(user_id))
        user.full_name = full_name
        user.email = email
        user.phone_number = phone_number

        if profile_picture: 
            user.profile_picture = profile_picture
        
        if not password:
            user.save()

        messages.success(
            request=request, 
            message=f'User "{user.full_name}" berhasil diubah.', 
        )
        
        return redirect('customers_page')
        
def delete_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('inputDeleteId')
        user = User.objects.get(id=int(user_id))
        user.delete()
        messages.success(
                request=request, 
                message=f'User "{user.full_name}" berhasil dihapus.', 
        )
    return redirect('customers_page')

def logout_user(request):
    logout(request)
    return redirect('login_user')

@login_required(login_url='login-user/')
def dashboard(request):
    customers_count = User.objects.filter(is_admin=False).count()
    items_count = Item.objects.all().count()
    unprocessed_orders_count = Order.objects.filter(status='dikonfirmasi').count()
    context = {
        'customers_count': customers_count,
        'items_count': items_count,
        'unprocessed_orders_count': unprocessed_orders_count,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login-user/')
def customers_page(request):
    customers = User.objects.filter(is_admin=False)
    context = {
        'customers': customers
    }
    return render(request, 'customers_page.html', context)

@login_required(login_url='login-user/')
def cashier_page(request):
    cashiers = User.objects.filter(is_admin=True, is_superuser=False)
    context = {
        'cashiers': cashiers
    }
    return render(request, 'cashier_page.html', context)

@login_required(login_url='login-user/')
def admin_page(request):
    admins = User.objects.filter(is_superuser=True)
    context = {
        'admins': admins
    }
    return render(request, 'admin_page.html', context=context)

@login_required(login_url='login-user/')
def order_page(request):
    orders = Order.objects.all().exclude(status='selesai').order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'order_page.html', context)

@login_required(login_url='login-user/')
def order_history_page(request):
    orders = Order.objects.filter(status='selesai')
    context = {
        'orders': orders
    }
    return render(request, 'order_history_page.html', context)

@login_required(login_url='login-user/')
def notification_page(request):
    notifications = Notifikasi.objects.all()
    context = {
        'notifications': notifications
    }
    return render(request, 'notification_page.html', context)


# ===== ITEM VIEWS =====
@login_required(login_url='login-user/')
def item_page(request):
    items = Item.objects.all()
    list_item = []
    for item in items:
        item_obj = {}
        item_obj['id'] = item.id
        item_obj['nama_item'] = item.nama_item
        item_obj['kategori'] = item.kategori
        item_obj['harga'] = item.harga
        item_obj['stok'] = item.stok
        item_obj['deskripsi'] = item.deskripsi
        item_obj['nilai'] = item.nilai
        item_obj['gambar'] = item.gambar
        item_obj['kriterias'] = []

        kriterias = Kriteria.objects.all()

        saws = item.saw_set.all()
        for i, saw in enumerate(saws):
            item_obj['kriterias'].append({kriterias[i].nama_kriteria: saw.subkriteria.nama_subkriteria if saw.subkriteria is not None else None})

        list_item.append(item_obj)

    kriterias = Kriteria.objects.all()
    list_kriteria = []
    for kriteria in kriterias:
        sub_by_krit = {}
        sub_by_krit[kriteria.nama_kriteria] = [sub.nama_subkriteria for sub in kriteria.subkriteria_set.all()]
        list_kriteria.append(sub_by_krit)

    
    context = {
        'list_item': list_item,
        'list_kriteria': list_kriteria
    }
    return render(request, 'item_page.html', context)

@login_required(login_url='login-user/')
def add_item(request):
    if request.method == 'POST':
        nama = request.POST.get('inputNamaItem')
        kategori = request.POST.get('inputKategoriItem')
        harga = request.POST.get('inputHargaItem')
        stok = request.POST.get('inputStokItem')
        gambar = request.POST.get('inputGambarItem')

        existing_item = Item.objects.filter(nama_item=nama)
        if existing_item.exists():
            messages.error(
                request=request, 
                message=f'Nama menu "{nama}" sudah ada.', 
            )
            return redirect('item_page')

        item = Item.objects.create(nama_item=nama, kategori=kategori, harga=harga, stok=stok, gambar=gambar)

        kriterias = Kriteria.objects.all()
        list_subs = []
        for kriteria in kriterias:
            sub = request.POST.get(kriteria.nama_kriteria)
            list_subs.append(sub)

        for subkriteria in list_subs:
            Saw.objects.create(
                alternatif=item,
                subkriteria=Subkriteria.objects.get(nama_subkriteria=subkriteria)
            )

        messages.success(
                request=request, 
                message=f'Item "{item.nama_item}" berhasil ditambahkankan.', 
        )
        return redirect('item_page')
    
@login_required(login_url='login-user/')
def edit_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('inputItemId')
        nama = request.POST.get('inputNamaItem')
        kategori = request.POST.get('inputKategoriItem')
        harga = request.POST.get('inputHargaItem')
        stok = request.POST.get('inputStokItem')
        deskripsi = request.POST.get('inputDeskripsiItem')
        gambar = request.FILES.get('inputGambarItem')

        existing_item = Item.objects.filter(nama_item=nama).exclude(id=item_id)
        if existing_item.exists():
            messages.error(
                request=request, 
                message=f'Nama menu "{nama}" sudah ada!', 
            )
            return redirect('item_page')
        
        item = Item.objects.get(id=item_id)
        
        item.nama_item = nama
        item.kategori = kategori
        item.harga = harga
        item.stok = stok
        item.deskripsi = deskripsi
        if gambar:
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
                message=f'Item "{item.nama_item}" berhasil diupdate.', 
        )
        return redirect('item_page')

@login_required(login_url='login-user/')
def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('inputDeleteId')
        item = Item.objects.get(id=int(item_id))
        saws = Saw.objects.filter(alternatif=item)
        for saw in saws:
            saw.delete()
        item.delete()
        messages.success(
                request=request, 
                message=f'Item "{item.nama_item}" berhasil dihapus.', 
        )
    return redirect('item_page')


# ===== SAW VIEWS =====
@login_required(login_url='login-user/')
def saw_page(request):
    items = Item.objects.all()

    saw_res = []
    for item in items:
        saw_by_item = {}
        saw_by_item['id'] = item.id
        saw_by_item['nama_item'] = item.nama_item
        saw_by_item['subkriterias'] = []
        saw_res.append(saw_by_item)

        kriterias = Kriteria.objects.all()

        saws = item.saw_set.all()
        for i, saw in enumerate(saws):
            saw_dict = {}
            saw_dict[kriterias[i].nama_kriteria] = saw.subkriteria.nama_subkriteria if saw.subkriteria is not None else None
            saw_by_item['subkriterias'].append(saw_dict)

    context = {
        'saws': saw_res
    }
    return render(request, 'saw_page.html', context)

# ===== KRITERIA VIEWS =====
@login_required(login_url='login-user/')
def kriteria_page(request):

    kriterias = Kriteria.objects.all()
    context = {
        'kriterias': kriterias
    }
    return render(request, 'kriteria_page.html', context)

@login_required(login_url='login-user/')
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
            message=f'Kriteria "{kriteria.nama_kriteria}" berhasil ditambahkan.', 
    )
    return redirect('kriteria_page')

@login_required(login_url='login-user/')
def edit_kriteria(request):
    id_kriteria = request.POST.get('inputKriteriaId')
    nama_kriteria = request.POST.get('inputNamaKriteria')
    atribut = request.POST.get('inputAttribut')
    bobot = request.POST.get('inputBobot')
    pertanyaan = request.POST.get('inputPertanyaan')

    Kriteria.objects.filter(id=id_kriteria).update(
        nama_kriteria = nama_kriteria,
        atribut=atribut,
        bobot=float(bobot),
        pertanyaan=pertanyaan
    )

    messages.success(
        request=request, 
        message=f'Kriteria "{nama_kriteria}" berhasil diubah.', 
    )
    return redirect('kriteria_page')

@login_required(login_url='login-user/')
def delete_kriteria(request):
    if request.method == 'POST':
        kriteria_id = request.POST.get('inputDeleteId')

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
            message=f'Kriteria "{kriteria.nama_kriteria}" berhasil dihapus.', 
        )
    return redirect('kriteria_page')

# ===== SUBKRITERIA =====
@login_required(login_url='login-user/')
def subkriteria_page(request):
    subkriterias = Subkriteria.objects.all()
    kriterias = Kriteria.objects.all()
    context = {
        'subkriterias': subkriterias,
        'kriterias': kriterias 
    }
    return render(request, 'subkriteria_page.html', context)

@login_required(login_url='login-user/')
def add_subkriteria(request):
    nama_subkriteria = request.POST.get('inputNamaSubkriteria')
    nama_kriteria = request.POST.get('inputNamaKriteria')

    kriteria = Kriteria.objects.filter(nama_kriteria=nama_kriteria).first()

    subkriteria, created = Subkriteria.objects.get_or_create(
        nama_subkriteria=nama_subkriteria,
        kriteria=kriteria
    )
    if created:
        messages.success(
            request=request, 
            message=f'Subkriteria "{subkriteria.nama_subkriteria}" berhasil ditambahkan.', 
        )
    else:
        messages.error(
            request=request, 
            message=f'Subkriteria "{subkriteria.nama_subkriteria}" telah ditambahkan sebelumnya!', 
        )
    
    return redirect('subkriteria_page')

@login_required(login_url='login-user/')
def edit_subkriteria(request):
    subkriteria_id = request.POST.get('inputKriteriaId')
    nama_subkriteria = request.POST.get('inputNamaSubkriteria')
    nama_kriteria = request.POST.get('inputNamaKriteria')

    kriteria = Kriteria.objects.filter(nama_kriteria=nama_kriteria).first()

    # cek duplikasi data 
    existing_subkriteria = Subkriteria.objects.filter(nama_subkriteria=nama_subkriteria).exclude(id=subkriteria_id)
    if existing_subkriteria:
        messages.error(
            request=request,
            message=f'Subkriteria "{existing_subkriteria[0]}" sudah ada.',
        )
        return redirect('subkriteria_page')

    Subkriteria.objects.filter(id=subkriteria_id).update(
        nama_subkriteria=nama_subkriteria,
        kriteria=kriteria
    )   

    messages.success(
        request=request, 
        message=f'Subkriteria "{nama_subkriteria}" berhasil diubah!', 
    )
    return redirect('subkriteria_page')

@login_required(login_url='login-user/')
def delete_subkriteria(request):
    subkriteria_id = request.POST['inputDeleteId']
    subkriteria = Subkriteria.objects.get(id=subkriteria_id)

    # menghapus objects saw yang berhubungan dengan subkriteria
    saws = Saw.objects.filter(subkriteria=subkriteria)
    for saw in saws:
        saw.subkriteria = None
        saw.save()

    subkriteria.delete()

    messages.success(
            request=request, 
            message=f'Subkriteria "{subkriteria.nama_subkriteria}" berhasil.', 
    )
    return redirect('subkriteria_page')



    