# Greedy Wi-Fi Placement

> Makalah IF2211 Strategi Algoritma

<p align="center">
  <img src="doc/preview.png" width="60%"/>
</p>

Program simulasi penempatan Access Point Wi-Fi menggunakan algoritma Greedy Set Cover pada denah dua dimensi.

Program ini membaca skenario dari file JSON, menghitung cakupan setiap kandidat Access Point, memilih kandidat menggunakan strategi greedy, lalu menghasilkan visualisasi denah awal dan hasil penempatan Access Point.

## Fitur

- Membaca data denah dari file JSON.
- Menghitung cakupan pengguna berdasarkan jarak Euclidean.
- Menjalankan algoritma Greedy Set Cover.
- Menampilkan log iterasi pemilihan Access Point.
- Menghasilkan gambar denah awal dan hasil penempatan.
- Mendukung eksekusi melalui PowerShell dan WSL/Linux.

## Struktur Proyek

```text
greedy-wifi-placement/
├── app.py
├── coverage.py
├── greedy.py
├── visualization.py
├── requirements.txt
├── scenarios/
│   └── denah.json
├── output/
│   └── .gitkeep
└── README.md
```

Keterangan file utama:

| File                   | Fungsi                                                                             |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `app.py`               | Entry point program, membaca skenario, menjalankan algoritma, dan menyimpan output |
| `coverage.py`          | Menghitung cakupan kandidat Access Point terhadap pengguna                         |
| `greedy.py`            | Implementasi algoritma Greedy Set Cover                                            |
| `visualization.py`     | Membuat visualisasi denah dan hasil algoritma                                      |
| `scenarios/denah.json` | Contoh data denah                                                                  |
| `output/`              | Folder hasil gambar yang dihasilkan program                                        |

## Requirements

Program membutuhkan Python 3 dan pustaka berikut:

```text
matplotlib
```

Dependensi tersedia di file:

```text
requirements.txt
```

## Cara Menjalankan dengan PowerShell

Masuk ke folder proyek:

```powershell
cd "C:\path\to\greedy-wifi-placement"
```

Buat virtual environment:

```powershell
python -m venv .venv
```

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependensi:

```powershell
pip install -r requirements.txt
```

Jalankan program:

```powershell
python app.py --scenario scenarios/denah.json
```

Untuk menampilkan jendela visualisasi:

```powershell
python app.py --scenario scenarios/denah.json --show
```

## Cara Menjalankan dengan WSL/Linux

Masuk ke folder proyek:

```bash
cd ~/path/to/greedy-wifi-placement
```

Buat virtual environment:

```bash
python3 -m venv .venv
```

Aktifkan virtual environment:

```bash
source .venv/bin/activate
```

Install dependensi:

```bash
pip install -r requirements.txt
```

Jalankan program:

```bash
python3 app.py --scenario scenarios/denah.json
```

Untuk menampilkan jendela visualisasi:

```bash
python3 app.py --scenario scenarios/denah.json --show
```

Jika `venv` belum tersedia di WSL/Linux, install terlebih dahulu:

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
```

## Argumen Program

Program menerima beberapa argumen:

| Argumen        | Keterangan                              |
| -------------- | --------------------------------------- |
| `--scenario`   | Path file JSON skenario                 |
| `--output-dir` | Folder untuk menyimpan hasil gambar     |
| `--show`       | Menampilkan visualisasi secara langsung |

Contoh:

```bash
python3 app.py \
  --scenario scenarios/denah.json \
  --output-dir output \
  --show
```

## Format Skenario

Skenario disimpan dalam format JSON. Contoh struktur data:

```json
{
  "name": "Denah contoh",
  "width": 12,
  "height": 8,
  "radius": 3.0,
  "users": {
    "U1": [1.2, 6.6],
    "U2": [4.6, 6.1]
  },
  "candidates": {
    "A1": [3.0, 6.0],
    "A2": [9.0, 6.0]
  },
  "walls": [
    [
      [0.0, 4.8],
      [12.0, 4.8]
    ]
  ],
  "rooms": [
    {
      "name": "Ruang Kerja",
      "x": 0.0,
      "y": 4.8,
      "width": 7.0,
      "height": 3.2
    }
  ]
}
```

Keterangan:

| Field        | Keterangan                                           |
| ------------ | ---------------------------------------------------- |
| `width`      | Lebar denah                                          |
| `height`     | Tinggi denah                                         |
| `radius`     | Radius cakupan setiap Access Point                   |
| `users`      | Daftar pengguna dan koordinatnya                     |
| `candidates` | Daftar kandidat lokasi Access Point dan koordinatnya |
| `walls`      | Garis dinding untuk visualisasi                      |
| `rooms`      | Informasi ruangan untuk visualisasi                  |

Catatan: dinding dan ruangan hanya digunakan untuk visualisasi. Perhitungan cakupan hanya menggunakan koordinat pengguna, koordinat kandidat Access Point, dan radius.

## Output Program

Program menghasilkan file gambar di folder `output/`:

```text
output/denah.png
output/hasil.png
```

Keterangan:

| File        | Isi                                                             |
| ----------- | --------------------------------------------------------------- |
| `denah.png` | Denah awal berisi pengguna dan kandidat lokasi Access Point     |
| `hasil.png` | Denah hasil pemilihan Access Point menggunakan Greedy Set Cover |

Program juga menampilkan ringkasan di terminal, misalnya:

```text
=== Log Iterasi Greedy Set Cover ===
Iterasi 1: pilih A4; pengguna baru tercakup = U10, U4, U6, U9.
Iterasi 2: pilih A1; pengguna baru tercakup = U1, U2, U5.

=== Ringkasan ===
Access Point terpilih : A4, A1, A3, A2
Jumlah Access Point   : 4
Pengguna tercakup     : 10/10
Persentase            : 100.00%
Jumlah iterasi        : 4
Waktu eksekusi        : 0.1234 ms
```

## Ringkasan Algoritma

Setiap kandidat Access Point merepresentasikan himpunan pengguna yang berada dalam radius cakupannya. Program memilih kandidat secara greedy dengan aturan:

1. Hitung pengguna yang belum tercakup.
2. Pilih kandidat Access Point yang mencakup pengguna belum tercakup paling banyak.
3. Tandai pengguna tersebut sebagai tercakup.
4. Ulangi hingga semua pengguna tercakup atau tidak ada kandidat yang memberi cakupan tambahan.

Jika terdapat beberapa kandidat dengan nilai cakupan tambahan yang sama, program memilih kandidat dengan ID terkecil secara leksikografis agar hasil eksekusi konsisten.

## Batasan

- Setiap Access Point memiliki radius cakupan yang sama.
- Dinding belum memengaruhi kekuatan sinyal.
- Interferensi, kapasitas perangkat, kanal frekuensi, dan pelemahan sinyal belum dimodelkan.
- Model digunakan untuk simulasi algoritmik, bukan perencanaan jaringan Wi-Fi nyata.

## Lisensi

Proyek ini dibuat untuk keperluan makalah IF2211 Strategi Algoritma.
