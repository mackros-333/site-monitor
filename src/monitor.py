import requests
import datetime
import os


class SiteMonitor:
    """
    Монитор сайтов.
    Проверяет список URL и записывает их в лог файл.
    """

    def __init__(self, sites=None):
        """
        При создании можно передать список сайтов.
        Если не передали - используется список по умолчанию.
        """
        if sites is None:
            # Список сайтов для проверки (можно менять)
            self.sites = [
                "https://www.google.com",
                "https://www.github.com",
                "https://www.python.org",
            ]

        else:
            self.sites = sites

        # Имя лог файла
        self.log_file = "site_status.log"

    def check_one_site(self, url):
        """
        Проверяет ОДИН сайт.
        Возвращает словарь с результатом:
        {
            "url": "https://...",
            "status": "OK" или "FAIL",
            "code": 200 или 0,
            "timestamp": "2026-05-22 19:15:00
        }
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Делаем HEAD-запрос (быстрее, чем GET - не качаем весь сайт)
            response = requests.head(url, timeout=10, allow_redirects=True)

            if response.status_code == 200:
                status = "OK"
            else:
                status = "FAIL"

            result = {
                "url": url,
                "status": status,
                "code": response.status_code,
                "timestamp": timestamp,
            }

        except requests.exceptions.RequestException:
            # Любая ошибка соединения -сайт не отвечает
            result = {
                "url": url,
                "status": "FAIL",
                "code": 0,
                "timestamp": timestamp,
            }

        return result

    def check_all_sites(self):
        """
        Проверяет ВСЕ сайты из списка.
        Записывает результат в лог-файл.
        Возвращает список результатов.
        """
        results = []
        print(f"=== Проверка сайтов: {datetime.datetime.now()} ===")

        for site in self.sites:
            print(f"Проверяю: {site} ...", end="")
            result = self.check_one_site(site)
            results.append(result)

            # Вывод в консоль
            if result["status"] == "OK":
                print("✅ OK")
            else:
                print(f"❌ FAIL (код: {result['code']})")

        # Запись в лог-файл
        self.write_log(results)
        return results

    def write_log(self, results):
        """
        Дописывает результаты в лог-файл.
        Если файла нет - создаёт.
        """
        with open(self.log_file, "a", encoding="utf-8") as f:
            for r in results:
                line = f"{r['timestamp']} | {r['url']} | "
                f.write(line + "\n")

        print(f"\nРезультаты записаны в файл: {self.log_file}")

    def read_log(self):
        """
        Читает лог-файл и возвращает его содержимое.
        Если файла нет - возвращает пустую строку.
        """
        if not os.path.exists(self.log_file):
            return "Лог-файл ещё не создан. Запустите check_all_sites()."

        with open(self.log_file, "r", encoding="utf-8") as f:
            return f.read()
