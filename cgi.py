import requests
from requests.auth import *
import Luzinfo
import time
import datetime
import json
import threading
import logging
import configparser

Luzinfo.printLuzinfo("medicine Title setter","2023-01-11")
logging.basicConfig(filename="log.log", level=logging.INFO)
config=configparser.ConfigParser()
path='cgiconf.ini'
config.read(path)
medicine_url=config['config']['thirdurl']
testjson="""{
    "code": 0,
    "data": {
        "setlinfo": [
            {
                "setl_time": "2023-01-11 09:59:06",
                "feeinfo": {
                    "fee": [
                        {
                            "hilist_name": "知柏地黄丸/仲景",
                            "hilist_code": "301229897",
                            "bkkp_sn": "2"
                        },
                        {
                            "hilist_name": "口炎清颗粒",
                            "hilist_code": "301304655",
                            "bkkp_sn": "1"
                        }
                    ]
                },
                "jslsh": "P330522006722023011020099368441",
                "fixmedins_code": "P33052200672",
                "psn_no": "33050099000010000001689700",
                "mdtrt_id": "330000167334638726901198550858",
                "mdtrt_cert_no": "EE838411X",
                "fixmedins_name": "长兴滨海大药房",
                "setl_id": "330000167334638789600938673675",
                "psn_name": "冯茹春"
            }
        ]
    },
    "message": "成功"
}"""

def encode_Init(ip,username,password):#打开自定义标题，编码混合，预览混合
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].EncodeBlend=true",auth=HTTPDigestAuth(str(username),str(password))).text) #编码混合
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].PreviewBlend=true",auth=HTTPDigestAuth(str(username),str(password))).text)#预览混合
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].Rect[1]=0",auth=HTTPDigestAuth(str(username),str(password))).text)#坐标
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].Rect[0]=0",auth=HTTPDigestAuth(str(username),str(password))).text)#坐标
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].TextAlign=0",auth=HTTPDigestAuth(str(username),str(password))).text)#左对齐


def title_Set(ip,username,password,text):#设置自定义标题文本
    print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),requests.get("http://"+str(ip)+"/cgi-bin/configManager.cgi?action=setConfig&VideoWidget[0].CustomTitle[0].Text="+str(text),auth=HTTPDigestAuth(str(username),str(password)),timeout=5).text)

def get_Medicine(istest=0,starttime="2023-01-10 18:15:00",endtime="2023-01-10 18:15:00"):
    if(istest):#调试模式
        return testjson
    else:
        data={"data":{"begntime":starttime,"endtime":endtime}}
        print(medicine_url,starttime,endtime)
        logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 请求三方"+str(starttime)+str(endtime))
        resp=requests.post(url=medicine_url,json=data,timeout=5).text
        print(resp)
        return resp
def publish_Osd(record):
    logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : "+'下发OSD',str(record))
    i=record
    recordtime=i['setl_time']
    while(1):
        now=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : "+recordtime,now)
        print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),(recordtime,now))
        if(now>=recordtime):
            title_text=''
            title_text=title_text+'刷卡时间:\t'+i['setl_time']+'\n'
            title_text=title_text+'序列号:\t'+i['jslsh']+'\n'
            title_text=title_text+'姓名:\t'+i['psn_name']+'\n'
            title_text=title_text+'人员编号:\t'+i['psn_no']+'\n'
            title_text=title_text+'就诊ID:\t'+i['mdtrt_id']+'\n'
            feeinfo=''
            for j in i['feeinfo']['fee']:
                feeinfo=feeinfo+j['hilist_name']+' '+j['hilist_code']+' '+j['bkkp_sn']+'\n'
            title_text=title_text+'购药清单:\n'+feeinfo
            ip=config['camera'][i['fixmedins_code']]
            camerauser=config['config']['camerauser']
            camerapassword=config['config']['camerapassword']
            camerakeep=config['config']['keeptime']
            title_text=title_text.replace('\n','|')
            title_Set(ip,camerauser,camerapassword,title_text)
            encode_Init(ip,camerauser,camerapassword)
            logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 打开OSD"+ip)
            print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 打开OSD"+ip)
            logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 设置OSD"+ip,title_text)
            print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 设置OSD"+ip,title_text)
            time.sleep(int(camerakeep))
            title_Set(ip,camerauser,camerapassword,' ')
            logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 置空OSD"+ip)
            print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : 置空OSD"+ip)
            return 0
        else:
            print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),'未到时间,等待')
            time.sleep(1)

def main():
    sleeptime=config['config']['requestssleep']#两次请求间隔，秒
    while(1):
        try:
	        nowtime=datetime.datetime.now()
	        last=nowtime+datetime.timedelta(seconds=-6) 
	        medicine_list=json.loads(get_Medicine(istest=0,starttime=datetime.datetime.strftime(last,'%Y-%m-%d %H:%M:%S'),endtime=datetime.datetime.strftime(nowtime,'%Y-%m-%d %H:%M:%S')))['data']['setlinfo']  #调用正式接口
	        #medicine_list=json.loads(get_Medicine(istest=1))['data']['setlinfo']  #调用测试数据
	        logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : "+str(medicine_list))
	        for i in medicine_list:
	            threading.Thread(target=publish_Osd,args=(i,)).start()
	            
	        
	        time.sleep(int(sleeptime))
        except:
             print(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')),"请求第三方接口出错")
             logging.info(str(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))+" : "+"请求第三方接口出错")
main()
#encode_Init('33.156.242.208','admin','a12345678@')
