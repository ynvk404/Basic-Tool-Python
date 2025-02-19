import requests
from colorama import Fore, Style
logins = []
with open('D:\\Documents\Python-for-PT\\Fuzz\\logins.txt') as files:
    for line in files:
        login = line.strip()
        logins.append(login)

domain = 'http://testphp.vulnweb.com'

def check_domain(domain, logins):
    total_logins = len(logins)
    count = 1
    try:
        with open('D:\\Documents\Python-for-PT\\Fuzz\\output.txt', "w", encoding="utf-8") as output:
            for login in logins:
                response = requests.get(domain + '/' + login)
                status_messages = {
                    200: "Login resource found",
                    404: "Login resource not found",
                    403: "Forbidden resource",
                    302: "Redirected resource found",
                    500: "Internal server error",
                    503: "Service unavailable"
                }
                message = status_messages.get(response, "Unknown status code")
                result = f"[{response.status_code}] {message}: {'/'} {login}\n"
                output.write(result)
                percent = (count / total_logins) * 100
                count += 1
                print(f"\rĐang chạy: {percent:.2f}%", end="")             
    except requests.exceptions.RequestException as e:
        print("Error: %s" % e)

if __name__ == '__main__':
    banner = """
 __     __   ____    _    _   _   _    _____   _   _   _      _   _  __
 \ \   / /  / __ \  | |  | | | \ | |  / ____| | \ | | \ \    / / | |/ /                
  \ \_/ /  | |  | | | |  | | |  \| | | |  __  |  \| |  \ \  / /  | ' /                 
   \   /   | |  | | | |  | | | . ` | | | |_ | | . ` |   \ \/ /   |  <                  
    | |    | |__| | | |__| | | |\  | | |__| | | |\  |    \  /    | . \                 
    |_|     \____/   \____/  |_| \_|  \_____| |_| \_|     \/     |_|\_\               
                                                                                       
                                                                                       
   _____                 _           _       ____              _   _  __      __  _  __
  / ____|               (_)         | |     |  _ \            | \ | | \ \    / / | |/ /
 | (___     ___   _ __   _   _ __   | |_    | |_) |  _   _    |  \| |  \ \  / /  | ' / 
  \___ \   / __| | '__| | | | '_ \  | __|   |  _ <  | | | |   | . ` |   \ \/ /   |  < 
  ____) | | (__  | |    | | | |_) | | |_    | |_) | | |_| |   | |\  |    \  /    | . \ 
 |_____/   \___| |_|    |_| | .__/   \__|   |____/   \__, |   |_| \_|     \/     |_|\_\
                            | |                       __/ |                            
                            |_|                      |___/ 


"""
    print(f"{Fore.RED}🔥 Exploit Script by YOUNG NVK 🔥{Style.RESET_ALL}")
    print(banner)
    check_domain(domain, logins)
    print(f"\n✅ Kết quả đã được lưu vào: {"output.txt"}")