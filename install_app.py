import subprocess
import shlex
import re
import os

# Файлы со списками пакетов
pacman_conf = "/etc/pacman.conf"
pacman_list = "app.lst"
aur_list = "aur.lst"

# Проверка, установлен ли yay
def is_yay_installed():
    try:
        subprocess.run(["yay", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Установка yay, если он не установлен
def setup_yay():
    if is_yay_installed():
        print("yay уже установлен.")
        return

    repo_url = "https://aur.archlinux.org/yay.git"
    local_dir = "/tmp/yay"

    print(f"Клонирование {repo_url} в {local_dir}")
    subprocess.run(["git", "clone", repo_url, local_dir], check=True)

    print("Сборка yay...")
    subprocess.run(["makepkg", "-si", "--noconfirm"], cwd=local_dir, check=True)

    print("yay успешно установлен!")
    subprocess.run(["rm", "-rf", local_dir])

# Настройка pacman.conf (с sudo)
def configure_pacman():
    print("Настройка pacman.conf...")

    # Читаем текущий конфиг
    with open(pacman_conf, "r") as f:
        lines = f.readlines()

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
        elif line.startswith("#ParallelDownloads") or re.match(r"^ParallelDownloads\s*=\s*\d+", line):
            modified_lines.append("ParallelDownloads = 5\n")
            parallel_found = True
        else:
            modified_lines.append(line)

    if not parallel_found:
        modified_lines.append("\nParallelDownloads = 5\n")

    # Записываем изменения с правами root
    temp_file = "/tmp/pacman.conf"
    with open(temp_file, "w") as f:
        f.writelines(modified_lines)

    subprocess.run(["sudo", "mv", temp_file, pacman_conf], check=True)
    print("Файл pacman.conf обновлен!")

# Установка пакетов из списка
def install_packages(package_file, package_manager):
    if not os.path.exists(package_file):
        print(f"Файл {package_file} не найден, пропускаю установку.")
        return

    with open(package_file, "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not packages:
        print(f"Нет пакетов для установки из {package_file}.")
        return

    if package_manager == "pacman":
        cmd = f"sudo pacman -Sy --needed --noconfirm {' '.join(packages)}"
    elif package_manager == "yay":
        cmd = f"yay -Sy --needed --noconfirm {' '.join(packages)}"
    else:
        print(f"Неизвестный пакетный менеджер: {package_manager}")
        return

    print(f"Устанавливаю {len(packages)} пакетов из {package_file} с помощью {package_manager}:")
    print(", ".join(packages))
    subprocess.run(shlex.split(cmd), check=True)

# Основная логика скрипта
if __name__ == "__main__":
    # Настройка pacman.conf
    configure_pacman()

    # Обновление системы
    print("Обновление системы...")
    subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"], check=True)

    # Установка пакетов из официальных репозиториев
    install_packages(pacman_list, "pacman")

    # Установка yay (если не установлен)
    setup_yay()

    # Установка пакетов из AUR
    install_packages(aur_list, "yay")

    print("Все пакеты установлены!")

