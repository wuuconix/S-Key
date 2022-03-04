from hashlib import md5
import socket
import json
import random
import string

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 10000
serversocket.bind((host, port))
serversocket.listen(5)
record = {} # 账号-密码字典
salt = {} # 账号-盐值字典
times = {} # 账号-成功登录次数字典

def getSalt(): #生成随机4位字符串 (字母+数字+标点里面选择4个字符)
    salt = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 4))
    return salt 

def h(w): #哈希函数
    return md5(w.encode('utf-8')).hexdigest()

def getChain(w: str): #得到密码链
    chain = []
    for i in range(5):
        hw = h(w)
        chain.append(hw)
        w = hw
    chain.reverse() #逆序密码链，让H^n(w)在最前面
    return chain

def sendRes(s: socket, res:dict): #服务端发送回应
    s.send(json.dumps(res).encode("utf-8"))

def recvReq(s: socket): #服务端接收请求
    req = json.loads(s.recv(1024).decode("utf-8"))
    return req

def log(msg: str): #记录日志
    with open("log.txt", "a") as f:
        f.write(json.dumps(msg))

while True:
    clientsocket,addr = serversocket.accept()      
    req = recvReq(clientsocket)
    print(req)
    log(req)
    if (req['method'] == 'test'):
        name = req['name']
        if name in record:
            res = {'result': 'true'}
        else:
            res = {'result': 'false'}
        sendRes(clientsocket, res)
    elif (req['method'] == 'register'):
        chain = getChain(req['name'] + getSalt()) #用户名加盐 作为种子生成chain
        record[name] = chain[0] #将H^n(w)加入密码字典中，舍弃其他的
        times[name] = 0 #登录次数置零
        res = {'chain': chain}
        sendRes(clientsocket, res)
    elif (req['method'] == 'login'):
        name = req['name']
        pwd = req['pwd']
        if h(pwd) == record[name]: #验证成功
            res = {'result': 'true'}
            times[name] += 1
            if (times[name] == 4): #用户用完了所有的OPT
                chain = getChain(name + getSalt())
                record[name] = chain[0]
                times[name] = 0
                res['newChain'] = chain
            else:
                record[name] = pwd #更新密钥
        else:
            res = {'result': 'false'}
        sendRes(clientsocket, res)
    clientsocket.close()