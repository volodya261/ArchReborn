#!/usr/bin/env bash

# Список иконок (Nerd Font)
#  Замок,  Выход,  Сон,  Ребут,  Выключение
options="\n\n\n\n"

# Вызываем rofi в режиме dmenu
chosen="$(echo -e "$options" | rofi -dmenu -theme ~/.config/rofi/powermenu.rasi -p "Power Menu")"

# Логика действий
case $chosen in
    "") hyprlock ;; # или swaylock / ваша команда блокировки
    "") hyprctl dispatch exit ;;
    "") systemctl suspend ;;
    "") systemctl reboot ;;
    "") systemctl poweroff ;;
esac
