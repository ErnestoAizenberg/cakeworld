import sys
from datetime import datetime
from functools import wraps


class CustomLogger:
    def __init__(self, debug=False):
        self.debug = debug
        self.start_times = {}  # Для хранения времени начала операций
        self.metrics = {
            "socketio_events": {},
            "database_operations": {},
            "total_messages_sent": 0,
            "total_messages_received": 0,
        }

    def log(self, message, level="INFO"):
        if self.debug:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{level}] {message}"
            if level == "WARNING":
                # Выводим предупреждения красным цветом
                log_message = f"\033[91m{log_message}\033[0m"
            print(log_message, file=sys.stderr)

    def start_timer(self, operation_name):
        if self.debug:
            self.start_times[operation_name] = datetime.now()

    def end_timer(self, operation_name):
        if self.debug and operation_name in self.start_times:
            elapsed_time = (
                datetime.now() - self.start_times[operation_name]
            ).total_seconds()
            self.log(f"Operation '{operation_name}' took {elapsed_time:.3f} seconds")
            del self.start_times[operation_name]

    def track_socketio_event(self, event_name):
        if self.debug:
            if event_name not in self.metrics["socketio_events"]:
                self.metrics["socketio_events"][event_name] = 0
            self.metrics["socketio_events"][event_name] += 1
            self.log(f"Socket.IO event '{event_name}' triggered")

    def track_database_operation(self, operation_name):
        if self.debug:
            if operation_name not in self.metrics["database_operations"]:
                self.metrics["database_operations"][operation_name] = 0
            self.metrics["database_operations"][operation_name] += 1
            self.log(f"Database operation '{operation_name}' executed")

    def track_message_sent(self):
        if self.debug:
            self.metrics["total_messages_sent"] += 1
            self.log("Message sent")

    def track_message_received(self):
        if self.debug:
            self.metrics["total_messages_received"] += 1
            self.log("Message received")

    def print_metrics(self):
        if self.debug:
            self.log("=== Metrics ===")
            for metric, value in self.metrics.items():
                self.log(f"{metric}: {value}")
            self.log("===============")

    def warn_if_inefficient(self, operation_name, threshold=1.0):
        if self.debug and operation_name in self.start_times:
            elapsed_time = (
                datetime.now() - self.start_times[operation_name]
            ).total_seconds()
            if elapsed_time > threshold:
                self.log(
                    f"Warning: Operation '{operation_name}' is inefficient (took {elapsed_time:.3f} seconds)",
                    level="WARNING",
                )
