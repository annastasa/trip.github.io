import sqlite3
import os
import platform

# === Konek ke database ===
mydb = sqlite3.connect("pariwisatapbo.db")
mycursor = mydb.cursor()

# === Bersihkan layar & simpan sesi login memakai array ===
bersihkanLayar = lambda: os.system('cls')
arrayAkun = []

bersihkanLayar()

class User:
	def __init__(self, username=None, password=None, nama=None, no_ktp=None, alamat=None, level=None):
		self.username = username
		self.password = password
		self.nama = nama
		self.no_ktp = no_ktp
		self.alamat = alamat
		self.level = level

	def setLogin(self):
		value = (self.username, self.password)

		mycursor.execute("SELECT id_akun, username, nama, no_ktp, alamat, level FROM tb_akun WHERE username = ? AND password = ?", value)
		hasil = mycursor.fetchone()

		bersihkanLayar()

		if(hasil):
			arrayAkun.append(hasil)
			print("Selamat datang")
		else:
			print("Username atau password salah")

		return hasil

	def registrasiAkun(self):
		value = [(self.username, self.password, self.nama, self.no_ktp, self.alamat, self.level)]

		mycursor.executemany("INSERT INTO tb_akun (username, password, nama, no_ktp, alamat, level) VALUES (?, ?, ?, ?, ?, ?)", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil disimpan")

	def tampilkanAkun(self): 
		mycursor.execute("SELECT id_akun, username, nama, no_ktp, alamat, level FROM tb_akun")
		hasil = mycursor.fetchall()

		bersihkanLayar()

		if(len(hasil) == 0):
			print("Tidak ada data")
		else:
			for x in range(0, len(hasil)):
				print(f"=== ID: {hasil[x][0]} ===")
				print(f"Username: {hasil[x][1]}")
				print(f"Nama: {hasil[x][2]}")
				print(f"No KTP: {hasil[x][3]}")
				print(f"Alamat: {hasil[x][4]}")
				print(f"Level: {hasil[x][5]}")

		return hasil

	def editAkun(self, id_akun):
		value = (self.username, self.password, self.nama, self.no_ktp, self.alamat, self.level, id_akun)

		mycursor.execute("UPDATE tb_akun SET username = ?, password = ?, nama = ?, no_ktp = ?, alamat = ?, level = ? where id_akun = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil diubah")

	def hapusAkun(self, id_akun):
		value = (id_akun,)

		mycursor.execute("DELETE FROM tb_akun where id_akun = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil dihapus")

class ObjekPariwisata:
	def __init__(self, nama_tempat=None, desk_tempat=None):
		self.nama_tempat = nama_tempat
		self.desk_tempat = desk_tempat

	def tambahTempat(self):
		value = [(self.nama_tempat, self.desk_tempat)]

		mycursor.executemany("INSERT INTO tb_tempat (nama_tempat, desk_tempat) VALUES (?, ?)", value)
		mydb.commit()
		
		bersihkanLayar()
		print("Data berhasil disimpan")

	def tampilkanTempat(self): 
		mycursor.execute("SELECT * FROM tb_tempat")
		hasil = mycursor.fetchall()

		bersihkanLayar()

		if(len(hasil) == 0):
			print("Tidak ada data")
		else:
			for x in range(0, len(hasil)):
				print(f"=== ID: {hasil[x][0]} ===")
				print(f"Nama Tempat: {hasil[x][1]}")
				print(f"Deskripsi: {hasil[x][2]}")

		return hasil

	def tampilkanSatuTempat(self, id_tempat):
		value = (id_tempat,)

		mycursor.execute("SELECT * FROM tb_tempat WHERE id_tempat = ?", value)
		return mycursor.fetchone()

	def editTempat(self, id_tempat):
		value = (self.nama_tempat, self.desk_tempat, id_tempat)

		mycursor.execute("UPDATE tb_tempat SET nama_tempat = ?, desk_tempat = ? where id_tempat = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil diubah")

	def hapusTempat(self, id_tempat):
		value = (id_tempat,)

		mycursor.execute("DELETE FROM tb_tempat where id_tempat = ?", value)
		mydb.commit()
		
		bersihkanLayar()
		print("Data berhasil dihapus")

class PaketPariwisata(ObjekPariwisata):
	def __init__(self, nama_paket=None, harga=None):
		self.nama_paket = nama_paket
		self.harga = harga

	def tambahPaket(self, id_tempat): 
		value = [(self.nama_paket, id_tempat, self.harga)]

		mycursor.executemany("INSERT INTO tb_paket (nama_paket, id_tempat, harga) VALUES (?, ?, ?)", value)
		mydb.commit()
		
		bersihkanLayar()
		print("Data berhasil disimpan")

	def tampilkanPaket(self):
		mycursor.execute("SELECT paket.id_paket, paket.nama_paket, tempat.nama_tempat, tempat.desk_tempat, paket.harga FROM tb_paket paket INNER JOIN tb_tempat tempat using(id_tempat)")
		hasil = mycursor.fetchall()

		bersihkanLayar()

		if(len(hasil) == 0):
			print("Tidak ada data")
		else:
			for x in range(0, len(hasil)):
				print(f"=== ID: {hasil[x][0]} ===")
				print(f"Nama Paket: {hasil[x][1]}")
				print(f"Nama Tempat: {hasil[x][2]}")
				print(f"Deskripsi Tempat: {hasil[x][3]}")
				print(f"Harga: {hasil[x][4]}")

		return hasil

	def editPaket(self, id_tempat, id_paket):
		value = (self.nama_paket, id_tempat, self.harga, id_paket)

		mycursor.execute("UPDATE tb_paket SET nama_paket = ?, id_tempat = ?, harga = ? where id_paket = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil diubah")

	def hapusPaket(self, id_paket):
		value = (id_paket,)

		mycursor.execute("DELETE FROM tb_paket where id_paket = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Data berhasil dihapus")

class Transaksi(PaketPariwisata):
	def __init__(self, id_paket=None, id_akun=None):
		self.id_paket = id_paket
		self.id_akun = id_akun

	def buatTransaksi(self):
		value = [(self.id_paket, self.id_akun, "0")]

		mycursor.executemany("INSERT INTO tb_transaksi (id_paket, id_akun, status_bayar) VALUES (?, ?, ?)", value)
		mydb.commit()
		
		bersihkanLayar()
		print("Pesanan berhasil dibuat")

	def bayarTransaksi(self, id_transaksi):
		value = ("1", id_transaksi)

		mycursor.execute("UPDATE tb_transaksi SET status_bayar = ? WHERE id_transaksi = ?", value)
		mydb.commit()

		bersihkanLayar()
		print("Transaksi telah dibayar")

	def lihatRiwayat(self):
		mycursor.execute("SELECT transaksi.id_transaksi, akun.nama, paket.nama_paket, paket.harga, tempat.nama_tempat, tempat.desk_tempat, transaksi.status_bayar FROM tb_transaksi transaksi INNER JOIN tb_akun akun using(id_akun) INNER JOIN tb_paket paket using(id_paket) INNER JOIN tb_tempat tempat using(id_tempat)")
		hasil = mycursor.fetchall()

		bersihkanLayar()

		if(len(hasil) == 0):
			print("Tidak ada data")
		else:
			for x in range(0, len(hasil)):
				print(f"=== ID: {hasil[x][0]} ===")
				print(f"Pemesan: {hasil[x][1]}")
				print(f"Nama Paket: {hasil[x][2]}")
				print(f"Harga: Rp {hasil[x][3]}")
				print(f"Tempat: {hasil[x][4]}")
				print(f"Deskripsi: {hasil[x][5]}")

				if(hasil[x][6] == "1"):
					pesan = "Sudah Bayar"
				else:
					pesan = "Belum Bayar"

				print(f"Status Bayar: {pesan}")

		return hasil

	def lihatSatuRiwayat(self, id_transaksi):
		value = (id_transaksi,)

		mycursor.execute("SELECT transaksi.id_transaksi, akun.nama, paket.nama_paket, paket.harga, tempat.nama_tempat, tempat.desk_tempat, transaksi.status_bayar FROM tb_transaksi transaksi INNER JOIN tb_akun akun using(id_akun) INNER JOIN tb_paket paket using(id_paket) INNER JOIN tb_tempat tempat using(id_tempat) WHERE id_transaksi = ?", value)
		return mycursor.fetchone()

	def lihatTransaksiUser(self, id_akun):
		value = (id_akun,)

		mycursor.execute("SELECT transaksi.id_transaksi, paket.nama_paket, paket.harga, tempat.nama_tempat, tempat.desk_tempat, transaksi.status_bayar FROM tb_transaksi transaksi INNER JOIN tb_akun akun using(id_akun) INNER JOIN tb_paket paket using(id_paket) INNER JOIN tb_tempat tempat using(id_tempat) WHERE id_akun = ?", value)
		hasil = mycursor.fetchall()

		bersihkanLayar()

		if(len(hasil) == 0):
			print("Tidak ada data")
		else:
			for x in range(0, len(hasil)):
				print(f"=== ID: {hasil[x][0]} ===")
				print(f"Nama Paket: {hasil[x][1]}")
				print(f"Harga: Rp {hasil[x][2]}")
				print(f"Tempat: {hasil[x][3]}")
				print(f"Deskripsi: {hasil[x][4]}")

				if(hasil[x][5] == "1"):
					pesan = "Sudah Bayar"
				else:
					pesan = "Belum Bayar"

				print(f"Status Bayar: {pesan}")

		return hasil

while True:
	if(len(arrayAkun) == 0):
		print("1. Login")
		print("2. Buat Akun")
		menu = int(input("Pilih menu: "))

		bersihkanLayar()

		if(menu == 1):
			username = input("Input username: ")
			password = input("Input password: ")

			login = User(username, password).setLogin()
		else:
			username = input("Input username: ")
			password = input("Input password: ")
			nama = input("Input nama: ")
			no_ktp = input("Input no_ktp: ")
			alamat = input("Input alamat: ")
			level = "Customer"

			register = User(username, password, nama, no_ktp, alamat, level).registrasiAkun()
	else:
		if(arrayAkun[0][5] == "Admin"):
			print("1. Edit Akun")
			print("2. Manage Akun")
			print("3. Objek Pariwisata")
			print("4. Paket Pariwisata")
			print("5. Riwayat Transaksi")
			print("6. Logout")
			menu = int(input("Pilih menu: "))

			bersihkanLayar()

			if(menu == 1):
				username = input("Input username: ")
				password = input("Input password: ")
				nama = input("Input nama: ")
				no_ktp = input("Input no_ktp: ")
				alamat = input("Input alamat: ")
				level = "Admin"

				edit = User(username, password, nama, no_ktp, alamat, level).editAkun(arrayAkun[0][0])
				arrayAkun = []

				print("Berhasil mengubah info akun. Silahkan login kembali")
			elif(menu == 2):
				print("1. Tambah Akun")
				print("2. Tampilkan Daftar Akun")
				print("3. Edit Akun")
				print("4. Hapus Akun")
				menu2 = int(input("Pilih menu: "))
				
				if(menu2 == 1):
					username = input("Input username: ")
					password = input("Input password: ")
					nama = input("Input nama: ")
					no_ktp = input("Input no_ktp: ")
					alamat = input("Input alamat: ")
					level = input("Input level (Admin/Customer): ").capitalize()

					register = User(username, password, nama, no_ktp, alamat, level).registrasiAkun()
				elif(menu2 == 2):
					User().tampilkanAkun()
				elif(menu2 == 3):
					User().tampilkanAkun()

					id_akun = input("Pilih ID yang ingin diubah: ")
					username = input("Input username: ")
					password = input("Input password: ")
					nama = input("Input nama: ")
					no_ktp = input("Input no_ktp: ")
					alamat = input("Input alamat: ")
					level = input("Input level (Admin/Customer): ").capitalize()

					edit = User(username, password, nama, no_ktp, alamat, level).editAkun(id_akun)
				elif(menu2 == 4):
					User().tampilkanAkun()

					id_akun = input("Pilih ID yang ingin dihapus: ")
					edit = User().hapusAkun(id_akun)
				else:
					bersihkanLayar()
					print("Menu tidak valid")
			elif(menu == 3):
				print("1. Tambah Tempat")
				print("2. Tampilkan Tempat")
				print("3. Edit Tempat")
				print("4. Hapus Tempat")
				menu2 = int(input("Pilih menu: "))

				bersihkanLayar()
				
				if(menu2 == 1):	
					nama_tempat = input("Input nama tempat: ")
					desk_tempat = input("Input deskripsi tempat: ")

					tambah = ObjekPariwisata(nama_tempat, desk_tempat).tambahTempat()
				elif(menu2 == 2):
					ObjekPariwisata().tampilkanTempat()
				elif(menu2 == 3):
					ObjekPariwisata().tampilkanTempat()

					id_tempat = input("Pilih ID yang ingin diubah: ")
					nama_tempat = input("Input nama tempat: ")
					desk_tempat = input("Input deskripsi tempat: ")

					edit = ObjekPariwisata(nama_tempat, desk_tempat).editTempat(id_tempat)
				elif(menu2 == 4):
					ObjekPariwisata().tampilkanTempat()

					id_tempat = input("Pilih ID yang ingin dihapus: ")
					edit = ObjekPariwisata().hapusTempat(id_tempat)
				else:
					bersihkanLayar()
					print("Menu tidak valid")
			elif(menu == 4):
				print("1. Tambah Paket")
				print("2. Tampilkan Paket")
				print("3. Edit Paket")
				print("4. Hapus Paket")
				menu2 = int(input("Pilih menu: "))

				bersihkanLayar()
				
				if(menu2 == 1):
					nama_paket = input("Input nama paket: ")
					harga = input("Input harga: ")

					PaketPariwisata().tampilkanTempat()
					id_tempat = input("Input ID tempat: ")

					tambah = PaketPariwisata(nama_paket, harga).tambahPaket(id_tempat)
				elif(menu2 == 2):
					PaketPariwisata().tampilkanPaket()
				elif(menu2 == 3):
					PaketPariwisata().tampilkanPaket()

					id_paket = input("Pilih ID yang ingin diubah: ")
					nama_paket = input("Input nama paket: ")
					harga = input("Input harga: ")

					PaketPariwisata().tampilkanTempat()
					id_tempat = input("Pilih ID tempat: ")

					edit = PaketPariwisata(nama_paket, harga).editPaket(id_tempat, id_paket)
				elif(menu2 == 4):
					PaketPariwisata().tampilkanPaket()
					id_paket = input("Pilih ID yang ingin dihapus: ")

					edit = PaketPariwisata().hapusPaket(id_paket)
				else:
					bersihkanLayar()
					print("Menu tidak valid")
			elif(menu == 5):
				Transaksi().lihatRiwayat()
				menu2 = int(input("1. Proses Pembayaran\nInputkan selain 1 untuk keluar dari menu: "))

				bersihkanLayar()

				if(menu2 == 1):
					Transaksi().lihatRiwayat()
					id_transaksi = input("Masukkan ID yang bersangkutan: ")
					hasil = Transaksi().lihatSatuRiwayat(id_transaksi)

					if(hasil):
						transaksi = input(f"Apakah transaksi dengan ID {hasil[0]} telah dibayar? (Inputkan 0 (Belum) atau 1 (Sudah)): ")	
						
						if(transaksi):
							Transaksi().bayarTransaksi(id_transaksi)
					else:
						print("Tidak ada transaksi yang dimaksud")
			elif(menu == 6):
				arrayAkun = []
				print("Silahkan login kembali")
			else:
				bersihkanLayar()
				print("Menu tidak valid")
		else:
			print("1. Edit Akun")
			print("2. Pesan Paket")
			print("3. Daftar Transaksi")
			print("4. Logout")
			menu = int(input("Pilih menu: "))

			bersihkanLayar()

			if(menu == 1):
				username = input("Input username: ")
				password = input("Input password: ")
				nama = input("Input nama: ")
				no_ktp = input("Input no_ktp: ")
				alamat = input("Input alamat: ")
				level = "Customer"

				edit = User(username, password, nama, no_ktp, alamat, level).editAkun(arrayAkun[0][0])
				arrayAkun = []
				print("Silahkan login kembali")
			elif(menu == 2):
				hasil = Transaksi().tampilkanPaket()

				if(hasil):
					id_paket = input("Pilih ID paket yang diinginkan: ")

					Transaksi(id_paket, arrayAkun[0][0]).buatTransaksi()
			elif(menu == 3):
				Transaksi().lihatTransaksiUser(arrayAkun[0][0])
			else:
				arrayAkun = []
				print("Silahkan login kembali")