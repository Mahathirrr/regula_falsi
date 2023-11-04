from tkinter import *
from tkinter import messagebox


# Fungsi untuk menghitung nilai persamaan
def f(x, p):
    return eval(p)


# Fungsi untuk menampilkan hasil perhitungan dalam bentuk tabel
def print_results(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            entry = Entry(f4, width=10, font=("Helvetica Neue", 12), justify="center")
            entry.grid(row=i, column=j)
            entry.insert(0, data[i][j])


# Fungsi untuk menampilkan kesimpulan perhitungan
def conclusion(iteration, error, root):
    result = "Kesimpulan\n\n"
    result += f"Setelah {iteration} iterasi, nilai ERROR lebih kecil dari {error}.\n"
    result += f"Maka iterasi dihentikan dan diperoleh solusi persamaan non-linier yang diinginkan:\n"
    result += f"APROKSIMASI AKAR = {root:.6f}"
    messagebox.showinfo("Kesimpulan", result)


# Fungsi untuk memeriksa syarat terpenuhi untuk iterasi
def check_condition():
    persamaan = str(ent_persamaan.get())
    batas_bawah = float(ent_batas_bawah.get())
    batas_atas = float(ent_batas_atas.get())

    if f(batas_bawah, persamaan) * f(batas_atas, persamaan) < 0:
        btn_calculate["state"] = NORMAL
        btn_check_condition["state"] = DISABLED
        messagebox.showinfo("Syarat Terpenuhi", f"F({batas_bawah}).F({batas_atas}) < 0\n"
                                                f"Maka terdapat akar persamaan pada selang [{batas_bawah}, {batas_atas}]\n"
                                                "Selanjutnya tekan tombol Hitung...")
    else:
        btn_calculate["state"] = DISABLED
        messagebox.showinfo("Syarat Tidak Terpenuhi", f"F({batas_bawah}).F({batas_atas}) > 0\n"
                                                      f"Tidak terdapat akar persamaan pada selang [{batas_bawah}, {batas_atas}]\n"
                                                      "Silakan cari selang baru...")


# Fungsi untuk menghitung akar persamaan dengan metode Regula Falsi
def calculate():
    btn_calculate["state"] = DISABLED
    btn_reset["state"] = NORMAL

    persamaan = str(ent_persamaan.get())
    tol_err = float(ent_tol_err.get())
    batas_bawah = float(ent_batas_bawah.get())
    batas_atas = float(ent_batas_atas.get())
    i = 1
    results = [["Iterasi", "a", "b", "xr", "F(a)", "F(b)", "F(xr)", "Error"]]

    while True:
        fa = f(batas_bawah, persamaan)
        fb = f(batas_atas, persamaan)

        xr = batas_atas - (fb * (batas_atas - batas_bawah) / (fb - fa))
        fxr = f(xr, persamaan)
        error = abs(fxr)
        results.append([i, f"{batas_bawah:.6f}", f"{batas_atas:.6f}", f"{xr:.6f}",
                        f"{fa:.6f}", f"{fb:.6f}", f"{fxr:.6f}", f"{error:.6f}"])

        if error < tol_err:
            print_results(results)
            conclusion(i, tol_err, xr)

            # Menambah label keterangan di bawah tabel
            lbl_keterangan = Label(f4, text="Keterangan:", font=("Helvetica Neue", 12, "bold"), bg="#E5E5E5", pady=16)
            lbl_keterangan.grid(row=len(results) + 1, column=0, sticky="w")

            keterangan = f"Akhir iterasi, diperoleh akar dengan nilai xr = {xr:.6f}"
            lbl_keterangan_text = Label(f4, text=keterangan, font=("Helvetica Neue", 12), bg="#E5E5E5")
            lbl_keterangan_text.grid(row=len(results) + 1, column=0, columnspan=7)
            break

        if fa * fxr < 0:
            batas_atas = xr
        else:
            batas_bawah = xr

        i += 1


# Fungsi untuk mereset semua input dan tampilan
def reset():
    btn_check_condition["state"] = NORMAL
    btn_reset["state"] = DISABLED

    ent_persamaan.delete(0, END)
    ent_tol_err.delete(0, END)
    ent_batas_bawah.delete(0, END)
    ent_batas_atas.delete(0, END)

    for widget in f4.winfo_children():
        widget.destroy()


# Inisialisasi GUI menggunakan tkinter
root = Tk()
root.title("Metode Regula Falsi")
root.geometry("750x600")
root.configure(bg="#E5E5E5")

# Membuat beberapa frame untuk tata letak elemen GUI
f1 = Frame(root, width=600, height=50, bg="#E5E5E5")
f1.pack(side=TOP, pady=16)
f2 = Frame(root, width=600, height=100, bg="#E5E5E5")
f2.pack(side=TOP, pady=16)
f3 = Frame(root, width=600, height=50, bg="#E5E5E5")
f3.pack(side=TOP, pady=16)
f4 = Frame(root, width=600, height=350, bg="#E5E5E5")
f4.pack(side=TOP, pady=16)

# Label judul aplikasi
lbl_title = Label(f1, font=("Helvetica Neue", 16, "bold"), text="Metode Regula Falsi", bg="#E5E5E5")
lbl_title.pack()

# Label dan input untuk persamaan, toleransi error, batas bawah, dan batas atas
lbl_persamaan = Label(f2, text="Persamaan", font=("Helvetica Neue", 12), bg="#E5E5E5")
lbl_persamaan.grid(row=0, column=0, sticky="w")
ent_persamaan = Entry(f2, font=("Helvetica Neue", 12), justify="right")
ent_persamaan.grid(row=0, column=1)

lbl_tol_err = Label(f2, text="Toleransi Error", font=("Helvetica Neue", 12), bg="#E5E5E5")
lbl_tol_err.grid(row=1, column=0, sticky="w")
ent_tol_err = Entry(f2, font=("Helvetica Neue", 12), justify="right")
ent_tol_err.grid(row=1, column=1, pady=4)

lbl_batas_bawah = Label(f2, text="Batas Atas", font=("Helvetica Neue", 12), bg="#E5E5E5")
lbl_batas_bawah.grid(row=0, column=2, padx=(20, 0), sticky="w")
ent_batas_bawah = Entry(f2, font=("Helvetica Neue", 12), justify="right")
ent_batas_bawah.grid(row=0, column=3)

lbl_batas_atas = Label(f2, text="Batas Bawah", font=("Helvetica Neue", 12), bg="#E5E5E5")
lbl_batas_atas.grid(row=1, column=2, padx=(20, 0), sticky="w")
ent_batas_atas = Entry(f2, font=("Helvetica Neue", 12), justify="right")
ent_batas_atas.grid(row=1, column=3, pady=4)

# Tombol "Syarat" untuk memeriksa syarat terpenuhi
btn_check_condition = Button(f3, text="Syarat", width=16, command=check_condition, bd=0, relief="solid", padx=10,
                             pady=5, borderwidth=2, bg="#FF9800")
btn_check_condition.grid(row=0, column=1)

# Tombol "Hitung" untuk melakukan perhitungan
btn_calculate = Button(f3, text="Hitung", width=16, command=calculate, bd=0, relief="solid", padx=10, pady=5,
                       borderwidth=2, bg="#FF9800", state=DISABLED)
btn_calculate.grid(row=0, column=2, padx=(8, 8))

# Tombol "Reset" untuk mereset input dan tampilan
btn_reset = Button(f3, text="Reset", width=16, command=reset, bd=0, relief="solid", padx=10, pady=5, borderwidth=2,
                   bg="#FF9800", state=DISABLED)
btn_reset.grid(row=0, column=3)

# Memulai aplikasi tkinter
root.mainloop()
