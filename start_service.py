import subprocess

# Список сервисов для включения и запуска
SERVICES = ["NetworkManager", 
            "bluetooth", 
            "libvirtd.socket", 
            "earlyoom",
            "laptop-mode.service",
            "sddm"
            ]

def manage_service(service_name, action):
    """Управляет сервисами systemd (start, enable, restart, stop)."""
    try:
        subprocess.run(["sudo", "systemctl", action, service_name], check=True)
        print(f"Сервис {service_name} {action} успешно.")
    except subprocess.CalledProcessError:
        print(f"Ошибка при выполнении {action} для {service_name}.")

def main():
    """Включает и запускает указанные сервисы."""
    for service in SERVICES:
        print(f"Настройка {service}...")

        # Включаем автозапуск
        manage_service(service, "enable")

        # Запускаем сервис
        manage_service(service, "start")

if __name__ == "__main__":
    main()

