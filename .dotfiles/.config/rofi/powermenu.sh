#!/usr/bin/env bash

# порядок: Выключение, Ребут, Сон, Выход, Замок
options="\n\n\n\n"

# Вызываем rofi
chosen="$(echo -e "$options" | rofi -dmenu -theme ~/.config/rofi/powermenu.rasi -p "Power Menu")"

# Логика действий (теперь порядок в case не важен, главное совпадение символа)
case $chosen in
    "") systemctl poweroff ;;
    "") systemctl reboot ;;
    "") systemctl suspend ;;
    "") hyprctl dispatch exit ;;
    "") hyprlock ;; # Убедитесь, что у вас установлен hyprlock или замените на свою команду
esac
