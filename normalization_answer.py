import json

# Membaca file JSON
with open('answer_position.json', 'r') as file:
    data = json.load(file)

# Fungsi untuk menghilangkan duplikat dalam setiap sublist tanpa mengubah urutan
def remove_duplicates(sublist):
    seen = set()
    unique_sublist = []
    for item in sublist:
        # Mengubah item menjadi tuple agar bisa disimpan dalam set
        item_tuple = tuple(item)
        if item_tuple not in seen:
            unique_sublist.append(item)
            seen.add(item_tuple)
    return unique_sublist

# Menghilangkan duplikat dalam setiap sublist
data_unique = [remove_duplicates(sublist) for sublist in data]

# Menampilkan data tanpa duplikat
print(data_unique)

# Menyimpan hasil ke file JSON baru
with open('answer_position_normalize.json', 'w') as file:
    json.dump(data_unique, file, indent=4)
