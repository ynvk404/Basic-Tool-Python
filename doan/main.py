import tkinter as tk
from gui import create_interface
from callbacks import scan_url_callback  

root, selected_function = create_interface(scan_url_callback)

root.mainloop()  # Chạy giao diện
