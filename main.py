# Mengimpor modul tkinter (disingkat) sebagai tk
import tkinter as tk
# Mengimpor fungsi filedialog dari tkinter
from tkinter import filedialog
# Mengimpor modul Image, ImageTk, ImageEnhance, ImageDraw, ImageFont dari library PILLOW
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont


# Kelas untuk mengimplementasikan sebuah aplikasi konversi gambar menjadi ASCII
class ASCIIConverter:

    # Fungsi untuk inisialisasi awal (constructor) --------------------------------------------------------
    def __init__(self, root):
        self.root = root
        self.root.title("Image to ASCII Art Converter")
        self.root.iconbitmap("assets\\ascii.ico")

        # Full-windowed mode
        self.root.state("zoomed")

        # Variable utuk gambar asli hingga ascii
        self.image_path = ""
        self.image = None
        self.ascii_image = None
        self.ascii_image_width = None
        self.ascii_image_height = None

        # Nilai awal dari Slider
        self.char_count_var = tk.IntVar()
        self.char_count_var.set(20)

        self.brightness_var = tk.IntVar()
        self.brightness_var.set(1)

        self.contrast_var = tk.IntVar()
        self.contrast_var.set(1)
        
        self.saturation_var = tk.IntVar()
        self.saturation_var.set(1)

        self.sharpness_var = tk.IntVar()
        self.sharpness_var.set(1)

        # Menampilkan widget
        self.create_widgets()


    # Fungsi untuk membuat widget yang diperlukan ---------------------------------------------------------
    def create_widgets(self):
        # Frame untuk canvas preview gambar
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=10)
    
        # Frame untuk hasil ascii
        result_frame = tk.Frame(main_frame)
        result_frame.grid(row=0, column=0, padx=15)

        # Canvas untuk hasil konversi (ditampikan dalam textbox)
        self.textbox = tk.Text(result_frame, font=("Courier", 6), width=200, height=92)
        self.textbox.grid(row=0, column=0)
        self.textbox.config(wrap="none", state="disabled")
        self.textbox.tag_configure("center", justify="center")
        self.textbox.tag_add("center", "1.0", "end")

        # Label untuk menampilkan keretangan ukuran hasil ascii
        self.ascii_detail = tk.Label(result_frame, text="Width(Columns): -, Height(Rows): -")
        self.ascii_detail.grid(row=1, column=0, pady=2)

        # Frame untuk slider pengaturan
        settings_frame = tk.Frame(main_frame)
        settings_frame.grid(row=0, column=1, padx=10)

        # Canvas untuk gambar asli
        self.canvas_image = tk.Canvas(settings_frame, width=400, height=400, background="lightgrey")
        self.canvas_image.grid(row=0, column=0, pady=10, columnspan=2)

        # Tombol untuk memuat gambar
        load_button = tk.Button(settings_frame, text="Load Image", command=self.load_image, width=25)
        load_button.grid(row=1, column=0, padx=10 ,pady=10)

        # Tombol untuk mengembalikan ke pengaturan awal
        load_button = tk.Button(settings_frame, text="Reset Settings", command=self.reset_settings, width=25)
        load_button.grid(row=1, column=1, padx=10 ,pady=10)

        # Membuat slider pengaturan
        # create_slider(parent_frame, label, variable, resolution, from, to, row, column, collumn_span, len)
        self.create_slider(settings_frame, "Character Count", self.char_count_var, 1, 20, 400, 2, 0, 2, 382)
        self.create_slider(settings_frame, "Brightness", self.brightness_var, 1, 1, 300, 3, 0, 1, 177)
        self.create_slider(settings_frame, "Contrast", self.contrast_var, 1, -20, 20, 3, 1, 1, 177)
        self.create_slider(settings_frame, "Saturation", self.saturation_var, 1, -20, 20, 4, 0, 1, 177)
        self.create_slider(settings_frame, "Sharpness", self.sharpness_var, 1, -20, 20, 4, 1, 1, 177)

        # Tombol untuk menyimpan hasil
        save_button = tk.Button(settings_frame, text="Save ASCII Image", command=self.save_ascii_art_image, width=25)
        save_button.grid(row=5, column=0, padx=10, pady=15)

        # Tombol untuk menyimpan hasil
        save_button = tk.Button(settings_frame, text="Save ASCII Text", command=self.save_ascii_art_text, width=25)
        save_button.grid(row=5, column=1, padx=10, pady=15)


    # Fungsi untuk membuat slider pengaturan --------------------------------------------------------------
    def create_slider(self, parent_frame, label, variable, resolution, from_, to, row, column, collumn_span, len):
        # Membuat label frame untuk membingkai slider
        label_frame = tk.LabelFrame(parent_frame, text=label)
        label_frame.grid(row=row, column=column, columnspan=collumn_span, pady=3)

        # Membuat slider untuk mengubah nilai pengaturan
        slider = tk.Scale(label_frame, from_=from_, to=to, variable=variable, resolution=resolution, orient=tk.HORIZONTAL, command=self.update_preview, length=len)
        slider.pack()


    # Fungsi untuk mengembalikan pengaturan gambar ke pengaturan awal -------------------------------------
    def reset_settings(self):
        # Menyetel nilai variabel pengaturan ke setelan awal yaitu 1
        self.brightness_var.set(1)
        self.contrast_var.set(1)
        self.saturation_var.set(1)
        self.sharpness_var.set(1)
        # Jumlah karakter tidak perlu di-reset

        # Memperbarui preview gambar asli dan hasil ascii
        self.update_preview()
    

    # Fungsi untuk memuat gambar --------------------------------------------------------------------------
    def load_image(self):
        # Membuka filedialog untuk memudahkan user memilih file gambar
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])

        # Jika file (path) didapatkan, maka buka dan simpan data gambar lalu perbarui preview
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.update_preview()


    # Fungsi untuk mendapatkan data gambar dengan ukuran yang sesuai character_count ----------------------
    def resize_image(self, image, new_width):
        # Menyimpan lebar dan tinggi gambar
        width, height = image.size
        # Menghitung rasio gambar
        ratio = height / width
        # Menghitung tinggi yang sesuai rasio 
        new_height = int(new_width * ratio)
        # Mendapatkan data gambar dengan ukuran yang sesuai
        resized_image = image.resize((new_width, new_height))

        # Memperbarui informasi detail
        self.ascii_detail.config(text="Width(Columns): " + str(new_width) + ", Height(Rows): " + str(new_height))

        # Memperbarui ukuran ascii image (untuk simpan hasil ascii menjadi gambar)
        self.ascii_image_height = new_height
        self.ascii_image_width = new_width

        # Mengembalikan gambar yng telah disesuaikan ukurannya
        return resized_image


    # Fungsi untuk mengubah gambar menjadi grayscale ------------------------------------------------------
    def grayscale_image(self, image):
        grayscale_image = image.convert("L")
        return grayscale_image


    # Funsgi untuk mengubah gambar ke karakter ascii ------------------------------------------------------
    def image_to_ascii(self, image):
        # Karakter ascii yang digunakan
        ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

        # Mendapatakan data warna tunggal (grayscale) tiap pixel dari gambar
        pixels = image.getdata()

        # Mengisi array ascii_image dengan kekosongan
        ascii_image = ""
        # Melakukan perulangan untuk setiap isi array pixels
        for pixel in pixels:
            # Memilih (indeks dari) karakter ascii sesuai kecerahan gambar
            index = int(pixel / 255 * (len(ASCII_CHARS) - 1))
            # Menggabungkan karakter ascii yang sudah ditentukan ke array ascii_image
            ascii_image += ASCII_CHARS[index]
        return ascii_image


    # Fungsi untuk memperbarui textbox dengan hasil ascii -------------------------------------------------
    def update_textbox(self, ascii_image, width):
        # Mengatur textbox ke kondisi normal untuk diisi hasil ascii
        self.textbox.config(state="normal")
        # Membersihkan isi textbox dari titik awal hingga paling akhir
        self.textbox.delete("1.0", tk.END)

        # Melakukan perulangan untuk dari 0 sampai sepanjang isi array ascii_image(jumlah pixel), dengan peningkatan sebanyak width(char_count
        for i in range(0, len(ascii_image), width):
            # Mendapatkan sebaris string dalam ascii_image
            line = ascii_image[i:i+width] + "\n"
            # Menambahkan baris tersebut ke titik paling akhir dalam textbox
            self.textbox.insert(tk.END, line)

        # Mengatur textbox ke kondisi disabled(tidak bisa diubah)
        self.textbox.config(state="disabled")


    # Fungsi untuk memperbarui preview gambar asli dan hasil ascii ----------------------------------------
    def update_preview(self, event=None):
        # Jika terdapat data gambar
        if self.image is not None:
            # Mendapatkan nilai pengaturan
            char_count = int(self.char_count_var.get())
            brightness = int(self.brightness_var.get())
            contrast = int(self.contrast_var.get())
            saturation = int(self.saturation_var.get())
            sharpness = int(self.sharpness_var.get())

            # Memproses kecerahan, kontras, warna(saturasi), dan ketajaman gambar sesuai nilai pengaturan
            img = self.image
            img = ImageEnhance.Brightness(img).enhance(brightness)
            img = ImageEnhance.Contrast(img).enhance(contrast)
            img = ImageEnhance.Color(img).enhance(saturation)
            img = ImageEnhance.Sharpness(img).enhance(sharpness)

            # Menampilkan hasil pengaturan ke preview gambar asli
            self.display_image(self.canvas_image, img)

            # # Proses mengubah gambar ke ascii art
            # Mendapatkan gambar dengan ukuran yang sesuai dengan jumlah karakter
            img = self.resize_image(img, char_count)
            # Mengubah gambar manjadi hanya berwarna grayscale
            img = self.grayscale_image(img)
            # Mengubah gambar menjadi ascii
            self.ascii_image = self.image_to_ascii(img)
            # Memperbarui textbox dengan diisikan hasil ascii
            self.update_textbox(self.ascii_image, char_count)


    # Fungsi untuk menampilkan gambar yang dimuat ke kanvas -----------------------------------------------
    def display_image(self, canvas, image):
        # Jika terdaoat data gambar
        if image:
            # # Proses menyesuaikan ukuran gambar dengan ukuran canvas
            # Mendapatkan lebar dan panjang gambar
            width, height = image.size
            # Menginisialisasi posisi awal (X = Horizontal | Y = Vertikal)
            posX = 0
            posY = 0
            if width > height:
                # Jika lebar > tinggi, maka sesuaikan denga ratio hasil pembagian tinggi terhadap lebar dan sesuaikan posisi vertikal
                ratio = height / width
                new_height = int(400 * ratio)
                resized_image = image.resize((400, new_height))
                posY = 200 - int(new_height / 2)
            else:
                # Jika lebar < tinggi, maka sesuaikan denga ratio hasil pembagian lebar terhadap tinggi dan sesuaikan posisi horizontal
                ratio = width / height 
                new_width = int(400 * ratio)
                resized_image = image.resize((new_width, 400))
                posX = 200 - int(new_width / 2)

            # Mengubah gambar menjadi objek ImageTk
            photo = ImageTk.PhotoImage(resized_image)
            # Membersihkan canvas dari gambar sebelumnya
            canvas.delete("all")
            # Menambahkan gambar ke canvas
            canvas.create_image(posX, posY, anchor=tk.NW, image=photo)
            # Menyimpan referensi gambar agar tidak dihapus oleh garbage collector
            canvas.image = photo

    
    # Fungsi untuk menyimpan hasil ascii menjadi gambar ---------------------------------------------------
    def save_ascii_art_image(self):
        # Jika terdapat hasil ascii
        if self.ascii_image is not None:
            # Membuka filedialog untuk memudahkan user menentukan nama file dan direktori penyimpanan
            # nama file dan direktori penyimpanan tersimpan sebagai path
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

            # Jika path didapatkan
            if save_path:
                # Mengambil text ascii yang siap cetak dari textbox
                ascii_text = self.textbox.get("1.0", tk.END)

                # Menyiapkan font untuk mencetak text ascii pada gambar
                font = ImageFont.truetype(r"assets\\courier.ttf", 10)  

                # Menentikan ukuran gambar menyesuaikan lebar dan tinggi text ascii
                final_width = self.ascii_image_width * 10 - int(self.ascii_image_width * 4)
                final_height = self.ascii_image_height * 10 - int(self.ascii_image_height * 2)
                
                # Membuat data gambar dengan lebar dan tinggi yang telah disesuaikan
                img = Image.new("RGBA",(final_width, final_height), "white")

                # Menggambarkan text ascii pada gambar
                draw = ImageDraw.Draw(img)
                draw.text((0, 0), ascii_text, fill="black", font=font, spacing=1)

                # Menyimpan gambar sesuai path
                img.save(save_path)

    
    # Fungsi untuk menyimpan hasil ascii menjadi text -----------------------------------------------------
    def save_ascii_art_text(self):
        # Jika terdaoat hasil ascii
        if self.ascii_image is not None:
            # Membuka filedialog untuk memudahkan user menentukan nama file dan direktori penyimpanan
            # nama file dan direktori penyimpanan tersimpan sebagai path
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

            # Jika path didapatkan
            if save_path:
                # Membuat file dengan mode "tulis" sesuai path
                with open(save_path, "w") as file:
                    # Menuliskan/mengisikan text ascii ke dalam file
                    file.write(self.textbox.get("1.0", tk.END))


# Jika file ini dijalankan sebagai program utama
if __name__ == "__main__":
    # Membuat window mengguanakan modul tkinter
    root = tk.Tk()
    # Menginstansiasiakan class ASCIIConverter dengan root sebagai argumen
    app = ASCIIConverter(root)
    # Menjalankan sebuah event loop yang akan terus berjalan hingga window (tkinter) ditutup user
    root.mainloop()
