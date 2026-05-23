# Запуск мониторинга сайтов

from src.monitor import SiteMonitor

# Создаём монитор со списком сайтов по умолчанию
monitor = SiteMonitor()

# Проверяем все сайты
monitor.check_all_sites()

# Показываем лог
print("\n===== СОДЕРЖИМОЕ ЛОГ-ФАЙЛА =====")
print(monitor.read_log())