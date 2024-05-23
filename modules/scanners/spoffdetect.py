from scapy.all import sniff


class ARPSpoofingDetector:
	def __init__(self):
		self.IP_MAC_Map = {}

	def process_packet(self):
		src_IP = packet['ARP'].psrc
		src_MAC = packet['Ether'].src

		if src_MAC in self.IP_MAC_Map.keys():
			if self.IP_MAC_Map[src_MAC] != src_IP :
				try:
					old_IP = self.IP_MAC_Map[src_MAC]
				except:
					old_IP = "Неизвестный"

				message = f'''ARP атака замечена
Это возможно со стороны машины с IP адресом {old_IP} для {src_IP}'''

				return message
			else:
				self.IP_MAC_Map[src_MAC] = src_IP

	def sniffing(self):
		sniff(count=0, filter="arp", store=0, prn=self.process_packet)
