import socket
import threading
import peewee
from datetime import datetime

from models import IPTask, PreProxy
from utils.funcs import generate_ip


class PortScan(object):
    def __init__(self, max_threads=1000):
        self.max_threads = max_threads
        self.exit_flag = False
        self.signal_lock = threading.Lock()

    def run(self):
        for i in range(self.max_threads):
            t = threading.Thread(target=self.main)
            try:
                t.start()
            except BaseException:
                print "Max Number of threads:%s" % i
                break

    def abort(self):
        with self.signal_lock:
            self.exit_flag = True

    def main(self):
        while not self.exit_flag:
            try:
                now = datetime.now().strftime("%Y-%m-%d")
                task = IPTask.select() \
                    .where((IPTask.last_test_date == None) | (IPTask.last_test_date < now)) \
                    .order_by(IPTask.last_test_date.asc()).get()
            except IPTask.DoesNotExist:
                print "Tasks Finished, aborting..."
                self.abort()
                continue
            start_ip = task.start_ip
            t_range = task.t_range
            for ip in generate_ip(start_ip, t_range):
                for port in xrange(1, 65535):
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(1)
                    result = s.connect_ex((ip, port))
                    if result == 0:
                        # Connection Success
                        if not PreProxy.select().where(PreProxy.ip == ip, PreProxy.port == port).exists():
                            PreProxy.create(ip=ip, port=port)
                    s.close()
            task.last_test_date = datetime.now()
            task.save()


class SlaveService(object):
    def __init__(self, num_port_scan=500, num_proxy_scan=1000):
        self.num_proxy_scan = num_proxy_scan
        self.num_port_scan = num_port_scan

    def run(self):
        portscan = PortScan(self.num_port_scan)
        portscan.run()

if __name__ == "__main__":
    service = SlaveService(1, 1)
    service.run()
