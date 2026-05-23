from src.monitor import SiteMonitor


def test_check_bad_url_returns_fail():
    """Несуществующий файл должен вернуть FAIL"""
    monitor = SiteMonitor()
    result = monitor.check_one_site("https://this.url.does.not.exist.local")
    assert result["status"] == "FAIL"
    assert result["code"] == 0


def test_check_real_url_returns_ok():
    """Настоящий сайт должен вернуть ОК."""
    monitor = SiteMonitor()
    result = monitor.check_one_site("https://www.google.com")
    assert result["status"] == "OK"
    assert result["code"] == 200


def test_monitor_has_default_sites():
    """При создании без параметров должен быть список сайтов."""
    monitor = SiteMonitor()
    assert len(monitor.sites) > 0
    assert "https://www.google.com" in monitor.sites
