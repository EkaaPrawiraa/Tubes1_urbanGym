# Tubes1-STIMA-Etimo Diamonds

## Kelompok urbanGym
```
Mohammad Nugraha Eka Prawira 13522001
Ahmad Farid Mudrika          13522008
Muhammad Yusuf Rafi          13522009
```
## Deskripsi Implementasi Greedy
```
Pada permainan Diamond, banyak gamestate yang bisa kita ketahui dengan mudah seperti posisi pemain, posisi lawan, inventori pemain, inventori lawan, dan lain-lain.
Tentu hal tersebut memudahkan program agar berjalan dengan efektif.
Pemain dapat mendeteksi keseluruhan map sehingga pemain dapat merencanakan pilihan paling optimal.
Semua objek pada board dapat dilihat pada atribut game_object dari objek board.
Hal ini mengakibatkan semua pencarian objek, baik yang paling sederhana hingga yang paling rumit memiliki kompleksitas waktu tetap mxn, dengan m adalah jumlah baris di kotak dan n jumlah kolom. Dalam hal ini, kita dapat menganggapnya O(1).
Pada strategi Greedy bot lawan, kita melakukan pencarian posisi bot lawan secara iteratif, lalu menghitung jarak tiap bot lain dari bot kita, mengurutkannya, dan menjadikan bot terdekat sebagai tujuan.
Karena ada pengurutan di dalamnya, kompleksitas waktunya O(n log n).
Pada strategi Greedy diamond, kita melakukan pencarian posisi semua diamond di board.
Meskipun terdapat method diamonds pada board, method ini tetap melakukan pencarian iteratif, sehingga kompleksitas waktunya sama dengan strategi lain. Setelah mendapat list diamond di board dan posisinya, kita menghitung jarak tiap diamond dari kita, lalu mengurutkannya dari yang terkecil. Kita lalu memilih diamond terdekat sebagai tujuan kita.
```

# Requirements

### 1) Python
`https://www.python.org/downloads`
### 2) Clone repository game-engine dan jalankan requirementsnya
`https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0`
### 3) Clone repository ini
### 4) Buka terminal dengan repository project
`cd tubes1-IF2110-bot-starter-pack-1.0.1`
### 5) Install dependencies menggunakan pip
`pip install -r requirements.txt`
### 6) Run
```
python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
```

