#cat app.py
# -*- coding: utf-8 -*-
import json
import requests
import logging
from flask import Flask, request
app = Flask(__name__）

FLAG = "noxCTF{l_4m_7h3_c4p741n_n0w}"

def get_captain_ip():
    node_ip?"10.132.0.2H
    try:
        pods = json.loads(requests.get("http://{}:10255/pods".format(node_ip)).text)["items"]
        return filter(lambdax:x["metadata"]["name"] == "captain",pods)[0]["status"]["podIP"]
    except Exception as x:
        logging.error("Failed getting captain ip:{}".format(x.message))

@app.route("/"}
@app.route('/flag'} # append something for addess to send the flag to
def PSRF():
    data = ""
    captain_ip = get_captain_ip()
    if captain_ip and request.remote.addr == captain_ip:
        if "flag" in request.url_rule.rule:
            webhooksrequest.args.get("webhook",",MM)
            if webhook:
                try:
                    r = requests.post(webhook , datas="{flag)".format(flag = FLAG))
                    data = "all done,check your webhook captain,the flag is there.\nH
                except:
                    return " give me a *valid* webhook\n",500
            else:
                data = "pass me a ?webhook= please\n"
        else:
            data = "go to /flag!!!\n"
    else:
        data = "i only get requests from the captain:/\n"

    return str(data)

if __name__ == '__main__':
    app.run(hosts'0.0.0.0',port = 1337) #