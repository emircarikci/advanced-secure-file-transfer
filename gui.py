import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import socket
import os
import time

def send_file_tcp(filename, server_ip='127.0.0.1', server_port=5000):
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import os
    import hashlib

    try:
        # Sunucu public anahtarını yükle
        with open("server_public.pem", "rb") as key_file:
            server_public_key = serialization.load_pem_public_key(key_file.read())

        # AES anahtarı ve IV üret
        aes_key = os.urandom(32)
        iv = os.urandom(16)

        # Dosyayı oku ve hash'le
        with open(filename, "rb") as f:
            file_data = f.read()
        sha256 = hashlib.sha256(file_data).digest()

        # [hash + dosya] birleştir
        data_to_encrypt = sha256 + file_data

        # AES ile şifrele
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data_to_encrypt) + encryptor.finalize()

        # AES anahtarını sunucu public anahtarı ile şifrele
        encrypted_key = server_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Soket ile bağlantı kur ve şu sıralamayla gönder:
        # 1. RSA ile şifrelenmiş anahtar uzunluğu (4 byte)
        # 2. RSA ile şifrelenmiş anahtar
        # 3. IV (16 byte)
        # 4. Şifreli veri uzunluğu (8 byte)
        # 5. Şifreli veri

        s = socket.socket()
        s.connect((server_ip, server_port))
        s.sendall(len(encrypted_key).to_bytes(4, 'big'))
        s.sendall(encrypted_key)
        s.sendall(iv)
        s.sendall(len(encrypted_data).to_bytes(8, 'big'))
        s.sendall(encrypted_data)
        s.close()

        messagebox.showinfo("Başarılı", "TCP ile şifreli dosya gönderildi.")

    except Exception as e:
        messagebox.showerror("Hata", str(e))


def send_file_udp(filename, server_ip='127.0.0.1', server_port=6000):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        with open(filename, 'rb') as f:
            data = f.read()
        packet_size = 1024
        for i in range(0, len(data), packet_size):
            s.sendto(data[i:i+packet_size], (server_ip, server_port))
            time.sleep(0.005)
        s.sendto(b'__END__', (server_ip, server_port))
        s.close()
        messagebox.showinfo("Başarılı", "UDP ile dosya gönderildi.")
    except Exception as e:
        messagebox.showerror("Hata", str(e))

def browse_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def send_file():
    filename = file_entry.get()
    proto = var_proto.get()
    if not filename or not os.path.isfile(filename):
        messagebox.showerror("Hata", "Dosya seçiniz!")
        return
    if proto not in ["tcp", "udp"]:
        messagebox.showerror("Hata", "Protokol seçiniz!")
        return
    t = threading.Thread(target=send_file_tcp if proto=="tcp" else send_file_udp, args=(filename,))
    t.start()

root = tk.Tk()
root.title("Hybrid Dosya Gönderici")

tk.Label(root, text="Dosya Seç:").grid(row=0, column=0, padx=10, pady=10)
file_entry = tk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10)
tk.Button(root, text="Gözat", command=browse_file).grid(row=0, column=2, padx=10)

tk.Label(root, text="Protokol:").grid(row=1, column=0, padx=10, pady=10)
var_proto = tk.StringVar()
tk.Radiobutton(root, text="TCP", variable=var_proto, value="tcp").grid(row=1, column=1, sticky='w')
tk.Radiobutton(root, text="UDP", variable=var_proto, value="udp").grid(row=1, column=2, sticky='w')

tk.Button(root, text="Gönder", command=send_file, bg='green', fg='white').grid(row=2, column=1, pady=20)

root.mainloop()
