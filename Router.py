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

    def masking(entry,ip):
        
        ip_binary = '.'.join(format(int(x), '08b') for x in ip.split('.'))
        pass
        

    def send_packets(self):
        for packet in self.packets:
            for entry in self.table:
                self.masking(entry,packet)
                
                

router = Router()
router.read_packets()
print(router.table)
ip_address = "192.168.1.100"
ip_binary = '.'.join(format(int(x), '08b') for x in ip_address.split('.'))
print(ip_binary)

