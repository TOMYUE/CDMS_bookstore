import requests
import threading
from urllib.parse import urljoin
from be import serve
from fe import conf

thread: threading.Thread = None


# 修改这里启动后端程序，如果不需要可删除这行代码
def run_backend():
    # rewrite this if rewrite backend
    serve.be_run(True)

def pytest_configure(config):
    global thread
    print("frontend begin test")
    thread = threading.Thread(target=run_backend)
    thread.start()

def pytest_unconfigure(config):
    global thread
    url = urljoin(conf.URL, "shutdown")
    try: 
        requests.get(url)
    except: 
        pass
    thread.join()
    print("frontend end test")
