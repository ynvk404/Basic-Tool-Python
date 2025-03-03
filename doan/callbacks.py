from urllib.parse import urlparse
from regexurl import is_valid_domain, is_valid_ip 
from process import fuzzing  

def scan_url_callback(entry_widget, notification_label, selected_function):
    url = entry_widget.get().strip()
    print("URL received from GUI:", url)

    if not url:
        notification_label.config(text="❌ URL cannot be empty!", fg="red")
        notification_label.place(x=125, y=185)
        notification_label.after(2000, lambda: notification_label.place_forget())
        return None

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed_url = urlparse(url)
        domain = parsed_url.hostname  
        url_target = url  

        if is_valid_domain(domain) or is_valid_ip(domain):
            notification_label.config(text=f"✅ Sending: {url_target}", fg="green")
            notification_label.place(x=125, y=185)
            notification_label.after(2000, lambda: notification_label.place_forget())

            # 🔥 Kiểm tra chức năng chọn
            if selected_function.get() == "Fuzzing":
                fuzzing(url_target)  # Gửi đến fuzzing luôn
            else:
                return url_target  # Trả về URL hợp lệ

        else:
            raise ValueError("Invalid domain or IP")
    except Exception as e:
        notification_label.config(text=f"❌ Invalid URL: {url}", fg="red")
        notification_label.place(x=125, y=185)
        notification_label.after(2000, lambda: notification_label.place_forget())
