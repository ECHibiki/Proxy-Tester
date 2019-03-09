import requests
import traceback
import time
import sys
import socks

from threading import *


class PingProxy:

    timeout_sec = 60
    sites_to_test = list()
    post_msg = ""
    # successful_get = list()
    # successful_post = list()
    # upload_string = ""
    lock = Lock()
    sock_type = {"socks4": socks.SOCKS4, "SOCKS4": socks.SOCKS4, "socks5": socks.SOCKS5, "SOCKS5": socks.SOCKS5}

    def add_responses_to_test_file(self, response_list, ip, port, connection_type):
        self.lock.acquire()
        proxy = ip + ":" + port
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
        ip = proxy_details[0]
        port = proxy_details[1]
        req_type = proxy_details[2].lower()
        http_type = req_type.find("http") > -1
        sockn = None
        proxies = None
        if http_type:
            proxy = ip + ":" + port
            proxies = {
                "http":  "http://" + proxy,
                "https":  "https://" + proxy,
            }
        else:
            sockn = socks.socksocket()
            sockn.set_proxy(self.sock_type[req_type], str(ip), int(port))
            headers = b"GET"

        site_responses = dict()
        for site in self.sites_to_test:
            try:
                if http_type:
                    assert sockn is None
                    req = requests.get(site, proxies=proxies, timeout=self.timeout_sec, verify=False)
                    print(req)
                else:
                    assert proxies is None
                    sockn.connect((site, 80))
                    sockn.sendall(headers)
                    print(sockn.recv(4096))
                site_responses[site] = "Success"
                print(ip + ":" + port + " " + req_type + " " + "success on " + site)
            except requests.exceptions.ConnectTimeout:
                print(ip + ":" + port + " " + req_type + " " + ' requests.ConnectTimeout on ' + site)
                site_responses[site] = "requests.ConnectTimeout"
            except requests.exceptions.ProxyError:
                print(ip + ":" + port + " " + req_type + " " + ' requests.ProxyError on ' + site)
                site_responses[site] = "requests.ProxyError"
            except requests.exceptions.ReadTimeout:
                print(ip + ":" + port + " " + req_type + " " + ' requests.ReadTimeout on ' + site)
                site_responses[site] = "requests.ReadTimeout"
            except requests.exceptions.SSLError:
                print(ip + ":" + port + " " + req_type + " " + ' requests.SSLError on ' + site)
                site_responses[site] = "requests.SSLError"
            except socks.ProxyConnectionError:
                traceback.print_exc()
                print(ip + ":" + port + " " + req_type + " " + ' socks.ProxyConnectionError on ' + site)
                site_responses[site] = "socks.ProxyConnectionError Error"
            except IOError:
                traceback.print_exc()
                print(ip + ":" + port + " " + req_type + " " + ' IOError on ' + site)
                site_responses[site] = "IOError"
            except:
                traceback.print_exc()
                print(ip + ":" + port + " " + req_type + " " + ' ??? Error on ' + site)
                site_responses[site] = "??? Error"
        self.add_responses_to_test_file(site_responses, ip, port, req_type)

    # def test_proxy_speed(self, proxy):
    #     if proxy == "" or proxy[:1] == "#":
    #         return
    #     proxy_details = proxy.split("\t")
    #     proxy = proxy_details[0] + ":" + proxy_details[1]
    #     print(proxy, end=" ")
    #     http_req = proxy_details[2]
    #     print(http_req)
    #     proxies = {
    #         http_req: http_req + '://' + proxy
    #     }
    #     site_responses = dict()
    #
    #     post_msg_bytes = sys.getsizeof(self.post_msg)
    #
    #     for site in self.sites_to_test:
    #         try:
    #             start_time = time.time()
    #             req = requests.post(site, proxies=proxies, timeout=self.timeout_sec, data=self.post_msg)
    #             end_time = time.time()
    #             duration = end_time - start_time
    #             proxy_speed = (int((post_msg_bytes / 1024) / duration * 100)) / 100
    #             duration = (int(duration * 100)) / 100
    #             site_responses[site] = "Success: Upload time " + str(duration) + " for "+ str(post_msg_bytes / 1024) + \
    #                 " bytes (" + str(proxy_speed) + "kb/s)"
    #             print(ip + ":" + port + " " + req_type + " " + "success on " + site)
    #         except requests.exceptions.ConnectTimeout:
    #             print(ip + ":" + port + " " + req_type + " " + ' ConnectTimeout on ' + site)
    #             site_responses[site] = "ConnectTimeout"
    #         except requests.exceptions.ProxyError:
    #             print(ip + ":" + port + " " + req_type + " " + ' ProxyError on ' + site)
    #             site_responses[site] = "ProxyError"
    #         except requests.exceptions.ReadTimeout:
    #             print(ip + ":" + port + " " + req_type + " " + ' ReadTimeout on ' + site)
    #             site_responses[site] = "ReadTimeout"
    #         except requests.exceptions.SSLError:
    #             print(ip + ":" + port + " " + req_type + " " + ' SSLError on ' + site)
    #             site_responses[site] = "SSLError"
    #         except IOError:
    #             traceback.print_exc()
    #             print(ip + ":" + port + " " + req_type + " " + ' IOError on ' + site)
    #             site_responses[site] = "IOError"
    #         except:
    #             traceback.print_exc()
    #             print(ip + ":" + port + " " + req_type + " " + ' ??? Error on ' + site)
    #             site_responses[site] = "??? Error"
    #     self.add_responses_to_test_file(site_responses, proxy)
