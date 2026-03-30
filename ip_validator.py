import re

# --- regex solution 
# def is_valid_ipv4(ip):

#     # rules 
#     # exmaple IPv4:  192.168.1.1
#     # four octets separated by 3 dots
#     # each octet range from 0 to 255 inclusive 
    
#     rules = r'^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
#             r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
#             r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.' \
#             r'(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$'
    
#     return re.match(rules, ip) 


# --- non regex solution 
def is_valid_ipv4(ip):
    parts = ip.split('.')
    
    # 3 rules to check
    # rule 1: check for 4 octets
    if len(parts) != 4:
        return False
    
    
    for part in parts:
        # rule 2: check each octet is contains digits only
        if not part.isdigit():
            return False
        
        
        # rule 3: in range of 0-255 inclusive 
        
        # cast string to int 
        octet = int(part)
        
        if octet < 0 or octet > 255:
            return False
        
    return True  

#ip = "192.168.1.1"
ip = input("Enter IPv4 Address: ")

if is_valid_ipv4(ip):
    print("Valid IPv4 address.")
else:
    print("Invalid IPv4 address.")
    
    
