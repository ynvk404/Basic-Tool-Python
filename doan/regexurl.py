import re

def is_valid_domain(domain):
    """Kiểm tra xem domain có hợp lệ không, bao gồm cả 'localhost'."""
    if domain == "localhost":
        return True

    regex = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:[a-zA-Z]{2,})$'
    return re.match(regex, domain) is not None

def is_valid_ip(ip):
    """Kiểm tra xem địa chỉ IPv4 có hợp lệ không."""
    regex = r'^(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|1?[0-9][0-9]?)$'
    return re.match(regex, ip) is not None
