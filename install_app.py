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
        subprocess.run(
            ["yay", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
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
        elif line.startswith("#ParallelDownloads") or re.match(
            r"^ParallelDownloads\s*=\s*\d+", line
        ):
            modified_lines.append("ParallelDownloads = 5\n")
            parallel_found = True
        else:
            modified_lines.append(line)

    if not parallel_found:
        modified_lines.append("\nParallelDownloads = 5\n")

    temp_file = "/tmp/pacman.conf"
    with open(temp_file, "w") as f:
        f.writelines(modified_lines)

    subprocess.run(["sudo", "mv", temp_file, pacman_conf], check=True)
    print("Файл pacman.conf обновлен!")


# Функция для чтения пакетов с игнорированием комментариев
def read_packages(package_file):
    if not os.path.exists(package_file):
        print(f"Файл {package_file} не найден, пропускаю установку.")
        return []

    packages = []
    with open(package_file, "r") as f:
        for line in f:
            clean_line = line.split("#")[0].strip()  # Удаляем комментарий и пробелы
            if clean_line:  # Добавляем только непустые строки
                packages.append(clean_line)
    return packages


# Функция установки пакетов
def install_packages(package_file, package_manager):
    packages = read_packages(package_file)
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

    print(
        f"Устанавливаю {len(packages)} пакетов из {package_file} с помощью {package_manager}:"
    )
    print(", ".join(packages))
    subprocess.run(shlex.split(cmd), check=True)


if __name__ == "__main__":
    configure_pacman()

    print("Обновление системы...")
    subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"], check=True)

    install_packages(pacman_list, "pacman")
    setup_yay()
    install_packages(aur_list, "yay")

    print("Все пакеты установлены!")
