"""
DOGHOTEL
Pada tahap ini melakukan dictionary dalam list untuk sample customers
"""

customers = [
    {"ID": "001", "owner": "Liam", "pet": "Mylo", "size": "M", "nights": 5, "special": "Behavioural Therapy", "addon": "Tidak ada tambahan"},
    {"ID": "002", "owner": "Liam", "pet": "Blu", "size": "XL", "nights": 5, "special": "Tidak ada", "addon": "Grooming"},
    {"ID": "003", "owner": "Liam", "pet": "Naomi", "size": "XL", "nights": 5, "special": "Skincare Treatment", "addon": "Tidak ada tambahan"},
    {"ID": "004", "owner": "Debbie", "pet": "Mia", "size": "L", "nights": 10, "special": "Tidak ada", "addon": "Tidak ada tambahan"},
]

pet_name_set = set(c["pet"] for c in customers)
next_id = 5

"""
Tahap ini menginput harga hotel per malam
berdasarkan size doggy 
"""
base_price_S = 200_000
lodging_prices = {
    "S": base_price_S,
    "M": base_price_S + 70_000,
    "L": base_price_S + 140_000,
    "XL": base_price_S + 210_000
}

"""
Tahap ini membuat pricelist untuk kebutuhan khusus & add-on
dari services yang ditawarkan
"""
special_prices = {"Dermatologi": 200_000, "Behavioural Issues": 100_000, "Flea and Tick": 150_000}
addon_prices = {"Grooming": 150_000, "Scaling Gigi": 120_000}
treatment_options = {
    "Dermatologi": ["Skincare Treatment", "Tidak"],
    "Behavioural Issues": ["Behavioural Therapy", "Tidak"],
    "Flea and Tick": ["Special Grooming", "Tidak"],
}

def input_choice(prompt, valid):
    """
    Berikutnya, membuat fungsi validasi input pilihan, yang dimana program
      akan meminta input terus hingga user memasukkan pilihan yang disuguhkan
    """
    while True:
        x = input(prompt).strip()
        if x in valid:
            return x
        print(f"Pilihan tidak valid, silakan masukkan salah satu dari: {', '.join(valid)}")

def input_int(prompt):
    """
    Selanjutnya membuat fungsi untuk menerima input angka
    dan terus meminta hingga user memasukkan angka yang disodorkan
    """
    while True:
        v = input(prompt).strip()
        if v.isdigit():
            return int(v)
        print("Silakan masukkan angka yang valid.")

def input_yesno(prompt):
    """
    Disini fungsi untuk menerima pilihan ya/tidak, jika True
    maka akan dikembalikan dan False jika tidak (kembali ke tahap sebelumnya)
    """
    return input_choice(prompt + " (ya/tidak): ", ["ya", "tidak"]) == "ya"

def menu_1_services():
    """
    Disini membuat MENU 1:
    Showing the Dog Hotel Services, yang mencakup
    harga kamar per ukuran (dari S hinggal XL), 
    menampilkan daftar special needs dog, dan 
    daftar add-on services
    """
    print("\n-- DAFTAR LAYANAN PET HOTEL --")
    print("Penginapan (per malam):")
    for sz, price in lodging_prices.items():
        print(f" {sz:<2} → {price:,} IDR")
    print("\nKategori Kebutuhan Khusus (Special Needs):")
    for cat, price in special_prices.items():
        print(f" {cat:<17}→ {price:,} IDR")
    print("\nAdd-on (untuk hewan tanpa kebutuhan khusus):")
    for name, price in addon_prices.items():
        print(f" {name:<13}→ {price:,} IDR")
    print()

def menu_2_register():
    """
    Lalu lanjut ke MENU 2: Registrasi Pelanggan Baru.
    Yang berupa input data pemilik dan hewan, konfirmasi data kalau benar lanjut
    payment, kalau tidak ulang dari awal
    dan validasi uang berupa memberi tahu uang kurang berapa dan dapat
    melanjutkan pembayaran berdasarkan value uang yang kurang
    serta saving data to customer list
    """
    global next_id
    print("\n-- REGISTRASI PELANGGAN BARU --")
    owner = input("Nama pemilik           : ").strip()
    session = []
    temp_pet_set = set()

    while True:
        while True:
            pet = input("Nama hewan             : ").strip()
            if pet in pet_name_set or pet in temp_pet_set:
                print("Nama hewan sudah digunakan, silakan isi nama lengkap.")
            else:
                break

        weight = input_int("Berat hewan dalam kg   : ")
        size = "S" if weight < 5 else "M" if weight < 10 else "L" if weight < 15 else "XL"
        nights = input_int("Jumlah malam           : ")

        if input_yesno("Apakah ada kebutuhan khusus?"):
            sp = input_choice("Pilih special needs: 1)Dermatologi 2)Behavioural Issues 3)Flea and Tick: ", ["1", "2", "3"])
            category = {"1": "Dermatologi", "2": "Behavioural Issues", "3": "Flea and Tick"}[sp]
            opts = treatment_options[category]
            opt = input_choice(f"Rekomendasi {category}: 1){opts[0]} 2){opts[1]}: ", ["1", "2"])
            special = opts[0] if opt == "1" else "Tidak ada"
            addon = "Tidak ada tambahan"
        else:
            special = "Tidak ada"
            rec = input_choice("Rekomendasi: 1)Grooming 2)Scaling Gigi 3)Tidak ada: ", ["1", "2", "3"])
            addon = {"1": "Grooming", "2": "Scaling Gigi", "3": "Tidak ada tambahan"}[rec]

        base = lodging_prices[size] * nights
        extra = special_prices.get(category if special != "Tidak ada" else "", 0)
        addon_ = addon_prices.get(addon, 0)
        cost = base + extra + addon_

        session.append({
            "pet": pet,
            "size": size,
            "nights": nights,
            "special": special,
            "addon": addon,
            "cost": cost
        })
        temp_pet_set.add(pet)

        if not input_yesno("Tambah hewan lain?"):
            break

    while True:
        print("\n-- Ringkasan Sebelum Pembayaran --")
        total_all = 0
        for idx, p in enumerate(session, 1):
            print(f"{idx}. {p['pet']} | Size:{p['size']} | Malam:{p['nights']} | Special Needs:{p['special']} | Add-on:{p['addon']} | Biaya:{p['cost']:,}")
            total_all += p['cost']
        print(f"Total keseluruhan: {total_all:,} IDR")

        correct = input_choice("Apakah data sudah benar? 1)Ya, Proses 2)Tidak: ", ["1", "2"])
        if correct == "1":
            pet_name_set.update(temp_pet_set)
            break
        else:
            print("Silakan ulangi registrasi.\n")
            return

    payment = 0
    while payment < total_all:
        add = input_int(f"Pembayaran (sisa {total_all - payment:,} IDR): ")
        payment += add
        if payment < total_all:
            print(f"Uang Anda masih kurang {total_all - payment:,} IDR.")

    print(f"Kembalian              : {payment - total_all:,} IDR")
    print("Pembayaran Anda Berhasil °")
    print("Registrasi dan Pembayaran Berhasil ⋆˚🐾˖.\n")

    for p in session:
        cid = f"{next_id:03d}"
        customers.append({
            "ID": cid,
            "owner": owner,
            "pet": p["pet"],
            "size": p["size"],
            "nights": p["nights"],
            "special": p["special"],
            "addon": p["addon"]
        })
        next_id += 1

def menu_3_view_customers():
    """
    Berikutnya ke MENU 3: Menampilkan data semua pelanggan
    Untuk menampilkan customer yang registered dari
    ID, pet owner's name, pet's name, size, nights stay, special needs,
    dan add-on
    """
    if not customers:
        print("\nBelum ada pelanggan terdaftar.\n")
        return
    print("\n-- DAFTAR PELANGGAN --")
    print("Idx | ID   | Pemilik   | Hewan      | Size | Malam | Special Needs        | Add-on")
    print("-"*85)
    for idx, r in enumerate(customers):
        print(f"{idx:<3}| {r['ID']:<4}| {r['owner']:<9}| {r['pet']:<10}| {r['size']:<4}| {r['nights']:^6}| {r['special']:<22}| {r['addon']}")
    print()

def menu_4_search_pet():
    """
    Membuat MENU 4: Mencari hewan peliharaan
    Dimana user dapat mencari berdasarkan pet's name.
    Dapat konfirmasi jika ada atau tidaknya hewan di hotel ini.
    """
    term = input("Masukkan nama hewan yang dicari: ").strip().lower()
    found = any(term in r["pet"].lower() for r in customers)
    if found:
        print("Hewan terdaftar di sini!\n")
    else:
        print("Maaf, tidak ditemukan :( \n")

def menu_5_delete_customer():
    """
    Membuat MENU  5: Menghapus data pelanggan.

    Menampilkan daftar pelanggan,
    meminta user memilih index pelanggan yang akan dihapus,
    melakukan konfirmasi ulang sebelum dihapus,
    lalu data dihapus jika disetujui
    """
    if not customers:
        print("\nTidak ada data untuk dihapus.\n")
        return

    while True:
        menu_3_view_customers()
        idx = input_choice("Index pelanggan yang akan dihapus: ", [str(i) for i in range(len(customers))])
        idx = int(idx)
        rem = customers[idx]

        print(f"\nData yang akan dihapus: {rem['pet']} | Pemilik: {rem['owner']} | ID: {rem['ID']}")
        confirm = input_choice("Apakah data yang akan dihapus sudah benar? (ya/tidak): ", ["ya", "tidak"])
        if confirm == "ya":
            customers.pop(idx)
            pet_name_set.remove(rem["pet"])
            print("Data berhasil dihapus.\n")
            break
        else:
            print("Silakan pilih index lain.\n")
"""Terakhir, membuat main loop"""
while True:
    print("=== SELAMAT DATANG DI DOGHOTEL ===")
    print("1. Layanan Kami")
    print("2. Registrasi Pelanggan")
    print("3. Tampilkan Pelanggan")
    print("4. Cari Hewan")
    print("5. Hapus Pelanggan")
    print("6. Keluar Program")
    cmd = input_choice("Pilih menu (1-6): ", ["1", "2", "3", "4", "5", "6"])

    if cmd == "1":
        menu_1_services()
    elif cmd == "2":
        menu_2_register()
    elif cmd == "3":
        menu_3_view_customers()
    elif cmd == "4":
        menu_4_search_pet()
    elif cmd == "5":
        menu_5_delete_customer()
    elif cmd == "6":
        print("Program selesai. Terima kasih!")
        break
    print()
