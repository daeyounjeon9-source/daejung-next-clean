class NotificationService:
    def __init__(self, event_bus=None, log_manager=None): self.event_bus=event_bus; self.log_manager=log_manager
    def notify(self, message, level='INFO'):
        if self.log_manager: self.log_manager.add_log(message, level)
        if self.event_bus: self.event_bus.emit('notification', {'message':message,'level':level})
