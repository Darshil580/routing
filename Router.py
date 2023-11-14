# Author: Darshil Patel(B00946528)
import re

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
            # print(self.packets)

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
    
    def is_loopback_address(self, ip_address):
        loopback_pattern = re.compile(r'^127\.0\.0\.1$|^::1$')

        if loopback_pattern.match(ip_address):
            return True
        else:
            return False
        
    def validate_address_A_B_C(self, ip_address):
        # Regular expression for Class D or E IP addresses
        class_d_or_e_pattern = re.compile(r'^(22[4-9]|23[0-9]|2[4-9][0-9]|[3-9][0-9]{2}|1[0-9]{3})(\.\d{1,3}){3}$|^[4-9][0-9]{0,2}(\.\d{1,3}){3}$')

        # Check if the IP address matches the pattern
        return bool(class_d_or_e_pattern.match(ip_address))

    def send_packets(self):

        out_lst = []

        for packet in self.packets:
            
            flag = 0

            if self.is_loopback_address(packet):
                out_lst.append(packet+" is loopback; discarded")
                continue    
            elif self.validate_address_A_B_C(packet):
                out_lst.append(packet+" is malformed; discarded")
                continue



            for entry in self.table:

                mask_32_result = ""
                
                ip_part =entry[0].split("/")
                if ip_part[1] == "32":
                    # print(entry)
                    mask_32_result = self.mask_control(packet,int(ip_part[1]))

                    if mask_32_result == ip_part[0]:
                        if entry[1] == "-":
                            out_lst.append(packet+" will  be  forwarded on  the  directly  connected  network  on interface " + entry[2])
                            flag = 1
                            break
                        else:
                            out_lst.append(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                            flag = 1
                            break
                    else:
                        continue
            
            if flag == 1:
                continue

            for entry in self.table:

                mask_24_result = ""
                ip_part =entry[0].split("/")
                if ip_part[1] == "24":
                    mask_24_result = self.mask_control(packet,int(ip_part[1]))
                    
                    if mask_24_result == ip_part[0]:
                        if entry[1] == "-":
                            out_lst.append(packet+" will  be  forwarded on  the  directly  connected  network  on interface " + entry[2])
                            flag = 1
                            break
                        else:
                            out_lst.append(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                            flag = 1
                            break
                    else:
                        continue    
            if flag == 1:
                continue
            
    
            for entry in self.table:

                if entry[0] == "0.0.0.0/0":
                    out_lst.append(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                    break
                # mask_default_result = ""
                # ip_part =entry[0].split("/")
                # if ip_part[1] == "0":
                #     mask_default_result = self.mask_control(packet,int(ip_part[1]))
                #     if mask_default_result == ip_part[0]:

                #         if entry[1] == "-":
                #             print(packet+" will  be  forwarded on  the  directly  connected  network  on interface " + entry[2])
                #             break
                #         else:
                #             print(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                #             break
                #     else:
                #         continue   

        for index, x in enumerate(out_lst):
            print(index + 1,x)

router = Router()
router.read_packets()
router.send_packets()


