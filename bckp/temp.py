[
    {
        "id": 1,
        "nama_item": "beef crispy",
        "subkriteria": [
            {
                "cuaca": "dingin"
            },
            {
                "rasa": "manis"
            },
            {
                "kondisi": "teman"
            }
        ]
    }
]


[
    {
        'nama_item': 'beef crspy',
        'kategori': 'makanan',
        'harga': 20000,
        'gambar': 'null',
        'stok': 'tersedia',
        'nilai': 0,
        'kriterias': [
            {
                "cuaca": "dingin"
            },
            {
                "rasa": "manis"
            },
            {
                "kondisi": "teman"
            }
        ]
    }
]


#normal
saw_res = []
for item in items:
    saw_by_item = {}
    saw_by_item['id'] = item.id
    saw_by_item['nama_item'] = item.nama_item
    saw_by_item['subkriterias'] = [saw.subkriteria.nama_subkriteria if saw.subkriteria is not None else None for saw in item.saw_set.all()]
    saw_res.append(saw_by_item)



saw_res = []
for item in items:
    saw_by_item = {}
    saw_by_item['id'] = item.id
    saw_by_item['nama_item'] = item.nama_item
    saw_by_item['subkriterias'] = []
    saw_res.append(saw_by_item)

    saws = item.saw_set.all()
    for saw in saws:
        if saw.subkriteria is not None:
            saw_dict = {}
            saw_dict[saw.subkriteria.kriteria.nama_kriteria] = saw.subkriteria.nama_subkriteria
            saw_by_item['subkriterias'].append(saw_dict)