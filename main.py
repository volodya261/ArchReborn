import subprocess

# Список скриптов для выполнения
SCRIPTS = ["install_app.py", "manage_services.py"]

def run_script(script_name):
    """Запускает указанный скрипт."""
    try:
        print(f"\n=== Запуск {script_name} ===")
        subprocess.run(["python", script_name], check=True)
        print(f"✅ {script_name} выполнен успешно!")
    except subprocess.CalledProcessError:
        print(f"❌ Ошибка при выполнении {script_name}.")

def main():
    """Запускает все необходимые скрипты по порядку."""
    for script in SCRIPTS:
        run_script(script)

if __name__ == "__main__":
    main()

