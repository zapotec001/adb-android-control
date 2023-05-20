import os
import subprocess
import sys
import time

ADB_PATH = r"ADB DİRECTORY HERE"  # adb dosyasının tam yolunu buraya yazın

def install_adb():
    print("ADB yükleniyor...")
    subprocess.run(["curl", "-O", "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"], check=True)
    subprocess.run(["tar", "-xf", "platform-tools-latest-windows.zip"], check=True)
    os.environ["PATH"] += os.pathsep + os.path.abspath("platform-tools")
    print("ADB başarıyla yüklendi.")

def check_adb_installed():
    try:
        result = subprocess.run([os.path.join(ADB_PATH, "adb"), "version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("ADB zaten yüklü.")
        else:
            print("ADB yüklü değil.")
            install_adb()
    except FileNotFoundError:
        print("ADB yüklü değil.")
        install_adb()

def connect_device():
    print("Cihaz bağlantısı kuruluyor...")
    subprocess.run([os.path.join(ADB_PATH, "adb"), "devices"], check=True)
    print("Cihaz bağlantısı başarıyla kuruldu.")
    time.sleep(10)

def enable_usb_tethering():
    subprocess.run([os.path.join(ADB_PATH, "adb"), "shell", "settings", "put", "global", "tether_dun_required", "0"])
    subprocess.run([os.path.join(ADB_PATH, "adb"), "shell", "service", "call", "connectivity", "33", "i32", "1"])
    time.sleep(10)

def disable_usb_tethering():
    subprocess.run([os.path.join(ADB_PATH, "adb"), "shell", "service", "call", "connectivity", "33", "i32", "0"])
    time.sleep(10)

def main():
    check_adb_installed()
    connect_device()
    enable_usb_tethering()
    print("USB üzerinden internet paylaşımı etkinleştirildi.")

    time.sleep(10)  # 10 saniye bekleyin

    disable_usb_tethering()
    print("USB üzerinden internet paylaşımı devre dışı bırakıldı.")

if __name__ == "__main__":
    main()
