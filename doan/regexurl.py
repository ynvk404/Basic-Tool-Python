# regex.py
import re

def is_valid_domain(domain):
    #Kiểm tra xem tên miền có hợp lệ không
    regex = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2,})$'
    return re.match(regex, domain) is not None

def is_valid_ip(ip):
    #Kiểm tra xem địa chỉ IP có hợp lệ không
    regex = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    return re.match(regex, ip) is not None
