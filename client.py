import socket
import json

def getNewSocket(old: socket):
    if (old):
        old.close()
    new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 10000
    new.connect((host, port))
    return new

def sendReq(s: socket, req:dict):
    s.send(json.dumps(req).encode("utf-8"))

def recvRes(s: socket):
    res = json.loads(s.recv(1024).decode("utf-8"))
    return res

s = getNewSocket(None)
name = input("Please input your name:")
req = {'method': 'test', 'name': name} #测试姓名是否存在
sendReq(s, req)
res = recvRes(s)
if res['result'] == 'false': #新用户
    print("\nYou are new customer! Welcome")
    req = {'method': 'register', 'name': name} #注册请求
    s = getNewSocket(s)
    sendReq(s, req)
    res = recvRes(s)
    chain = res['chain']
    print(f"Here is you password chain. Take care of it. Do not use the firt OTP. Use it from the second. You must use it one by one. Once they are used up, server will give you a new chain.\n\n{chain}")
elif res['result'] == 'true': #老用户 登录
    pwd = input("Please input your OTP:")
    req = {'method': 'login', 'name': name, 'pwd': pwd}
    s = getNewSocket(s)
    sendReq(s, req)
    res = recvRes(s)
    if (res['result'] == 'false'):
        print("Wrong Password")
    elif (res['result'] == 'true'):
        print("Success. You Login in.")
        if 'newChain' in res:
            chain = res['newChain']
            print(f"Ops, you have used up your OPT. Don't worry, here is your new chain. :)\n{chain}")
s.close()