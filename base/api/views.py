# import os # for production
# os.environ['OPENBLAS_NUM_THREADS'] = '1' # for production

from collections import OrderedDict

from category_encoders import OrdinalEncoder
import pandas as pd

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ViewSet

from base.models import Saw, Kriteria, Item, Subkriteria, Order, OrderItem, Notifikasi
from .serializers import (
    ItemModelSerializer,
    NotifikasiModelSerializer,
    OrderItemModelSerializer,
    OrderModelSerializer, 
    PertanyaanModelSerializer,
)

from .filters import ItemFilterSet


class SawView(APIView):
    def post(self, request, format= None):
        user_response = request.data
        
        # convert model kriteria to df
        kriterias = Kriteria.objects.all()
        kriteria_dict = []
        for kriteria in kriterias:
            kriteria_dict.append({"nama": kriteria.nama_kriteria, "bobot": float(kriteria.bobot), "attribut": kriteria.atribut})
        kriteria_df = pd.DataFrame(kriteria_dict)

        # convert model subkriteria to df
        subkriterias = Subkriteria.objects.all()
        subkriteria_dict = []
        for sub in subkriterias:
            subkriteria_dict.append({"kriteria": str(sub.kriteria), "sub_kriteria": str(sub.nama_subkriteria)})
        sub_kriteria_df = pd.DataFrame(subkriteria_dict)

        # convert model saw to df
        saws = Saw.objects.all()
        list_saw = [saw.subkriteria.kriteria.nama_kriteria for saw in saws if saw.subkriteria != None]
        correct_saw = [saw for saw in saws if saw.subkriteria != None]
        counter = max([list_saw.count(i) for i in list_saw if i != None])
        available_col = []
        for key in list(OrderedDict.fromkeys(list_saw)):
            if key is not None:
                if list_saw.count(key) == counter:
                    available_col.append(key)
                if list_saw.count(key) != counter:
                    print(key)
                    for saw in correct_saw:
                        if saw.subkriteria is not None:
                            if saw.subkriteria.kriteria.nama_kriteria == key:
                                correct_saw.remove(saw)
                                
        saw_dict = []
        for saw in correct_saw:
            if saw.subkriteria is not None:
                saw_dict.append({'alternatif': saw.alternatif.nama_item, 'sub_kriteria' : saw.subkriteria.nama_subkriteria})

        # for i in correct_saw:
        #     print(i)

        saw_df = pd.DataFrame(saw_dict)
        saw_df = saw_df[saw_df.sub_kriteria != 'None']    

        # gabung subkriteria jadi 1 row per alternatif
        merge_saw_df = saw_df.groupby("alternatif", as_index=False, sort=False).agg({"sub_kriteria": ", ".join})

        # ngilangin kategori yang belum terhubung ke alternatif
        set_col = list(set(available_col))
        kriteria_df = kriteria_df[kriteria_df['nama'].isin(set_col)]
        sub_kriteria_df = sub_kriteria_df[sub_kriteria_df['kriteria'].isin(set_col)]

        # convert item to df
        alternatifs = Item.objects.all()
        alternatif_dict = []
        for alt in alternatifs:
            alternatif_dict.append({'alternatif':alt})
        alternatif_df = pd.DataFrame(alternatif_dict)

        col_name = kriteria_df["nama"].values.tolist()
        merge_saw_df[col_name] = merge_saw_df["sub_kriteria"].str.split(", ", expand=True)
        data_df = merge_saw_df.drop(["sub_kriteria"], axis=1).copy()

        # pisahin label dan features
        df = data_df.drop(["alternatif"], axis=1).copy()

        # fungsi pembobotan kriteria
        def bobot_alternatife(sub_kriteria, label, bobot_max, bobot_min, response):
            selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == label]
            if selected_kriteria.iloc[0]["attribut"] == "cost":
                bobot_min = bobot_max
                bobot_max = 1
            input_user = response
            map_kriteria = sub_kriteria.copy()
            for key in map_kriteria.keys():
                if key == input_user:
                    map_kriteria[key] = bobot_max
                if key != input_user:
                    map_kriteria[key] = bobot_min
            return map_kriteria

        # fungsi pembuat format dasar nilai kriteria
        def maping_subkriteria(map_dict):
            key_kriteria = sub_kriteria_df.iloc[:]["kriteria"].unique().tolist()
            for key in key_kriteria:
                map_dict[key] = {}
                selected_sub = sub_kriteria_df.loc[sub_kriteria_df["kriteria"] == key]
                val_kriteria = selected_sub.iloc[:]["sub_kriteria"].values.tolist()
                for value in val_kriteria:
                    map_dict[key].update({value: 0})

        # normalisasi
        def normalisasi(normalisasi):
            for key in normalisasi.keys():
                selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == key]
                if selected_kriteria.iloc[0]["attribut"] != "cost":
                    max_value = normalisasi[key].max()
                    for i in range(normalisasi.shape[0]):
                        max_norm = (normalisasi[key][i] / max_value)
                        normalisasi.loc[i, key] = max_norm
                if selected_kriteria.iloc[0]["attribut"] == "cost":
                    min_value = normalisasi[key].min()
                    for i in range(normalisasi.shape[0]):
                        min_norm = (min_value / normalisasi[key][i])
                        normalisasi.loc[i, key] = min_norm

        # preferensi
        def preferensi(preferensi):
            for key in preferensi.keys():
                selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == key]
                bobot = selected_kriteria.iloc[0]["bobot"]
                for i in range(preferensi.shape[0]):
                    nilai_preferensi = bobot * preferensi[key][i]
                    preferensi.loc[i, key] = nilai_preferensi

        # fungsi guna menghubungkan label dan featurs kembali
        def ranking(rank):
            rank["Jumlah"] = rank.sum(axis=1)
            rank["Alternatif"] = alternatif_df["alternatif"]

        map_kriteria = {}
        maping_subkriteria(map_kriteria)

        key_kriteria = sub_kriteria_df.iloc[:]["kriteria"].unique().tolist()
        for key in key_kriteria:
            map_kriteria[key] = {}
            selected_sub = sub_kriteria_df.loc[sub_kriteria_df["kriteria"] == key]
            val_kriteria = selected_sub.iloc[:]["sub_kriteria"].values.tolist()
            for value in val_kriteria:
                map_kriteria[key].update({value: 0})

        for key in map_kriteria:
            map_kriteria[key] = bobot_alternatife(
                map_kriteria[key], key, len(list(map_kriteria[key].keys())), 1, user_response[key]
            )

        for key in df.keys():
            kriteria_num = [{"col": key, "mapping": map_kriteria[key]}]
            oe = OrdinalEncoder(mapping=kriteria_num)
            df[[key]] = oe.fit_transform(df[[key]])

        normalisasi_df = df.copy()
        normalisasi(normalisasi_df)

        preferensi_df = normalisasi_df.copy()
        preferensi(preferensi_df)

        rank_df = preferensi_df.copy()
        ranking(rank_df)
        sorted_rank = rank_df.sort_values(by=["Jumlah"], ascending=False)

        # bagian api
        serializer = ItemModelSerializer(sorted_rank['Alternatif'][:3], many=True, context={'request': request})

        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    

class PertanyaanView(APIView):
    def get(self, request, format=None):
        kriterias = Kriteria.objects.all()
        pertanyaan_serializer = PertanyaanModelSerializer(kriterias, many=True)

        
        for kriteria in pertanyaan_serializer.data:
            list_subkriteria = []
            for subkriteria in kriteria['subkriteria']:
                list_subkriteria.append(subkriteria['nama_subkriteria'])
            kriteria['subkriteria'] = list_subkriteria


        return Response({
            'data': pertanyaan_serializer.data
        }, status=status.HTTP_200_OK)


class ItemModelViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemModelSerializer
    filterset_class = ItemFilterSet
    search_fields = ['nama_item', 'kategori', 'harga']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': serializer.data})


class OrderItemModelViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
    filterset_fields = ['order', 'item']


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    filterset_fields = ['user', 'status']

    def create(self, request):
        order, created = Order.objects.get_or_create(
            user=request.user,
            status='keranjang'
        )

        item_id = request.data.get('item_id')
        item = Item.objects.get(id=item_id)

        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        order_item.jumlah_pesanan = request.data.get('jumlah_pesanan')
        order_item.total_harga = order_item.item.harga * order_item.jumlah_pesanan
        if request.data.get('catatan'): 
            order_item.catatan = request.data.get('catatan') 
        else: order_item.catatan = ''
        order_item.save()

        order_items = order.orderitem_set.all()
        total = 0
        for item in order_items:
            total += item.total_harga
        order.total_pembayaran = total
        order.save()

        return Response({
            'data': OrderModelSerializer(order).data,
        })

    @action(detail=True, methods=['POST'])
    def confirm_order(self, request, pk):
        order = Order.objects.get(id=pk)
        order.status = 'dikonfirmasi'
        order.save()

        Notifikasi.objects.create(
            user=request.user,
            order=order
        )

        return Response({
            'message': 'Order berhasil dikonfirmasi'
        })
    
    @action(detail=True, methods=['POST'])
    def pay_order(self, request, pk):
        order = Order.objects.get(id=pk)
        order.status = 'selesai'
        order.save()

        Notifikasi.objects.filter(
            user=request.user,
            order=order
        ).update(is_paid=True)

        return Response({
            'message': 'Order berhasil dibayar'
        })


class NotifikasiModelViewSet(ModelViewSet):
    queryset = Notifikasi.objects.all()
    serializer_class = NotifikasiModelSerializer
    filterset_fields = ['user', 'is_paid']


# @api_view(['GET'])
# def get_pertanyaan(request):
#     kriterias = Kriteria.objects.all()
#     pertanyaan_serializer = PertanyaanModelSerializer(kriterias, many=True)

    
#     for kriteria in pertanyaan_serializer.data:
#         list_subkriteria = []
#         for subkriteria in kriteria['subkriteria']:
#             list_subkriteria.append(subkriteria['nama_subkriteria'])
#         kriteria['subkriteria'] = list_subkriteria


#     return Response({
#         'code': '200',
#         'status': 'OK',
#         'data': pertanyaan_serializer.data
#     }, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def saw(request):
#     user_response = request.data
    
#     # convert model kriteria to df
#     kriterias = Kriteria.objects.all()
#     kriteria_dict = []
#     for kriteria in kriterias:
#         kriteria_dict.append({"nama": kriteria.nama_kriteria, "bobot": float(kriteria.bobot), "attribut": kriteria.atribut})
#     kriteria_df = pd.DataFrame(kriteria_dict)

#     # convert model subkriteria to df
#     subkriterias = Subkriteria.objects.all()
#     subkriteria_dict = []
#     for sub in subkriterias:
#         subkriteria_dict.append({"kriteria": str(sub.kriteria), "sub_kriteria": str(sub.nama_subkriteria)})
#     sub_kriteria_df = pd.DataFrame(subkriteria_dict)

#     # convert model saw to df
#     saws = Saw.objects.all()
#     list_saw = [saw.subkriteria.kriteria.nama_kriteria for saw in saws if saw.subkriteria != None]
#     correct_saw = [saw for saw in saws if saw.subkriteria != None]
#     counter = max([list_saw.count(i) for i in list_saw if i != None])
#     available_col = []
#     for key in list(OrderedDict.fromkeys(list_saw)):
#         if key is not None:
#             if list_saw.count(key) == counter:
#                 available_col.append(key)
#             if list_saw.count(key) != counter:
#                 print(key)
#                 for saw in correct_saw:
#                     if saw.subkriteria is not None:
#                         if saw.subkriteria.kriteria.nama_kriteria == key:
#                             correct_saw.remove(saw)
                            
#     saw_dict = []
#     for saw in correct_saw:
#         if saw.subkriteria is not None:
#             saw_dict.append({'alternatif': saw.alternatif.nama_item, 'sub_kriteria' : saw.subkriteria.nama_subkriteria})

#     # for i in correct_saw:
#     #     print(i)

#     saw_df = pd.DataFrame(saw_dict)
#     saw_df = saw_df[saw_df.sub_kriteria != 'None']    

#     # gabung subkriteria jadi 1 row per alternatif
#     merge_saw_df = saw_df.groupby("alternatif", as_index=False, sort=False).agg({"sub_kriteria": ", ".join})

#     # ngilangin kategori yang belum terhubung ke alternatif
#     set_col = list(set(available_col))
#     kriteria_df = kriteria_df[kriteria_df['nama'].isin(set_col)]
#     sub_kriteria_df = sub_kriteria_df[sub_kriteria_df['kriteria'].isin(set_col)]

#     # convert item to df
#     alternatifs = Item.objects.all()
#     alternatif_dict = []
#     for alt in alternatifs:
#         alternatif_dict.append({'alternatif':alt})
#     alternatif_df = pd.DataFrame(alternatif_dict)

#     col_name = kriteria_df["nama"].values.tolist()
#     merge_saw_df[col_name] = merge_saw_df["sub_kriteria"].str.split(", ", expand=True)
#     data_df = merge_saw_df.drop(["sub_kriteria"], axis=1).copy()

#     # pisahin label dan features
#     df = data_df.drop(["alternatif"], axis=1).copy()

#     # fungsi pembobotan kriteria
#     def bobot_alternatife(sub_kriteria, label, bobot_max, bobot_min, response):
#         selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == label]
#         if selected_kriteria.iloc[0]["attribut"] == "cost":
#             bobot_min = bobot_max
#             bobot_max = 1
#         input_user = response
#         map_kriteria = sub_kriteria.copy()
#         for key in map_kriteria.keys():
#             if key == input_user:
#                 map_kriteria[key] = bobot_max
#             if key != input_user:
#                 map_kriteria[key] = bobot_min
#         return map_kriteria

#     # fungsi pembuat format dasar nilai kriteria
#     def maping_subkriteria(map_dict):
#         key_kriteria = sub_kriteria_df.iloc[:]["kriteria"].unique().tolist()
#         for key in key_kriteria:
#             map_dict[key] = {}
#             selected_sub = sub_kriteria_df.loc[sub_kriteria_df["kriteria"] == key]
#             val_kriteria = selected_sub.iloc[:]["sub_kriteria"].values.tolist()
#             for value in val_kriteria:
#                 map_dict[key].update({value: 0})

#     # normalisasi
#     def normalisasi(normalisasi):
#         for key in normalisasi.keys():
#             selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == key]
#             if selected_kriteria.iloc[0]["attribut"] != "cost":
#                 max_value = normalisasi[key].max()
#                 for i in range(normalisasi.shape[0]):
#                     max_norm = (normalisasi[key][i] / max_value)
#                     normalisasi.loc[i, key] = max_norm
#             if selected_kriteria.iloc[0]["attribut"] == "cost":
#                 min_value = normalisasi[key].min()
#                 for i in range(normalisasi.shape[0]):
#                     min_norm = (min_value / normalisasi[key][i])
#                     normalisasi.loc[i, key] = min_norm

#     # preferensi
#     def preferensi(preferensi):
#         for key in preferensi.keys():
#             selected_kriteria = kriteria_df.loc[kriteria_df["nama"] == key]
#             bobot = selected_kriteria.iloc[0]["bobot"]
#             for i in range(preferensi.shape[0]):
#                 nilai_preferensi = bobot * preferensi[key][i]
#                 preferensi.loc[i, key] = nilai_preferensi

#     # fungsi guna menghubungkan label dan featurs kembali
#     def ranking(rank):
#         rank["Jumlah"] = rank.sum(axis=1)
#         rank["Alternatif"] = alternatif_df["alternatif"]

#     map_kriteria = {}
#     maping_subkriteria(map_kriteria)

#     key_kriteria = sub_kriteria_df.iloc[:]["kriteria"].unique().tolist()
#     for key in key_kriteria:
#         map_kriteria[key] = {}
#         selected_sub = sub_kriteria_df.loc[sub_kriteria_df["kriteria"] == key]
#         val_kriteria = selected_sub.iloc[:]["sub_kriteria"].values.tolist()
#         for value in val_kriteria:
#             map_kriteria[key].update({value: 0})

#     for key in map_kriteria:
#         map_kriteria[key] = bobot_alternatife(
#             map_kriteria[key], key, len(list(map_kriteria[key].keys())), 1, user_response[key]
#         )

#     for key in df.keys():
#         kriteria_num = [{"col": key, "mapping": map_kriteria[key]}]
#         oe = OrdinalEncoder(mapping=kriteria_num)
#         df[[key]] = oe.fit_transform(df[[key]])

#     normalisasi_df = df.copy()
#     normalisasi(normalisasi_df)

#     preferensi_df = normalisasi_df.copy()
#     preferensi(preferensi_df)

#     rank_df = preferensi_df.copy()
#     ranking(rank_df)
#     sorted_rank = rank_df.sort_values(by=["Jumlah"], ascending=False)

#     # bagian api
#     serializer = ItemModelSerializer(sorted_rank['Alternatif'][:3], many=True)

#     return Response({
#         'code': '200',
#         'status': 'OK',
#         'data': serializer.data
#     }, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def add_kriteria(request):
#     nama_kriteria = request.data.get('nama_kriteria')
#     atribut = request.data.get('atribut')
#     bobot = request.data.get('bobot')

#     cek_kriteria = Kriteria.objects.filter(nama_kriteria=nama_kriteria)
#     if cek_kriteria: return Response({
#         'code': '400',
#         'status': 'BAD_REQUEST',
#         'error': 'Kriteria sudah ada'
#         }, status=status.HTTP_400_BAD_REQUEST)

#     kriteria = Kriteria(
#         nama_kriteria = nama_kriteria,
#         atribut = atribut,
#         bobot = bobot
#     )
#     kriteria_serializer = KriteriaModelSerializer(kriteria)

#     list_subkriteria = list(request.data.get('subkriteria'))
#     list_obj_subkriteria = []
#     for subkriteria in list_subkriteria:
#         obj_subkriteria = Subkriteria(
#             kriteria=kriteria,
#             nama_subkriteria=subkriteria
#         )
#         list_obj_subkriteria.append(obj_subkriteria)
#     subkriteria_serializer = SubkriteriaModelSerializer(list_obj_subkriteria, many=True)

#     alternatifs = Item.objects.all()
#     list_obj_saw = []
#     for alternatif in alternatifs:
#         saw = Saw(
#             alternatif=alternatif,
#             subkriteria=None
#         )
#         list_obj_saw.append(saw)
#     saw_serializer = SawModelSerializer(list_obj_saw, many=True)

#     # save kriteria object 
#     kriteria.save()
#     # save subkriteria objects
#     for subkriteria in list_obj_subkriteria:
#         subkriteria.save()
#     # save saw objects
#     for saw in list_obj_saw:
#         saw.save()

#     return Response({
#         'code': '201',
#         'status': 'CREATED',
#     }, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def add_item(request):
#     nama_item = request.data.get('nama_item')
#     kategori = request.data.get('kategori')
#     harga = request.data.get('harga')

#     cek_item = Item.objects.filter(nama_item=nama_item)
#     if cek_item: return Response({
#         'code': '400',
#         'status': 'BAD_REQUEST',
#         'error': 'Item sudah ada'
#     }, status=status.HTTP_400_BAD_REQUEST)

#     alternatif = Item(nama_item=nama_item, kategori=kategori, harga=harga)

#     list_subkriteria = list(request.data.get('subkriteria'))
#     list_obj_saw = []
#     for subkriteria in list_subkriteria:
#         saw = Saw(
#             alternatif=alternatif,
#             subkriteria=Subkriteria.objects.get(id=subkriteria),
#         )
#         list_obj_saw.append(saw)

#     # save alternatif objects
#     alternatif.save()
#     # save saw objects
#     for saw in list_obj_saw:
#         saw.save()
    
#     return Response({
#         'code': '201',
#         'status': 'CREATED'
#     }, status=status.HTTP_201_CREATED)




