
import PingProxyClass
import sys
from threading import *

if __name__ == "__main__":

    ips = open('proxies.txt', 'r+')
    ips = ips.read().split('\n')
    sites = open('sites.txt', 'r+')
    sites = sites.read().split('\n')

    threads = []

    proxy_pinger = PingProxyClass.PingProxy()
    proxy_pinger.timeout_sec = 60
    proxy_pinger.sites_to_test = sites

    for proxy in ips:
        thread = Thread(target=proxy_pinger.test_proxy_conn, args=[str(proxy)])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    # threads = []
    #
    # proxy_pinger = PingProxyClass.PingProxy()
    # proxy_pinger.timeout_sec = 60
    # proxy_pinger.sites_to_test = sites
    # for i in range(0,30000):
    #     proxy_pinger.post_msg = proxy_pinger.post_msg + "0"
    # for proxy in ips:
    #     thread = Thread(target=proxy_pinger.test_proxy_speed, args=[str(proxy)])
    #     thread.start()
    #     threads.append(thread)
    #
    # for thread in threads:
    #     thread.join()

    input('Finished - Press anykey')