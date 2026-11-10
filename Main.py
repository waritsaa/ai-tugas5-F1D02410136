import json

def load_kb(filename="kb_wifi.json"):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def get_user_inputs(kb):
    semua_jika = set()
    semua_maka = set()
    for r in kb["aturan"]:
        semua_maka.add(r["maka"])
        for kondisi in r["jika"]:
            semua_jika.add(kondisi)

    fakta_tanya = sorted(list(semua_jika - semua_maka))

    print(f"\n{kb['judul']}")
    print("Jawab y/t.")

    memori = set()
    for i, fakta in enumerate(fakta_tanya, 1):
        jawab = input(f"{i}. Apakah {fakta}? (y/t) > ").strip().lower()
        if jawab == 'y':
            memori.add(fakta)

    return memori, fakta_tanya

def forward_chaining(kb, memori):
    aturan_list = kb["aturan"]
    riwayat_alasan = {}
    siklus = 1

    print(f"\nFakta awal: {', '.join(memori) if memori else 'tidak ada'}\n")

    while True:
        cocok = []
        for r in aturan_list:
            if r["maka"] in memori:
                continue

            if r["mode"] == "dan":
                terpenuhi = all(kondisi in memori for kondisi in r["jika"])
            elif r["mode"] == "atau":
                terpenuhi = any(kondisi in memori for kondisi in r["jika"])
            else:
                terpenuhi = False

            if terpenuhi:
                cocok.append(r)

        if not cocok:
            print(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break

        r_eksekusi = cocok[0]
        memori.add(r_eksekusi["maka"])
        riwayat_alasan[r_eksekusi["maka"]] = r_eksekusi

        print(f"Siklus {siklus}: {r_eksekusi['id']} -> {r_eksekusi['maka']}")
        siklus += 1

    return memori, riwayat_alasan

def cetak_alasan(fakta, riwayat_alasan):
    if fakta in riwayat_alasan:
        r = riwayat_alasan[fakta]
        kondisi_str = ", ".join(r["jika"])
        print(f"    {fakta}  <-  {r['id']} ({kondisi_str})")
        for k in r["jika"]:
            cetak_alasan(k, riwayat_alasan)

def main():
    kb = load_kb()
    memori, fakta_tanya = get_user_inputs(kb)

    fakta_awal_user = memori.copy()

    memori, riwayat_alasan = forward_chaining(kb, memori)

    kesimpulan_list = []
    semua_jika = set(k for r in kb["aturan"] for k in r["jika"])
    for f in memori:
        if f not in fakta_awal_user and f not in semua_jika:
            kesimpulan_list.append(f)
    if not kesimpulan_list:
        kesimpulan_list = [f for f in memori if f not in fakta_awal_user]

    print("\nKesimpulan: ", end="")
    if kesimpulan_list:
        print(", ".join(kesimpulan_list))
        print("Alasan:")
        for kess in kesimpulan_list:
            cetak_alasan(kess, riwayat_alasan)
    else:
        print("tidak ada")

    print(f"\nCatatan: {kb['batas']}")

if __name__ == "__main__":
    main()
