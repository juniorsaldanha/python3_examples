import os, sys


def main():
    """
    This code is reusable.
    Executes each funtion in the script
    """
    try:
        option = int(input("""
    Choose one of option below:
    ⮕  1. One IP         ex: 192.168.0.1
    ⮕  2. List of IP     ex: 192.168.0.1 192.168.0.2 192.168.0.3
    ⮕  3. Subnet         ex: 192.168.0.0/24
    ⮕  4. Exit           Close this application
        """))
        results_file = open("ping_subnet.txt", "w")
        if option != 4: var = str(input())
        if option == 1: #One
            ping(var.replace(' ',''))
        elif option == 2: #List
            ping_list(results_file, var.split(' '))
        elif option == 3: #Subnet
            if '/' in var:
                (addr, cidr) = var.split('/')
                ping_list(results_file, create_ip_list(*get_network_broadcast_cidr(addr, cidr)))
            else: 
                (addr, mask) = var.split(' ')
                ping_list(results_file, create_ip_list(*get_network_broadcast_mask(addr, mask)))
    except Exception as err:
        print(f"ERROR:{err}")
    finally:
        sys.exit()
        results_file.close()
        


def get_network_broadcast_cidr(addr, cidr) -> tuple:
    addr = [int(x) for x in addr.split(".")]
    cidr = int(cidr)
    mask = [( ((1<<32)-1) << (32-cidr) >> i ) & 255 for i in reversed(range(0, 32, 8))]
    netw = [addr[i] & mask[i] for i in range(4)]
    bcas = [(addr[i] & mask[i]) | (255^mask[i]) for i in range(4)]
    return netw, bcas

def get_network_broadcast_mask(addr, mask) -> tuple:
    addr = [int(x) for x in addr.split(".")]
    mask = [int(x) for x in mask.split(".")]
    cidr = sum((bin(x).count('1') for x in mask))
    netw = [addr[i] & mask[i] for i in range(4)]
    bcas = [(addr[i] & mask[i]) | (255^mask[i]) for i in range(4)]
    return netw, bcas

def create_ip_list(start_addr, end_addr) -> list:
    """Appends the concatenated ip to the ip_list"""
    ip_list = []
    start_addr[3]+=1
    while(start_addr[3] < end_addr[3]):
        ip_list.append(f"{start_addr[0]}.{start_addr[1]}.{start_addr[2]}.{start_addr[3]}")
        start_addr[3] += 1
    return ip_list

def ping(ip) -> str:
    response = os.popen(f"ping {ip} -c 1").read()
    if "1 received" in response:
        result = f"UP   {ip} Ping Successful"
    else:
        result = f"Down {ip} Ping Unsuccessful"
    print(result)
    return result

def ping_list(results_file, ips:list):
    for ip in ips: results_file.write(ping(ip)+'\n')

def ping_subnet(results_file, subnet, num):
    ip_addresses = create_ip_list(subnet, num)
    ping_list(results_file, ip_addresses)


if __name__ == "__main__":
    main()