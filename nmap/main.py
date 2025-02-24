import nmap
from colorama import Fore, Style, init
import ipaddress

init(autoreset=True)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def scan_nmap(ip, limit_port):
    if not is_valid_ip(ip):
        print(f"{Fore.RED}[!] Địa chỉ IP không hợp lệ: {ip}{Style.RESET_ALL}")
        return

    nmap1 = nmap.PortScanner()
    try:
        nmap1.scan(ip, f'1-{limit_port}', arguments='-sS -Pn -vv -T5', timeout='30')
    except Exception as e:
        print(f"{Fore.RED}[!] Lỗi khi quét Nmap: {e}{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Lệnh Nmap đã thực thi : {nmap1.command_line()}{Style.RESET_ALL}")

    for host in nmap1.all_hosts():
        print(f"\nHost: {host} ({nmap1[host].hostname()}) - State : {nmap1[host].state()}")
        for proto in nmap1[host].all_protocols():
            print(f"Protocol : {proto}")
            lport = nmap1[host][proto].keys()
            for port in sorted(lport):
                state = nmap1[host][proto][port].get('state', 'unknown')
                print(f"Port: {port}\tState: {state}")
        print("-" * 50)

if __name__ == '__main__':
    banner = """
              (   (           (                   )      )   *           (                    
   (    (     )\ ))\ )  (     )\ )  (    (     ( /(   ( /( (  `    (     )\ )                 
 ( )\   )\   (()/(()/(  )\   (()/(  )\   )\    )\())  )\()))\))(   )\   (()/(                 
 )((_|(((_)(  /(_))(_)|((_)   /(_)|((_|(((_)( ((_)\  ((_)\((_)()((((_)(  /(_))                
((_)_ )\ _ )\(_))(_)) )\___  (_)) )\___)\ _ )\ _((_)  _((_|_()((_)\ _ )\(_))                  
 | _ )(_)_\(_) __|_ _((/ __| / __((/ __(_)_\(_) \| | | \| |  \/  (_)_\(_) _ \                 
 | _ \ / _ \ \__ \| | | (__  \__ \| (__ / _ \ | .` | | .` | |\/| |/ _ \ |  _/                 
 (___//_/ \(\|_(_/_(_| \___| |___/ \___/_/)\_\|_|\)| |)|\_|_|  |_/)/ \_\|_|   )            )  
 )\ )  (   )\ ))\ ))\ )  *   )     (   ( /(    ( /(( /(        ( /( (      ( /(         ( /(  
(()/(  )\ (()/(()/(()/(` )  /(   ( )\  )\())   )\())\())    (  )\()))\ )   )\())(   (   )\()) 
 /(_)|((_) /(_))(_))(_))( )(_))  )((_)((_)\   ((_)((_)\     )\((_)\(()/(  ((_)\ )\  )\|((_)\  
(_)) )\___(_))(_))(_)) (_(_())  ((_)___ ((_) __ ((_)((_) _ ((_)_((_)/(_))_ _((_|(_)((_)_ ((_) 
/ __((/ __| _ \_ _| _ \|_   _|   | _ ) \ / / \ \ / / _ \| | | | \| (_)) __| \| \ \ / /| |/ /  
\__ \| (__|   /| ||  _/  | |     | _ \\ V /   \ V / (_) | |_| | .` | | (_ | .` |\ V / | ' <   
|___/ \___|_|_\___|_|    |_|     |___/ |_|     |_| \___/ \___/|_|\_|  \___|_|\_| \_/  |_|\_\                                                                                                                                                                                                                                              
"""
    print(f"{Fore.RED}🔥 Exploit Script by YOUNG NVK 🔥{Style.RESET_ALL}")
    print(Fore.GREEN + banner + Style.RESET_ALL)
    scan_nmap("10.10.101.172",1000)
