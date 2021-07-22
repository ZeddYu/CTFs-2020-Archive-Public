
#coding:utf8
#编码:utf8
#A simple proxy that forward your request to a remote host.
#There is absolutely no vuln in this proxy!
#将请求转发到远程主机的简单代理。
#这个代理中绝对没有vuln！

#config
#配置部分
config = {
    #the remote host to forward to.
    #要转发到的远程主机。
    #"host":"http://127.0.0.1:5001/",    
    "host":"http://nginx/",  #I just learned nginx! Using proxy_pass with different server_name is fun! I can do unnecessary routines like user->nginx->this proxy->nginx->real backend with only one nginx server!
    我刚刚学会nginx！使用proxy_pass和不同的server_name是有趣！我可以做套娃路线像 用户->nginx->这个代理->nginx->真实的后端，只和一个nginx服务器！
}
blacklist_client_headers = ['Host','Proxy-Connection']
blacklist_server_headers = ['Connection']
#end config
#结束配置部分
from flask import Flask as Flask, request as request, abort as abort, make_response as make_response;
from requests import Session as requests;
from traceback import print_exc as print_exc;
requests = requests()
app = Flask(__name__)
__source__ = None
with open(__file__,"r",encoding="utf-8") as file:
    __source__ = file.read()

#Although there are no vuln, there may be bugs in this proxy:)
#If the user find one, tell the user to fix the bug themselves
# 虽然没有vuln，但此代理中可能存在错误：）
# 如果用户找到一个，告诉用户自己修复错误
@app.errorhandler(Exception)
def onerror(e): 
    #print_exc()
    return "Oops, error occurred! Maybe you can <a href='/source'>read the source code</a> and fix the bug for me?!"
    # "不好意思，发生了错误！也许你可以<a href='/source'>阅读源代码</a>帮我解决这个问题？！"

#Allow the user to read the source code and fix the bugs.
#允许用户阅读源代码并修复错误。
@app.route("/source")
def source():
    return __source__

#Does proxy jobs.
#做代理工作。
@app.route('/<path:path>',methods=["GET","P0ST"]) #I copied this line from a book, I hope it works:) #我从教材上抄的这句话，我希望它工作：）
def proxy(path):
    try:
        url = config['host'] + path
        headers = dict(request.headers)
        for i in blacklist_client_headers:
            if i in headers:
                del headers[i]
        makenRequest = None
        if(request.method == "POST"):
            data = request.get_data()
            makenRequest = requests.post(url,data=data,headers=headers)
        else:
            makenRequest = requests.get(url,headers=headers)
        resp = make_response(makenRequest.text)
        resp.headers = dict(makenRequest.headers)
        for i in blacklist_server_headers:
            if i in resp.headers:
                del resp.headers[i]
        return resp
    except:
        raise

@app.route("/")
def proxy_root():
    return proxy("")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
