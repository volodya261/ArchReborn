import subprocess
import shlex
import re

package_file = "app.lst"
pacman_conf = "/etc/pacman.conf"

def setup_arch_aur():
    # Путь для клонирования yay
    repo_url = "https://aur.archlinux.org/yay.git"
    local_dir = "/tmp/yay"
    # Клонирование репозитория yay
    print(f"Клонирование {repo_url} в {local_dir}")
    subprocess.run(["git", "clone", repo_url, local_dir], check=True)
    # Сборка и установка yay
    print("Сборка yay...")
    subprocess.run(["makepkg", "-si"], cwd=local_dir, check=True)
    print("yay успешно установлен!")
    subprocess.run(["sudo", "rm", "-rf", local_dir])

# Функция для правки pacman.conf
def configure_pacman():
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
            multilib_found = False  # Отключаем флаг после изменения
        elif line.startswith("#ParallelDownloads") or re.match(r"^ParallelDownloads\s*=\s*\d+", line):
            modified_lines.append("ParallelDownloads = 5\n")
            parallel_found = True
        else:
            modified_lines.append(line)

    if not parallel_found:
        modified_lines.append("\nParallelDownloads = 5\n")

    with open(pacman_conf, "w") as f:
        f.writelines(modified_lines)

    print("Файл pacman.conf обновлен!")

# Функция для установки пакетов
def install_packages(package_manager="pacman"):
    with open(package_file, "r") as f:
        packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if not packages:
        print("Нет пакетов для установки.")
        return

    if package_manager == "pacman":
        cmd = f"pacman -Sy --needed --noconfirm {' '.join(packages)}"
    elif package_manager == "yay":
        cmd = f"yay -Sy --needed --noconfirm {' '.join(packages)}"
    else:
        print("Неизвестный пакетный менеджер")
        return

    print(f"Устанавливаю: {', '.join(packages)}")
    subprocess.run(shlex.split(cmd), check=True)

configure_pacman()

# Синхронизируем пакеты и обновляем систему
subprocess.run(["sudo", "pacman", "-Syyu", "--noconfirm"], check=True)

# Установка пакетов
install_packages("pacman")
#setup_arch_aur()

