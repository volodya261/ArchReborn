#!/bin/bash

# Проверка прав суперпользователя
if [[ $EUID -ne 0 ]]; then
   echo "Этот скрипт должен быть запущен с правами суперпользователя" 
   exit 1
fi

# Установить диапазон частот (например, 800 MHz до 1.2 GHz)
MIN_FREQ="400000"   # 400 MHz
MAX_FREQ="1500000"  # 1.5 GHz

echo "Ограничение частоты процессора от $MIN_FREQ до $MAX_FREQ"

# Применить ограничения частоты ко всем ядрам
for cpu in /sys/devices/system/cpu/cpu[0-9]*; do
    echo $MIN_FREQ > "$cpu/cpufreq/scaling_min_freq"
    echo $MAX_FREQ > "$cpu/cpufreq/scaling_max_freq"
done

# Получить общее количество ядер и определить ядра для отключения
total_cores=$(nproc)
cores_to_disable=8  # Количество ядер для отключения

if (( cores_to_disable >= total_cores )); then
    echo "Невозможно отключить $cores_to_disable ядер, так как на системе доступно всего $total_cores."
    exit 1
fi

echo "Отключение $cores_to_disable ядер..."

# Отключить указанные ядра
for (( i=total_cores-1; i>=total_cores-cores_to_disable; i-- )); do
    echo 0 > /sys/devices/system/cpu/cpu$i/online
    echo "Ядро $i отключено"
done

echo "Ограничение частоты и отключение ядер завершены."

