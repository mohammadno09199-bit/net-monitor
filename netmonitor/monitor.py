import psutil

class NetMonitor:
    def __init__(self):
        self.old_io = psutil.net_io_counters()

    def get_speed(self, interval):
        new_io = psutil.net_io_counters()
        
        up_delta = max(0, new_io.bytes_sent - self.old_io.bytes_sent)
        down_delta = max(0, new_io.bytes_recv - self.old_io.bytes_recv)
        
        up_speed = up_delta / interval
        down_speed = down_delta / interval
        
        self.old_io = new_io
        return up_delta, down_delta, up_speed, down_speed
