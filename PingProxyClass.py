import requests
import traceback
import time

from threading import *


class PingProxy:

    timeout_sec = 60
    sites_to_test = list()
    # successful_get = list()
    # successful_post = list()
    # upload_string = ""
    lock = Lock()

    def add_responses_to_test_file(self, response_list, proxy):
        self.lock.acquire()
        test_file = open("proxy_tests.txt", "a+")
        test_file.write(proxy + "\n\t" + response_list.__str__() + "\n")
        test_file.close()

        perfect = True
        for response in response_list:
            if response_list[response] != "Success":
                perfect = False
                break
        if perfect:
            perfect_file = open("perfect_proxies.txt", "a+")
            perfect_file.write(proxy + "\n")
            perfect_file.close()
        self.lock.release()

    def test_proxy_conn(self, proxy=""):
        if proxy[:1] == "#":
            return
        proxy_details = proxy.split("\t")
        proxy = proxy_details[0] + ":" + proxy_details[1]
        print(proxy, end=" ")
        http_req = proxy_details[2]
        print(http_req)
        if proxy == "":
            return
        proxies = {
            http_req:  http_req + '://' + proxy
        }
        site_responses = dict()
        for site in self.sites_to_test:
            try:
                req = requests.get(site, proxies=proxies, timeout=self.timeout_sec)
                site_responses[site] = "Success"
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

    def testProxySpeed(self, proxy):
        print("non-functional method")
        if proxy == "":
            return
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            for site in self.sites_to_test:
                past = time.time()
                req = requests.get(site, proxies=proxies, timeout=self.timeout_sec)
                ellapsed_get = time.time() - past

                past = time.time()
                req = requests.post('http://verniy.xyz/proxytest/proxytest.php?ul=' + self.upload_string, proxies=proxies,
                    timeout=self.timeout_sec)
                ellapsed_post = time.time() - past

                # lock.acquire()
                # timed.append(
                #     proxy + '\t\t' + str(ellapsed_dl) + 's/1mb-download\t\t' + str(ellapsed_ul) + 's/0.456mb-upload')
                # success = open('success.txt', 'a+')
                # success.write(
                #     proxy + '\t\t' + str(ellapsed_dl) + 's/1mb-download\t\t' + str(ellapsed_ul) + 's/0.456mb-upload\n')
                # success.close()
                # lock.release()
            # except requests.exceptions.ConnectTimeout:
            #     print(str(proxies) + ' ConnectTimeout')
            # except  requests.exceptions.ProxyError:
            #     print(str(proxies) + ' ProxyError')
            # except  requests.exceptions.ReadTimeout:
            #     print(str(proxies) + ' ReadTimeout')
            # except IOError:
            #     traceback.print_exc()
            #     lock.release()
            #     print('io error')
        except:
            traceback.print_exc()
            print('general error')