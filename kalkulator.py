import tkinter as tk
from tkinter import font
import math # Ditambahkan untuk memproses operasi matematika lanjutan

class KalkulatorDesktop:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Desktop")
        # Jendela dibuat sedikit lebih tinggi (540) untuk menampung baris tombol baru
        self.root.geometry("320x540") 
        self.root.resizable(False, False)
        
        # --- Tema Warna Modern Dark Mode ---
        self.bg_color = "#1E1E2E"       # Latar belakang gelap
        self.layar_color = "#181825"    # Latar layar
        self.btn_num = "#313244"        # Warna tombol angka
        self.btn_adv = "#45475A"        # Warna tombol operasi lanjutan (Abu-abu agak terang)
        self.btn_op = "#89B4FA"         # Warna tombol operasi (Biru)
        self.btn_clear = "#F38BA8"      # Warna tombol Clear (Merah)
        self.btn_eq = "#A6E3A1"         # Warna tombol Sama Dengan (Hijau)
        self.fg_color = "#CDD6F4"       # Warna teks utama
        self.fg_dark = "#11111B"        # Warna teks gelap (untuk tombol warna)
        
        self.root.configure(bg=self.bg_color)
        
        self.ekspresi = ""
        self.teks_input = tk.StringVar()
        self.teks_input.set("0")
        
        # Pengaturan Font
        self.font_layar = font.Font(family="Segoe UI", size=36, weight="bold")
        self.font_tombol = font.Font(family="Segoe UI", size=15, weight="bold")
        
        self.buat_layar()
        self.buat_tombol()

    def buat_layar(self):
        frame_layar = tk.Frame(self.root, bg=self.layar_color, bd=0)
        frame_layar.pack(expand=True, fill="both", pady=0, padx=0)
        
        layar = tk.Label(
            frame_layar, 
            textvariable=self.teks_input, 
            font=self.font_layar, 
            bg=self.layar_color, 
            fg=self.fg_color, 
            anchor="e", 
            justify="right",
            padx=20,
            pady=20
        )
        layar.pack(expand=True, fill="both", side="bottom")

    def buat_tombol(self):
        frame_tombol = tk.Frame(self.root, bg=self.bg_color)
        frame_tombol.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Susunan tombol sekarang memiliki 6 baris: (Teks, Baris, Kolom, Warna BG, Warna FG)
        tombol_list = [
            ('√x', 1, 0, self.btn_adv, self.fg_color), ('x²', 1, 1, self.btn_adv, self.fg_color), ('xʸ', 1, 2, self.btn_adv, self.fg_color), ('π', 1, 3, self.btn_adv, self.fg_color),
            ('C', 2, 0, self.btn_clear, self.fg_dark), ('DEL', 2, 1, self.btn_num, self.fg_color), ('%', 2, 2, self.btn_num, self.fg_color), ('÷', 2, 3, self.btn_op, self.fg_dark),
            ('7', 3, 0, self.btn_num, self.fg_color), ('8', 3, 1, self.btn_num, self.fg_color), ('9', 3, 2, self.btn_num, self.fg_color), ('×', 3, 3, self.btn_op, self.fg_dark),
            ('4', 4, 0, self.btn_num, self.fg_color), ('5', 4, 1, self.btn_num, self.fg_color), ('6', 4, 2, self.btn_num, self.fg_color), ('-', 4, 3, self.btn_op, self.fg_dark),
            ('1', 5, 0, self.btn_num, self.fg_color), ('2', 5, 1, self.btn_num, self.fg_color), ('3', 5, 2, self.btn_num, self.fg_color), ('+', 5, 3, self.btn_op, self.fg_dark),
            ('00', 6, 0, self.btn_num, self.fg_color), ('0', 6, 1, self.btn_num, self.fg_color), ('.', 6, 2, self.btn_num, self.fg_color), ('=', 6, 3, self.btn_eq, self.fg_dark)
        ]
        
        # Konfigurasi Grid (6 Baris, 4 Kolom)
        for i in range(1, 7):
            frame_tombol.rowconfigure(i, weight=1)
        for i in range(4):
            frame_tombol.columnconfigure(i, weight=1)
            
        for (teks, baris, kolom, bg_btn, fg_btn) in tombol_list:
            btn = tk.Button(
                frame_tombol, 
                text=teks, 
                font=self.font_tombol, 
                bg=bg_btn, 
                fg=fg_btn,
                bd=0, 
                relief="flat",
                activebackground="#585B70" if bg_btn == self.btn_adv else "#45475A",
                activeforeground="#FFFFFF",
                command=lambda t=teks: self.aksi_tombol(t)
            )
            btn.grid(row=baris, column=kolom, sticky="nsew", padx=4, pady=4)

    def aksi_tombol(self, nilai):
        if self.ekspresi == "Error":
            self.ekspresi = ""

        # Parser aman untuk evaluasi operasi tunggal (mengganti simbol UI ke simbol Python)
        expr_aman = self.ekspresi.replace('×', '*').replace('÷', '/').replace('^', '**')

        if nilai == 'C':
            self.ekspresi = ""
            self.teks_input.set("0")
            
        elif nilai == 'DEL':
            if self.ekspresi:
                self.ekspresi = self.ekspresi[:-1]
                self.teks_input.set(self.ekspresi if self.ekspresi else "0")

        elif nilai == '√x':
            if self.ekspresi:
                try:
                    # Menghitung ekspresi saat ini, lalu diakarkan
                    hasil = str(math.sqrt(float(eval(expr_aman))))
                    self.format_dan_tampilkan(hasil)
                except ValueError:
                    self.teks_input.set("Error") # Mencegah akar bilangan negatif
                    self.ekspresi = "Error"
                except:
                    pass

        elif nilai == 'x²':
            if self.ekspresi:
                try:
                    hasil = str(float(eval(expr_aman)) ** 2)
                    self.format_dan_tampilkan(hasil)
                except:
                    pass

        elif nilai == 'xʸ':
            if self.ekspresi and not self.ekspresi.endswith('^'):
                self.ekspresi += "^"
                self.teks_input.set(self.ekspresi)

        elif nilai == 'π':
            pi_val = "3.14159265"
            if self.ekspresi == "" or self.ekspresi == "0":
                self.ekspresi = pi_val
            # Jika sebelumnya adalah angka, otomatis tambahkan tanda kali (misal: 5π = 5 × π)
            elif self.ekspresi[-1].isdigit() or self.ekspresi[-1] == '.':
                self.ekspresi += "×" + pi_val
            else:
                self.ekspresi += pi_val
            self.teks_input.set(self.ekspresi)
                
        elif nilai == '%':
            if self.ekspresi:
                try:
                    hasil = str(eval(expr_aman) / 100)
                    self.format_dan_tampilkan(hasil)
                except:
                    pass
                    
        elif nilai == '=':
            if not self.ekspresi: return
            try:
                hasil = str(eval(expr_aman))
                self.format_dan_tampilkan(hasil)
            except ZeroDivisionError:
                self.teks_input.set("Error: Bagi 0")
                self.ekspresi = "Error"
            except Exception:
                self.teks_input.set("Error")
                self.ekspresi = "Error"
                
        else:
            if self.ekspresi == "" and nilai in ['0', '00']:
                self.teks_input.set("0")
                return
            self.ekspresi += str(nilai)
            self.teks_input.set(self.ekspresi)

    def format_dan_tampilkan(self, hasil):
        # Mencegah error jika hasil berupa notasi ilmiah (misal 1.2e+10)
        if 'e' in hasil or 'E' in hasil:
            self.teks_input.set(hasil)
            self.ekspresi = hasil
            return
            
        if hasil.endswith('.0'):
            hasil = hasil[:-2]
        elif '.' in hasil and len(hasil.split('.')[1]) > 6:
            hasil = str(round(float(hasil), 6))
            
        self.teks_input.set(hasil)
        self.ekspresi = hasil

if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorDesktop(root)
    root.mainloop()