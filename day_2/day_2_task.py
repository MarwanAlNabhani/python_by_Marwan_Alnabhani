import ipaddress

# =================================================================================
# Calculation
def calculateNetworkAddress(ip, cidr):
    """ convert the IP address and subnet mask to 
    binary, then perform a bitwsie AND operation, return in binary"""
    # ref: https://www.geeksforgeeks.org/computer-networks/role-of-subnet-mask/
    
    # convert ip and mask to binary
    ip_binary = ipToBinary(ip)
    mask_binary = cidrToBinaryMask(cidr)
    
    # bitwise AND
    network_binary = binaryAND(ip_binary, mask_binary)
    
    # return in binary form
    return network_binary


def calculateBroadcastAddress(ip,cidr):
    """ get the mask in binary, then invert the subnet mask to get the host 
    portion, then calculate network address in binary form, then perform bitwise 
    OR operation, return in binary"""
    # ref: https://www.geeksforgeeks.org/computer-networks/what-is-broadcasting-in-computer-network/
    
    # mask
    mask_binary = cidrToBinaryMask(cidr)
    inverted_mask = invertBinary(mask_binary)
    
    # network ip in binary
    network_binary = calculateNetworkAddress(ip,cidr)
    
    # Bitwise OR 
    broadcast_binary = binaryOR(network_binary, inverted_mask)
    
    # return in binary form
    return broadcast_binary 


def calculateUsableHosts(cidr):
    # ref: https://www.geeksforgeeks.org/computer-networks/how-to-calculate-number-of-host-in-a-subnet/
    if cidr == 31:
        return 2
    if cidr == 32:
        return 1
    return (2 ** (32 - cidr)) - 2
# =================================================================================

# =================================================================================
# HELPERS 
def ipToBinary(ip):
    """convert IP to Binary"""
    return '.'.join([bin(int(x)+256)[3:] for x in ip.split('.')]) 

def binaryToIp(bin_ip):
    """convert Binary to IP"""
    return '.'.join(str(int(octet, 2)) for octet in bin_ip.split('.'))

def cidrToBinaryMask(cidr):
    """ convert CIDR mask to Binary"""
    mask = '1' * cidr + '0' * (32-cidr)
    return '.'.join(mask[i:i+8] for i in range(0, 32, 8))

def invertBinary(binary_string):
    return '.'.join(
        ''.join('1' if bit == '0' else '0' for bit in part)
        for part in binary_string.split('.')
    )
# =================================================================================


# =================================================================================
# Bitwise AND & OR
def binaryAND(ip_binary, mask_binary):
    """ Apply AND operation to each bit between 
    the ip binary in mask binary """
    
    result = []
    ip_parts = ip_binary.split('.')
    mask_parts = mask_binary.split('.')
    
    for i in range(4):
        and_part = ''.join(
            '1' if ip_parts[i][j] == '1' and mask_parts[i][j] == '1' else '0'
            for j in range(8)
        )
        result.append(and_part)
    
    return '.'.join(result) 


def binaryOR(binary1, binary2):
    """Apply OR operation to each bit between two binary numbers"""
    result = []
    
    parts1 = binary1.split('.')
    parts2 = binary2.split('.')
    
    for i in range(4):
        or_part = ''.join(
            '1' if parts1[i][j] == '1' or parts2[i][j] == '1' else '0'
            for j in range(8)
        )
        result.append(or_part)
    
    return '.'.join(result)
# =================================================================================




def main():
    # Get ip and cidr
    ip = input("Enter an IP address: ").strip()
    cidr = input("Enter CIDR prefix: ").strip()
    
    
    print("=== Subnet Calculator ===")
    
    # Validate the IP address and cidr and handling the exception
    try:
        network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
    except ValueError as e:
        print(f"Error: Invalid IP address or CIDR prefix provided.")
        print(f"Details: {e}")
        print("=========================")
        return
    
    # casting to int
    CIDR = int(cidr)
    
    # Calculation
    networkAddress = binaryToIp(calculateNetworkAddress(ip,CIDR))
    broadcastAddress = binaryToIp(calculateBroadcastAddress(ip,CIDR))
    usableHosts = calculateUsableHosts(CIDR)
    
    # Display the output
    print(f"Network Address:            {networkAddress}")
    print(f"Broadcast Address:          {broadcastAddress}")
    print(f"Number of Usable Hosts:     {usableHosts}")
    print("=========================")
    
    
if __name__ == "__main__":
    main()