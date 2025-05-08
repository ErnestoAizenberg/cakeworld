import subprocess

from flask import render_template_string


class SitePerformanceChecker:
    def __init__(self, app):
        self.app = app
        self.configure_site_performance()

    def list_routes(self):
        routes = []
        for rule in self.app.url_map.iter_rules():
            # Игнорируем статические маршруты
            if rule.endpoint not in ["static"]:
                routes.append(rule.rule)
        return routes

    def measure_time(self, url):
        # Используем subprocess для выполнения curl и получения времени ответа
        result = subprocess.run(
            ["curl", "-o", "/dev/null", "-s", "-w", "%{time_total}", url],
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())

    def configure_site_performance(self):
        @self.app.route("/performance", methods=["GET", "POST"])
        def site_speed():
            all_routes = self.list_routes()
            statistics = []

            for route in all_routes:
                url = f"http://127.0.0.1:5000{route}"
                load_time = self.measure_time(url)
                statistics.append((route, load_time))

            # Сортировка статистики по времени загрузки
            statistics.sort(key=lambda x: x[1])

            load_times = [time for _, time in statistics]
            average_time = sum(load_times) / len(load_times) if load_times else 0
            min_time = min(load_times) if load_times else 0
            max_time = max(load_times) if load_times else 0

            # HTML-шаблон
            html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Site Performance Statistics</title>
                <style>
                    table {width: 100%; border-collapse: collapse;}
                    th, td {border: 1px solid #ddd; padding: 8px;}
                    th {background-color: #f2f2f2;}
                </style>
            </head>
            <body>
                <h1>Performance Statistics</h1>
                <table>
                    <tr>
                        <th>URL</th>
                        <th>Load Time (seconds)</th>
                    </tr>
                    {% for url, time in statistics %}
                    <tr>
                        <td>{{ url }}</td>
                        <td>{{ time }}</td>
                    </tr>
                    {% endfor %}
                </table>
                <p>Average Load Time: {{ average_time }} seconds</p>
                <p>Min Load Time: {{ min_time }} seconds</p>
                <p>Max Load Time: {{ max_time }} seconds</p>
                <p>Total Routes: {{ total_routes }}</p>
            </body>
            </html>
            """
            return render_template_string(
                html,
                statistics=statistics,
                average_time=average_time,
                min_time=min_time,
                max_time=max_time,
                total_routes=len(all_routes),
            )
