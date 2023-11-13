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
        
        for entry in self.table:
            print(entry)

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

        # print(ip)
        # print("hello",subnet_mask)

        return self.masking(ip,subnet_mask)

           
    def masking(self,ip,subnet_mask):
        ip_binary = '.'.join(format(int(x), '08b') for x in ip.split('.'))
        mask_binary = '.'.join(format(int(x), '08b') for x in subnet_mask.split('.'))
        network_address_binary = '.'.join([str(int(ip, 2) & int(mask, 2)) for ip, mask in zip(ip_binary.split('.'), mask_binary.split('.'))])
        return network_address_binary

    def send_packets(self):
        for packet in self.packets:

            for entry in self.table:

                mask_32_result = ""
                
                ip_part =entry[0].split("/")
                if ip_part[1] == "32":
                    # print(entry)
                    mask_32_result = self.mask_control(packet,int(ip_part[1]))

                    if mask_32_result == ip_part[0]:
                        if entry[1] == "-":
                            print(packet+" will  be  forwarded on  the  directly  connected  network  on interface " + entry[2])
                            return
                        else:
                            print(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                            return
                    else:
                        continue

            for entry in self.table:

                mask_24_result = ""
                ip_part =entry[0].split("/")
                if ip_part[1] == "24":
                    mask_24_result = self.mask_control(packet,int(ip_part[1]))
                    
                    if mask_24_result == ip_part[0]:
                        if entry[1] == "-":
                            print(packet+" will  be  forwarded on  the  directly  connected  network  on interface " + entry[2])
                        else:
                            print(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                    else:
                        continue               
                

router = Router()
router.read_packets()
router.send_packets()


