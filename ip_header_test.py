from scapy.all import IP, TCP, send

# Hedef IP (lokal test için 127.0.0.1 kullanılabilir)
target_ip = "127.0.0.1"

# IP paketini oluştur
ip_packet = IP(dst=target_ip, ttl=64, flags="DF", id=1001)

# TCP segmenti ekle (port 5000, çünkü sunucun bu portu dinliyor)
tcp_segment = TCP(dport=5000, sport=4444, flags="S")

# IP + TCP paketini birleştir ve gönder
print("[*] Paket gönderiliyor...")
send(ip_packet / tcp_segment)
print("[+] Paket gönderildi.")
