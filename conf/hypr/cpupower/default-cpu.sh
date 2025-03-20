#!/bin/bash

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "Этот скрипт должен быть запущен с правами суперпользователя"
   exit 1
fi

# Убираем ограничения частоты на всех ядрах
echo "Сброс ограничений частоты процессора..."
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
    max_available_freq=$(cat "$cpu/cpufreq/cpuinfo_max_freq")
    min_available_freq=$(cat "$cpu/cpufreq/cpuinfo_min_freq")
    echo $min_available_freq > "$cpu/cpufreq/scaling_min_freq"
    echo $max_available_freq > "$cpu/cpufreq/scaling_max_freq"
done

# Включаем все ядра
echo "Включение всех доступных ядер..."
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
    echo 1 > "$cpu/online" 2>/dev/null
done

echo "Настройки процессора сброшены по умолчанию."

