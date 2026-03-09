import json
import threading


class JSONExporter:

    def __init__(self, filename="products.json"):
        self.filename = filename
        self.lock = threading.Lock()
        self.file = open(self.filename, "a", encoding="utf-8")

    def export(self, item):

        with self.lock:
            line = json.dumps(dict(item), ensure_ascii=False)
            self.file.write(line + "\n")
            self.file.flush()

    def close(self):

        if not self.file.closed:
            self.file.close()