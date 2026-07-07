class SchedulerService:
    def __init__(self, event_bus=None, log_manager=None): self.event_bus=event_bus; self.log_manager=log_manager; self.enabled=False
    def start(self): self.enabled=True
    def stop(self): self.enabled=False
    def tick(self):
        if self.enabled and self.event_bus: self.event_bus.emit('scheduler_tick', None)
