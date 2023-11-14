# Author: Darshil Patel(B00946528)
import re

class Router:
    
    def __init__(self):
        
        # Reading routing table. 
        with open("RoutingTable.txt","r") as file:
            text = file.read()
            lst = text.split("\n")
            self.table = []

        # Storing the table in the Data Structure.
        i = 0
        while i < len(lst) - 2:
            temp = list((lst[i], lst[i+1], lst[i+2]))
            self.table.append(temp)
            i += 3
        
        #Simulating Table
        print("\n-------------- Routeing Table --------------")
        for entry in self.table:
            print(entry)
        print("--------- Routeing Table Ended -------------\n")


    # Reading random packets from the text file.
    def read_packets(self):
        with open("RandomPackets.txt","r") as file:
            input = file.read()
            self.packets = input.split("\n")

    # Decding the mask address for the IP address.
    def mask_control(self,ip,mask):

        mask = int(mask)
        subnet_mask = ""

        # Host specific Mask
        if mask == 32:
            subnet_mask = "255.255.255.255"
        # Normal Class A/B/C Mask
        elif mask == 24:
            subnet_mask = "255.255.255.0"
        elif mask == 16:
            subnet_mask = "255.255.0.0"
        elif mask == 8:
            subnet_mask = "255.0.0.0"  

        #Default Mask
        else:
            subnet_mask = "0.0.0.0"

        return self.masking(ip,subnet_mask)

    # Performing the operation binary AND operation between Mask and IP address.
    def masking(self,ip,subnet_mask):
        ip_binary = '.'.join(format(int(x), '08b') for x in ip.split('.')) # Converting to binary
        mask_binary = '.'.join(format(int(x), '08b') for x in subnet_mask.split('.')) # Converting to binary
        network_address = '.'.join([str(int(ip, 2) & int(mask, 2)) for ip, mask in zip(ip_binary.split('.'), mask_binary.split('.'))])
        return network_address
    
    # Checking Loopback IP.
    def is_loopback_address(self, ip_address):

        # Regex for checking the loopback_ip pattern
        loopback_pattern = re.compile(r'^127\.0\.0\.1$|^::1$')

        if loopback_pattern.match(ip_address):
            return True
        else:
            return False
    
    # For checking ip address is Type/Class D or E
    def validate_address(self, ip_address):

        # Regular expression for Class D or E IP addresses
        pattern = re.compile(r'^(22[4-9]|23[0-9]|2[4-9][0-9]|[3-9][0-9]{2}|1[0-9]{3})(\.\d{1,3}){3}$|^[4-9][0-9]{0,2}(\.\d{1,3}){3}$')

        # Check if the IP address matches the pattern
        return bool(pattern.match(ip_address))
    
    
    # Router 1.Masking and 2.Searching 3. Forwarding task. 
    def process_entries(self,packet, mask):

        for entry in self.table:
            entry_ip,entry_ip_mask = entry[0].split("/")

            # Comparing for mask value to be specific like 32/24/16/8/0 etc.
            if entry_ip_mask == mask:

                # Perform masking with packet ip address
                mask_result = self.mask_control(packet,entry_ip_mask)

                if mask_result == entry_ip:
                    # Checking next hope address (entry[1] - next hop, entry[2] - interface)
                    if entry[1] == "-":
                        self.out_lst.append(packet+" will be forwarded on the directly connected network on interface " + entry[2])
                    else:
                        self.out_lst.append(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                    return True
                
        return False

    # Sending packets to next destination
    def send_packets(self):

        # Data Structure for storing output logs
        self.out_lst = []

        for packet in self.packets:
            
            # First - checking for loopback address.
            if self.is_loopback_address(packet):
                self.out_lst.append(packet+" is loopback; discarded")
                continue    

            # Second - checking for validity of the address
            elif self.validate_address(packet):
                self.out_lst.append(packet+" is malformed; discarded")
                continue

            # Third - Checking for Host specific entries in the table
            if self.process_entries(packet,"32"):
                continue
            
            # Fourth - Checking for Normal network entries Type C
            if self.process_entries(packet,"24"):
                continue

            # Fifth - Checking for Normal network entrie Type B
            if self.process_entries(packet,"16"):
                continue

            # Sixth - Checking for Normal network entrie Type A
            if self.process_entries(packet,"8"):
                continue
            
            # Seven - default entries in the routing table.
            for entry in self.table:

                if entry[0] == "0.0.0.0/0":
                    self.out_lst.append(packet+" will be forwarded to "+ entry[1] +" out on interface " + entry[2])
                    break

    # Function of the router class that writes the output to a file called RoutingOutput.txt.
    def write_output_packets(self):
        with open("RoutingOutput.txt","w") as file:
            print("Output logs:")
            print("-------------------------------------------------")
            for item in self.out_lst:
                file.write(item + "\n")
                print(item)

router = Router()
router.read_packets()
router.send_packets()
router.write_output_packets()