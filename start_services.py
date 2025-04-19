import subprocess
import logging
import sys
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('archreborn.log')
    ]
)

SERVICES = [
    "NetworkManager",
    "bluetooth",
    "libvirtd.socket",
    "earlyoom",
    "laptop-mode.service",
    "sddm",
    "grub-btrfsd",
    "fstrim.service",
    "fstrim.timer"
]

class ServiceManager:
    @staticmethod
    def manage_service(service_name: str, action: str) -> bool:
        """
        Управление системным сервисом.
        
        Args:
            service_name: Имя сервиса
            action: Действие (enable/disable/start/stop/restart)
            
        Returns:
            bool: True если операция успешна, False в противном случае
        """
        try:
            subprocess.run(
                ["sudo", "systemctl", action, service_name],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(f"Сервис {service_name} {action} успешно.")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при выполнении {action} для {service_name}: {e.stderr}")
            return False

    @staticmethod
    def is_service_active(service_name: str) -> bool:
        """Проверяет, активен ли сервис."""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == "active"
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def setup_service(service_name: str) -> bool:
        """
        Настраивает сервис: включает автозапуск и запускает его.
        
        Args:
            service_name: Имя сервиса
            
        Returns:
            bool: True если все операции успешны, False в противном случае
        """
        logging.info(f"Настройка {service_name}...")
        
        # Включаем автозапуск
        if not ServiceManager.manage_service(service_name, "enable"):
            return False
            
        # Запускаем сервис если он не активен
        if not ServiceManager.is_service_active(service_name):
            if not ServiceManager.manage_service(service_name, "start"):
                return False
                
        return True

def main():
    """
    Основная функция для настройки всех сервисов.
    Использует многопоточность для ускорения процесса.
    """
    manager = ServiceManager()
    failed_services = []
    
    # Используем ThreadPoolExecutor для параллельной настройки сервисов
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_service = {
            executor.submit(manager.setup_service, service): service
            for service in SERVICES
        }
        
        for future in as_completed(future_to_service):
            service = future_to_service[future]
            try:
                success = future.result()
                if not success:
                    failed_services.append(service)
            except Exception as e:
                logging.error(f"Неожиданная ошибка при настройке {service}: {e}")
                failed_services.append(service)
    
    # Выводим итоговый результат
    if failed_services:
        logging.error("Следующие сервисы не удалось настроить:")
        for service in failed_services:
            logging.error(f"- {service}")
        sys.exit(1)
    else:
        logging.info("Все сервисы успешно настроены!")

if __name__ == "__main__":
    main()

