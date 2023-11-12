# Author: Darshil Patel(B00946528)

class Router:
    
    def __init__(self):
        with open("RoutingTable.txt","r") as file:
            text = file.read()
            lst = text.split("\n")
            self.table = []

        i = 0
        while i < len(lst) - 2:
            temp = list((lst[i], lst[i+1], lst[i+2]))
            self.table.append(temp)
            i += 3

    def read_packets(self):
        with open("RandomPackets.txt","r") as file:
            input = file.read()
            self.packets = input.split("\n")

    def mask_control(self,ip,mask):

        subnet_mask = ""
        
        if mask == 32:
            subnet_mask = "255.255.255.255"
        elif mask == 24:
            subnet_mask = "255.255.255.0"
        elif mask == 16:
            subnet_mask = "255.255.0.0"
        elif mask == 8:
            subnet_mask = "255.0.0.0"  
        else:
            subnet_mask = "0.0.0.0"

        self.masking(ip,subnet_mask)

           
    def masking(ip,mask):
        ip_binary = '.'.join(format(int(x), '08b') for x in ip.split('.'))
        mask_binary = '.'.join(format(int(x), '08b') for x in mask.split('.'))
        network_address_binary = ''.join([str(int(ip, 2) & int(mask, 2)) for ip, mask in zip(ip_binary.split('.'), mask_binary.split('.'))])
        decimal_ip = '.'.join(str(int(network_address_binary[i:i+8], 2)) for i in range(0, 32, 8))
        return decimal_ip

    def send_packets(self):
        for packet in self.packets:
            
            for entry in self.table:
                ip_part =entry.split("/")
                if ip_part[1] == "32":
                    self.masking(ip_part[1],int(ip_part[1]))
                
                

router = Router()
router.read_packets()
print(router.table)
ip_address = "192.168.1.100"
ip_binary = '.'.join(format(int(x), '08b') for x in ip_address.split('.'))
print(ip_binary)

