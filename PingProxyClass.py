import requests
import traceback
import time
import sys

from threading import *


class PingProxy:

    timeout_sec = 60
    sites_to_test = list()
    post_msg = ""
    # successful_get = list()
    # successful_post = list()
    # upload_string = ""
    lock = Lock()

    def add_responses_to_test_file(self, response_list, proxy, connection_type):
        self.lock.acquire()
        test_file = open("proxy_tests.txt", "a+")
        test_file.write(proxy + "\t" + connection_type + "\n\t" + response_list.__str__() + "\n")
        test_file.close()

        perfect = True
        for response in response_list:
            if response_list[response].find("Success") == -1:
                perfect = False
                break
        if perfect:
            perfect_file = open("perfect_proxies.txt", "a+")
            perfect_file.write(proxy + "\t" + connection_type + "\n")
            perfect_file.close()
        self.lock.release()

    def test_proxy_conn(self, proxy=""):
        if proxy == "" or proxy[:1] == "#":
            return
        proxy_details = proxy.split("\t")
        proxy = proxy_details[0] + ":" + proxy_details[1]
        print(proxy, end=" ")
        http_req = proxy_details[2].lower()
        print(http_req)
        proxies = {
            http_req:  http_req + '://' + proxy
        }
        site_responses = dict()
        for site in self.sites_to_test:
            try:
                req = requests.get(site, proxies=proxies, timeout=self.timeout_sec)
                site_responses[site] = "Success"
                print(str(proxies) + "success on " + site + " " + str(req.status_code))
            except requests.exceptions.ConnectTimeout:
                print(str(proxies) + ' ConnectTimeout on ' + site)
                site_responses[site] = "ConnectTimeout"
            except requests.exceptions.ProxyError:
                print(str(proxies) + ' ProxyError on ' + site)
                site_responses[site] = "ProxyError"
            except requests.exceptions.ReadTimeout:
                print(str(proxies) + ' ReadTimeout on ' + site)
                site_responses[site] = "ReadTimeout"
            except requests.exceptions.SSLError:
                print(str(proxies) + ' SSLError on ' + site)
                site_responses[site] = "SSLError"
            except IOError:
                traceback.print_exc()
                print(str(proxies) + ' IOError on ' + site)
                site_responses[site] = "IOError"
            except:
                traceback.print_exc()
                print(str(proxies) + ' ??? Error on ' + site)
                site_responses[site] = "??? Error"
        self.add_responses_to_test_file(site_responses, proxy, http_req)

    def test_proxy_speed(self, proxy):
        if proxy == "" or proxy[:1] == "#":
            return
        proxy_details = proxy.split("\t")
        proxy = proxy_details[0] + ":" + proxy_details[1]
        print(proxy, end=" ")
        http_req = proxy_details[2]
        print(http_req)
        proxies = {
            http_req: http_req + '://' + proxy
        }
        site_responses = dict()

        post_msg_bytes = sys.getsizeof(self.post_msg)

        for site in self.sites_to_test:
            try:
                start_time = time.time()
                req = requests.post(site, proxies=proxies, timeout=self.timeout_sec, data=self.post_msg)
                end_time = time.time()
                duration = end_time - start_time
                proxy_speed = (int((post_msg_bytes / 1024) / duration * 100)) / 100
                duration = (int(duration * 100)) / 100
                site_responses[site] = "Success: Upload time " + str(duration) + " for "+ str(post_msg_bytes / 1024) + \
                    " bytes (" + str(proxy_speed) + "kb/s)"
                print(str(proxies) + "success on " + site)
            except requests.exceptions.ConnectTimeout:
                print(str(proxies) + ' ConnectTimeout on ' + site)
                site_responses[site] = "ConnectTimeout"
            except requests.exceptions.ProxyError:
                print(str(proxies) + ' ProxyError on ' + site)
                site_responses[site] = "ProxyError"
            except requests.exceptions.ReadTimeout:
                print(str(proxies) + ' ReadTimeout on ' + site)
                site_responses[site] = "ReadTimeout"
            except requests.exceptions.SSLError:
                print(str(proxies) + ' SSLError on ' + site)
                site_responses[site] = "SSLError"
            except IOError:
                traceback.print_exc()
                print(str(proxies) + ' IOError on ' + site)
                site_responses[site] = "IOError"
            except:
                traceback.print_exc()
                print(str(proxies) + ' ??? Error on ' + site)
                site_responses[site] = "??? Error"
        self.add_responses_to_test_file(site_responses, proxy)
