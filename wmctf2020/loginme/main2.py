#coding:utf8
#编码:utf8
#A demo app that logins you.
#一个登录的演示应用程序。
from flask import Flask as Flask, request as request,render_template_string as render_template_string;
app = Flask(__name__)
__source__ = None
with open(__file__,"r",encoding="utf-8") as file:
    __source__ = file.read()
#I can't get the template folder for render_template to work:(
#So I am falling back to reading the template and using string formats with render_template_string.
#课本教的templates文件夹我权限搞不定啊
#所以我用读模板并且字符串格式化，应该没问题吧
templates = {}
with open("login.html","r",encoding="utf-8") as file:
    templates['login'] = file.read()

#template injection must have {{ and }}
#so I'm making sure {{ and }} cannot occurr
#SSTI必须要有{{和}}
#所以我确保{{和}}不能存在 
def waf(astr):
    return "{{" in astr and "}}" in astr

@app.route("/")
def index():
    return app.send_static_file("index.html")

#Allow the user to read the source code and maybe bypass my WAF？
#允许用户阅读源代码并绕过我的WAF？
@app.route("/code")
def source():
    return __source__

@app.route("/login",methods=['GET',"POST"])
def login():
    if(request.method == "GET"):
        return "What?"
    username = request.form['username']
    password = request.form['password']
    assert username is not None and password is not None;
    #I learned that render_template_string is unsafe
    #So I'm using some homemade WAF to make sure no template injection
    #render_template_string是不安全的
    #所以我使用自制WAF防止SSTI
    if(waf(username) or waf(password)):
        return "Oh no, you failed the WAF! Maybe <a href='/code'>read the source code</a> and find a way to bypass it?!"
        #"哦不，你失败了！也许<a href='/code'>查看源码</a>并且找到一个绕过WAF的方式？！"
    tpl=templates['login'].format(username=username,password=password)
    print(tpl)
    return render_template_string(tpl)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5001)