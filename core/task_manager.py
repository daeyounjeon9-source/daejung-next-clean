class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, callback):
        self.tasks.append({"name": name, "callback": callback})

    def run_all(self):
        results = []
        for task in self.tasks:
            results.append((task["name"], task["callback"]()))
        return results
