import subprocess
import logging
import sys
from typing import List, Optional
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('archreborn.log')
    ]
)

# Список скриптов для выполнения
SCRIPTS = [
    "install_app.py",
    "start_services.py"
]

class ScriptRunner:
    @staticmethod
    def validate_scripts() -> bool:
        """
        Проверяет наличие всех необходимых скриптов.
        
        Returns:
            bool: True если все скрипты найдены, False в противном случае
        """
        missing_scripts = []
        for script in SCRIPTS:
            if not Path(script).is_file():
                missing_scripts.append(script)
        
        if missing_scripts:
            logging.error("Следующие скрипты не найдены:")
            for script in missing_scripts:
                logging.error(f"- {script}")
            return False
        return True

    @staticmethod
    def run_script(script_name: str) -> bool:
        """
        Запускает указанный скрипт.
        
        Args:
            script_name: Имя скрипта для запуска
            
        Returns:
            bool: True если скрипт выполнен успешно, False в противном случае
        """
        try:
            logging.info(f"\n=== Запуск {script_name} ===")
            result = subprocess.run(
                ["python", script_name],
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(f"✅ {script_name} выполнен успешно!")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Ошибка при выполнении {script_name}:")
            logging.error(f"Код ошибки: {e.returncode}")
            if e.stdout:
                logging.error(f"Вывод: {e.stdout}")
            if e.stderr:
                logging.error(f"Ошибка: {e.stderr}")
            return False

def main():
    """
    Основная функция для последовательного запуска всех скриптов.
    """
    runner = ScriptRunner()
    
    # Проверяем наличие всех скриптов
    if not runner.validate_scripts():
        sys.exit(1)
    
    # Запускаем скрипты последовательно
    failed_scripts = []
    for script in SCRIPTS:
        if not runner.run_script(script):
            failed_scripts.append(script)
    
    # Выводим итоговый результат
    if failed_scripts:
        logging.error("\nСледующие скрипты завершились с ошибкой:")
        for script in failed_scripts:
            logging.error(f"- {script}")
        sys.exit(1)
    else:
        logging.info("\n✨ Все скрипты выполнены успешно!")

if __name__ == "__main__":
    main()

