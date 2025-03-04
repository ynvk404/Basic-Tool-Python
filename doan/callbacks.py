from urllib.parse import urlparse
from regexurl import is_valid_domain, is_valid_ip 
from process import fuzzing  
import gui

def scan_url_callback(root, entry_widget, notification_label, selected_function, text_area, trying_label, scan_button):
    """Hàm xử lý khi người dùng nhập URL và nhấn nút scan."""
    url = entry_widget.get().strip()
    print("URL received from GUI:", url)

    if not url:
        notification_label.config(text="❌ URL cannot be empty!", fg="red")
        notification_label.place(x=125, y=185)
        notification_label.after(2000, lambda: notification_label.place_forget())
        return None

    # Kiểm tra nếu URL chưa có http:// hoặc https:// thì thêm vào
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    print("Processed URL:", url) 

    try:
        parsed_url = urlparse(url)
        domain_with_port = parsed_url.netloc  # Lấy cả domain và port nếu có
        print("Parsed domain_with_port:", domain_with_port) 

        url_target = url  

        if domain_with_port and (is_valid_domain(domain_with_port.split(":")[0]) or is_valid_ip(domain_with_port.split(":")[0])):
            notification_label.config(text=f"✅ Sending: {url_target}", fg="green")
            notification_label.place(x=125, y=185)
            notification_label.after(2000, lambda: notification_label.place_forget())
            # Nếu chọn chức năng "In-band SQLi (Error-based, Union-based)""
            if selected_function.get() == "In-band SQLi (Error-based, Union-based)":
                fuzzing(root, url, text_area, trying_label, scan_button)
            else:
                return url_target
        else:
            raise ValueError("Invalid domain or IP")

    except Exception as e:
        print("Error:", e)
        notification_label.config(text=f"❌ Invalid URL: {url}", fg="red")
        notification_label.place(x=125, y=185)
        notification_label.after(2000, lambda: notification_label.place_forget())
