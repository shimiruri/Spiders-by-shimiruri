from proxies_settings import *
from multiprocessing import Process
from proxies_test import Test
from proxies_getter import Getter
from proxies_api import app
import time


class Scheduler(object):
    def test_scheduler(self):
        tester = Test()
        while True:
            print("Start Test Scheduler!!!")
            tester.run()
            time.sleep(test_cycle)

    def getter_scheduler(self):
        getter = Getter()
        while True:
            print("Proxy Getter is running!!!")
            getter.get_proxies()
            time.sleep(getter_cycle)

    def api_scheduler(self):
        app.run(api_host, api_port)

    def run(self):
        print("Start Proxies Pool!!!")

        if test_enable:
            test_process = Process(target=self.test_scheduler)
            test_process.start()

        if getter_enable:
            getter_process = Process(target=self.getter_scheduler)
            getter_process.start()

        if api_enable:
            api_process = Process(target=self.api_scheduler)
            api_process.start()
