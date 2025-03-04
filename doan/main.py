import tkinter as tk
from gui import create_interface
from callbacks import scan_url_callback  

root, selected_function, trying_label = create_interface(scan_url_callback)

root.mainloop()  #Run Chạy giao diện
