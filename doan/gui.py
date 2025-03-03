import tkinter as tk
from PIL import Image, ImageTk
from functools import partial 
from callbacks import scan_url_callback  

def create_interface(scan_url_callback):
    root = tk.Tk()
    root.title("SQL Injection Scanner")
    root.resizable(False, False)

    # logo
    logo_image = Image.open("D:/Documents/Python-for-PT/doan/imgs/logo.png")
    logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg="#ADD8E6")
    logo_label.place(x=360, y=15)
    logo_label.image = logo_photo

    # Nhập URL
    url_label = tk.Label(root, text="URL/Domain :", fg="Black", font=('Times New Roman', 14, 'bold'), bg="#ADD8E6")
    url_label.place(x=120, y=155)
    entry = tk.Entry(root, width=60)
    entry.place(x=285, y=155)
    
    # Thông báo lỗi
    notification_label = tk.Label(root, text="", fg="black", font=('Times New Roman', 14, 'bold'), bg="#ADD8E6")
    notification_label.place(x=285, y=185)
    notification_label.place_forget()

    # Thông báo
    text_area_label = tk.Label(root, text="Notification", fg="black", font=('Times New Roman', 14, 'bold'), bg="#ADD8E6")
    text_area_label.place(x=125, y=215)
    text_area = tk.Text(root, height=10, width=65, bg="white", fg="black", font=('Times New Roman', 12))
    text_area.place(x=125, y=255)
    text_area.config(state=tk.DISABLED)

    # Chọn chức năng
    function_label = tk.Label(root, text="Function:", fg="Black", font=('Times New Roman', 14, 'bold'), bg="#ADD8E6")
    function_label.place(x=125, y=500)  

    # Danh sách các chức năng
    function_choices = ["Fuzzing"]
    selected_function = tk.StringVar(root)
    selected_function.set(function_choices[0]) 
    
    # Chức năng
    function_menu = tk.OptionMenu(root, selected_function, *function_choices)
    function_menu.place(x=285, y=495) 

    # ✅ Nút Scan (Đã sửa để gửi selected_function)
    scan_button = tk.Button(
        root, text="Scan", fg="white", bg="#008B8B", font=('Times New Roman', 14, 'bold'),
        command=partial(scan_url_callback, entry, notification_label, selected_function)  # ✅ Gửi selected_function
    )
    scan_button.place(x=350, y=550)

    # Cửa sổ
    window_width = 800
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    root.config(bg="#ADD8E6")

    return root, selected_function  # ✅ Trả về cả selected_function
