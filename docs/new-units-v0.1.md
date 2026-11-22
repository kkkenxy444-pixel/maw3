# MAW3 Android v0.1: kendaraan dan bangunan baru

**Status: prototipe XML lulus pemeriksaan sintaks, belum diuji di dalam game Android.**

Analisis dilakukan dari APK v3.1.12 yang disediakan pengguna secara privat; file game tidak diunggah ke GitHub.

## Temuan yang menentukan

1. `assets/schema.xml` menyimpan 180 definisi `<unit>` dalam `<schema>`.
2. `Land Factory` mempunyai menu `Units` sendiri. Nama unit di daftar `<item Unit="..."/>` harus cocok persis dengan `Name` definisi unit.
3. Menu aktif `<menu>` mempunyai kategori `Engineering`, `Buildings`, `Defense`, dan `Mega Units`. Kategori `Land` berlabel `EditOnly="1"`.
4. Blok `Engr / Bldg / Dfnse / Mega` yang tampak di bawah menu sebenarnya berada di dalam komentar XML, sehingga **tidak aktif**. Jangan menambahkan unit ke situ.
5. `Level` menunjukkan tingkat teknologi pada banyak unit. `<precedences>` memuat syarat khusus. `<classes>` mendefinisikan perilaku, misalnya `Building`, `Turret`, `Ground`, `Commandable`.
6. Menurut catatan modding pengembang PC, `Id="0"` atau Id tanpa nilai boleh dipakai untuk unit tanpa lookup terjemahan. Ini masih memerlukan verifikasi Android.

## Prototipe yang dirancang

| Nama baru | Salin dari | Perubahan utama | Slot menu uji |
| --- | --- | --- | --- |
| Bulwark Tank | Challenger | Cost 320, Attack 65, HP 550, Speed 55, BuildTime 22 | Land Factory -> Challenger |
| Sentinel Cannon | M779 | Cost 650, Attack 50, HP 1300, Range 300, RepeatRate 0.4, PowerUsage 400, BuildTime 41 | Defense -> M779 |
| Longwatch Tower | Outpost | Cost 300, HP 500, ViewRad 700, PowerUsage 150, BuildTime 40 | Buildings -> Outpost |

Ketiganya adalah definisi tambahan (jumlah menjadi 183) dan memakai referensi animasi serta suara asli. **Aslinya tidak dihapus dari schema**, tetapi slot menu diganti untuk menghindari pertambahan tombol saat eksperimen awal. Pembatasan mutator yang berlaku bagi unit dasar juga disalin ke varian baru.

## Pemasangan uji Android

1. Buat cadangan APK asli **dan data simpanan**. Jangan uninstall game utama.
2. Di MT Manager, buka salinan APK; cari `assets/schema.xml`.
3. Ganti isinya dengan hasil generator yang dibuat **secara lokal dari APK milik sendiri** (gunakan nama file persis `schema.xml`).
4. APK yang diedit memerlukan tanda tangan ulang. Android tidak bisa memasang pembaruan dengan penanda tangan berbeda pada package name sama. Siapkan metode uji yang aman sebelum mencoba instalasi.
5. Jika berhasil dipasang, jalankan skirmish **offline**, lihat ketiga menu dan periksa harga, HP, serta jarak serangan/pandangan.
6. Jika gagal, catat error, screenshot/logcat (jika ada), versi Android, dan jangan hapus instalasi normal.

**Belum terbukti:** engine Android menerima `Name` baru, jumlah unit 183, penggunaan ID nol, menu build, ketersediaan ikon, dan kompatibilitas tanda tangan. Target uji pertama adalah menemukan apakah aplikasi membaca penambahan unit ini tanpa crash.

## Repo safety

Jangan unggah APK, `schema.xml` penuh, `data.pak`, sprite, audio, save, atau signing key ke repo publik ini. Hanya dokumentasi, kode orisinal dan instruksi patch lokal.

Referensi resmi komunitas:
- https://steamcommunity.com/app/303860/discussions/0/1333474229086149271/
- https://www.moddb.com/games/machines-at-war-3/forum/thread/modding-notes
