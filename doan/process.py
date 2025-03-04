import requests
import threading
import time
from detect_utils import check_content_length, check_html_similarity

SQL_ERRORS = [
    "You have an error in your SQL syntax",  # MySQL
    "Warning: mysql_fetch_assoc()",         # MySQL
    "Unknown column",                        # MySQL
    "ERROR: syntax error at or near",       # PostgreSQL
    "PG::SyntaxError: ERROR:",              # PostgreSQL
    "Unclosed quotation mark after the character string",  # MSSQL
    "Incorrect syntax near"                 # MSSQL
]

payload_file = r"D:/Documents/Python-for-PT/doan/payloads-sqli/general-error-based.txt"

def load_payloads(file_path):
    """Load danh sách payloads từ file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[X] Error loading payload file: {e}")
        return []

def fuzzing(root, url, text_area, trying_label, scan_button):
    """Chạy fuzzing trên thread riêng để tránh lag GUI."""
    scan_button.config(bg="#228B22", fg="red", text="Scanning...", font=('Times New Roman', 14, "bold"))

    # Hiện `trying_label` báo hiệu bắt đầu scan sau 2 giây
    trying_label.place(x=125, y=185)
    root.after(2000, lambda: trying_label.config(text="Starting scan...", fg="blue"))

    # Sau 2 giây mới chạy scan thực sự
    root.after(2000, lambda: threading.Thread(
        target=error_based_sqli_detection, args=(root, url, text_area, trying_label, scan_button)
    ).start())

def error_based_sqli_detection(root, url, text_area, trying_label, scan_button):
    """Kiểm tra Error-Based SQL Injection và cập nhật GUI."""
    payloads = load_payloads(payload_file)

    # Lấy phản hồi gốc (trước khi thử payload)
    try:
        original_response = requests.get(url, timeout=5)
        original_length = len(original_response.text)
        original_content = original_response.text
    except requests.RequestException:
        print("[X] Lỗi khi kết nối đến URL")
        root.after(0, lambda: trying_label.config(text="Connection Error!", fg="red"))
        root.after(3000, lambda: trying_label.place_forget())
        return

    detected_payload = None
    detected_status = None

    for payload in payloads:
        try:
            injected_url = f"{url}{payload}"
            
            # Hiển thị payload đang thử, chỉ sau khi đã hiển thị "Starting scan..."
            root.after(0, lambda: trying_label.config(text=f"Trying: {payload}", fg="blue"))
            time.sleep(0.5)  # Chờ 0.5 giây để hiển thị payload đang thử

            response = requests.get(injected_url, timeout=5)
            response_length = len(response.text)
            response_content = response.text

            # 1️⃣ Kiểm tra lỗi SQL từ HTTP status code hoặc trong nội dung phản hồi
            if response.status_code in [500, 400] or any(error.lower() in response_content.lower() for error in SQL_ERRORS):
                detected_payload, detected_status = payload, response.status_code
                break  # Phát hiện lỗi, dừng lại ngay
            elif response.status_code == 403:
                # Bỏ qua nếu bị chặn bởi WAF, không kết luận là SQLi
                continue      
            # 2️⃣ Kiểm tra sự thay đổi Content-Length đáng kể
            if check_content_length(original_length, response_length):
                detected_payload, detected_status = payload, response.status_code
                break

            # 3️⃣ So sánh nội dung HTML với bản gốc để tìm dấu hiệu bất thường
            if check_html_similarity(original_content, response_content):
                detected_payload, detected_status = payload, response.status_code
                break

        except requests.RequestException as e:
            print(f"[X] Request error: {e}")

    # Kết thúc scan, cập nhật trạng thái
    if detected_payload:
        root.after(0, lambda: trying_label.config(text="SQLi Detected!", fg="red"))
        root.after(5000, lambda: trying_label.place_forget())  # Giữ 5 giây nếu phát hiện SQLi
    else:
        root.after(0, lambda: trying_label.config(text="No SQLi found", fg="green"))
        root.after(2000, lambda: trying_label.place_forget())  # Ẩn sau 2 giây nếu không phát hiện

    # Cập nhật kết quả lên GUI
    root.after(0, lambda: update_text_area(text_area, detected_payload, detected_status))

    # Reset lại nút scan
    root.after(0, lambda: scan_button.config(bg="#228B22", fg="white", text="Scan", state="normal"))

def update_text_area(text_area, payload, status):
    """Cập nhật kết quả quét vào text_area."""
    text_area.config(state="normal")
    text_area.insert("end", "\n")

    if payload:
        result_text = (
            f"[!] SQL Injection Detected!\n"
            f"    - Payload: {payload}\n"
            f"    - HTTP Status: {status}\n"
        )
    else:
        result_text = "[+] No SQL Injection vulnerability found.\n"

    text_area.insert("end", result_text)  
    text_area.config(state="disabled")  
    text_area.yview("end")  
