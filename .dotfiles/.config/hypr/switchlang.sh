#!/usr/bin/bash
# ~/.config/hypr/switch-layout.sh

KEYBOARDS=(
    "at-translated-set-2-keyboard"
    "company--usb-device---keyboard"
)

# Используем первую активную клавиатуру из списка
ACTIVE_KEYBOARD="${KEYBOARDS[0]}"

# Получаем текущую раскладку для конкретной клавиатуры
current_name=$(hyprctl devices -j | jq -r ".keyboards[] | select(.name == \"$ACTIVE_KEYBOARD\") | .active_keymap")

# Если не нашли, берем первую доступную
if [ -z "$current_name" ]; then
    current_name=$(hyprctl devices -j | jq -r '.keyboards[0].active_keymap')
fi

# Показываем текущую раскладку
case "$current_name" in
    *English*|*US*)  icon="EN" ;;
    *Russian*)       icon="RU" ;;
    *Ukrainian*)     icon="UA" ;;
    *)               icon="${current_name:0:2}" ;;
esac

swayosd-client --custom-message "󰌌 $icon"

# Переключаем раскладку
for kb in "${KEYBOARDS[@]}"; do
    hyprctl switchxkblayout "$kb" next >/dev/null 2>&1 || true
done
