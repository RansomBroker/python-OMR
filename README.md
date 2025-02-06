## Petunjuk penggunaan OMR

#### Requirenment

1. opencv 4.0
2. flask
3. matplotlib
4. imutils
5. python3.11.11


##### Instalasi package dan menjalankan program 
Install package dengan perintah `conda create --name omr-test --file requirenments.txt` setelah semua package terinstall maka jalankan perintah, lalu install `conda install conda-forge::imutils` untuk menginstall package imutils 
`python app.py` untuk menjalankan server flask adapun cara menggunakan menggunakan postman atau curl dengan contoh 

``
curl --location 'http://127.0.0.1:5000/api/upload' \
--form 'image=@"/C:/Users/yadis/Pictures/lembar valid1.jpg"'
``

adapun terdapat penyesuian (optional) dalam file `routes.py` yang mana pada function `scan_answer` silahkan baca penjelasan program untuk keterangan lebih lanjut, tapi pada starting program ini, seharunya tinggal dijalankan saja tanpa melakukan seting lagi.

##### Penjelasan program
struktur program terdiri dari 2 bagian, yaitu bagian flask, dan bagian utama (core)
adapaun file flask terdiri dari 
1. app.py : bertugas sebagai run point 
2. routes.py : berisikan routes

adapun untuk struktur OMR terdiri dari 3 file utama
1. main.py : Berisikan fungsi pipeline dari deteksi OMR
2. answer_maping.py : Fungsi untuk melakukan pemetaan seluruh jawaban adapaun cara penggunaanya
   1. jalankan perintah `python answer_maping.py` lalu klik lingkaran yang menjadi jawaban, lalu tekan enter untuk memulai baris baru misalnya anda melakukan pemetaan untuk no 1, setelah semua pemetaan selesai maka tekan enter untuk melanjutkan ke nomor selanjutnya, adapun menekan tombol `esc` untuk menyimpan jawaban yang telah dipetakan menjadi json, yang akan digunakan di sebagai argument di function `scan_answer`
3. follder utils : yang berisikan kumpulan function untuk melakukan prosesing gambar dsb.