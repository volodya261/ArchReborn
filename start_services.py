import subprocess

SERVICES = ["NetworkManager", 
            "bluetooth", 
            "libvirtd.socket", 
            "earlyoom",
            "laptop-mode.service",
            "sddm",
            "grub-btrfsd",
            "fstrim.service",
            "fstrim.timer"
            ]

def manage_service(service_name, action):
    try:
        subprocess.run(["sudo", "systemctl", action, service_name], check=True)
        print(f"Сервис {service_name} {action} успешно.")
    except subprocess.CalledProcessError:
        print(f"Ошибка при выполнении {action} для {service_name}.")

def main():
    for service in SERVICES:
        print(f"Настройка {service}...")

        # Включаем автозапуск
        manage_service(service, "enable")

        # Запускаем сервис
        manage_service(service, "start")

if __name__ == "__main__":
    main()

