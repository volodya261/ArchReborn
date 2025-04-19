import subprocess
import shlex
import re
import os
import logging
import sys
from typing import List, Optional

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('archreborn.log')
    ]
)

# Файлы со списками пакетов
PACMAN_CONF = "/etc/pacman.conf"
PACMAN_LIST = "app.lst"
AUR_LIST = "aur.lst"
PARALLEL_DOWNLOADS = 5

class PackageInstaller:
    @staticmethod
    def is_yay_installed() -> bool:
        try:
            subprocess.run(
                ["yay", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def setup_yay() -> None:
        if PackageInstaller.is_yay_installed():
            logging.info("yay уже установлен.")
            return

        repo_url = "https://aur.archlinux.org/yay.git"
        local_dir = "/tmp/yay"

        try:
            logging.info(f"Клонирование {repo_url} в {local_dir}")
            subprocess.run(["git", "clone", repo_url, local_dir], check=True)

            logging.info("Сборка yay...")
            subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=local_dir, check=True)

            logging.info("yay успешно установлен!")
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при установке yay: {e}")
            raise
        finally:
            subprocess.run(["rm", "-rf", local_dir])

    @staticmethod
    def configure_pacman() -> None:
        logging.info("Настройка pacman.conf...")

        try:
            with open(PACMAN_CONF, "r") as f:
                lines = f.readlines()
        except IOError as e:
            logging.error(f"Ошибка при чтении {PACMAN_CONF}: {e}")
            raise

        modified_lines = []
        multilib_found = False
        parallel_found = False

        for line in lines:
            if line.strip() == "#[multilib]":
                modified_lines.append("[multilib]\n")
                multilib_found = True
            elif multilib_found and line.strip() == "#Include = /etc/pacman.d/mirrorlist":
                modified_lines.append("Include = /etc/pacman.d/mirrorlist\n")
                multilib_found = False
            elif line.startswith("#ParallelDownloads") or re.match(
                r"^ParallelDownloads\s*=\s*\d+", line
            ):
                modified_lines.append(f"ParallelDownloads = {PARALLEL_DOWNLOADS}\n")
                parallel_found = True
            else:
                modified_lines.append(line)

        if not parallel_found:
            modified_lines.append(f"\nParallelDownloads = {PARALLEL_DOWNLOADS}\n")

        temp_file = "/tmp/pacman.conf"
        try:
            with open(temp_file, "w") as f:
                f.writelines(modified_lines)
            subprocess.run(["sudo", "mv", temp_file, PACMAN_CONF], check=True)
            logging.info("Файл pacman.conf обновлен!")
        except (IOError, subprocess.CalledProcessError) as e:
            logging.error(f"Ошибка при обновлении {PACMAN_CONF}: {e}")
            raise

    @staticmethod
    def read_packages(package_file: str) -> List[str]:
        if not os.path.exists(package_file):
            logging.warning(f"Файл {package_file} не найден, пропускаю установку.")
            return []

        try:
            with open(package_file, "r") as f:
                return [
                    line.split("#")[0].strip()
                    for line in f
                    if line.split("#")[0].strip()
                ]
        except IOError as e:
            logging.error(f"Ошибка при чтении {package_file}: {e}")
            raise

    @staticmethod
    def install_packages(package_file: str, package_manager: str) -> None:
        packages = PackageInstaller.read_packages(package_file)
        if not packages:
            logging.info(f"Нет пакетов для установки из {package_file}.")
            return

        cmd_map = {
            "pacman": f"sudo pacman -Sy --needed --noconfirm {' '.join(packages)}",
            "yay": f"yay -Sy --needed --noconfirm {' '.join(packages)}"
        }

        if package_manager not in cmd_map:
            logging.error(f"Неизвестный пакетный менеджер: {package_manager}")
            return

        cmd = cmd_map[package_manager]
        logging.info(
            f"Устанавливаю {len(packages)} пакетов из {package_file} с помощью {package_manager}:"
        )
        logging.info(", ".join(packages))
        
        try:
            subprocess.run(shlex.split(cmd), check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при установке пакетов: {e}")
            raise

def main():
    try:
        installer = PackageInstaller()
        installer.configure_pacman()

        logging.info("Обновление системы...")
        subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"], check=True)

        installer.install_packages(PACMAN_LIST, "pacman")
        installer.setup_yay()
        installer.install_packages(AUR_LIST, "yay")

        logging.info("Все пакеты установлены!")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
