#-*- coding:gbk -*-
import urllib2
import re,sys,os
import json
from requests.packages import urllib3
import ssl
from threading import Thread

#reload(sys)
#sys.setdefaultencoding("gbk")



context = ssl._create_unverified_context()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'referer': 'https://live.fc2.com/16643464/',

}
def SixNumber(str_number,lent):
        str_number=str(str_number)
        while(len(str_number)<lent):
            str_number='0'+str_number
        return str(str_number)
def down_file(singer_url,channel):
    if not os.path.isdir(channel):
        os.makedirs(channel)
    #print num,singer_url+"\n"
    try:
        name= SixNumber(singer_url.split(".ts")[0].split("/")[-1],8)+"_"+ channel +".ts"
        print name + " " +channel + " " + "channel"+ "\n"
        req = urllib2.Request(singer_url, headers = headers)
        response = urllib2.urlopen(req,context=context,timeout=2)
        data = (response.read())
        
        
        if not os.path.exists(channel+"/"+name):
            with open(channel+"/"+name,"wb") as f:
                f.write(data)
    except Exception as e:
        print "error because->",e
 

def get_down_data(url):
    #url=raw_input(u"请输入关键fc2_url_2:\n")
    print url
    



    enable_proxy = True
    proxy_handler = urllib2.ProxyHandler({"http" : 'http://127.0.0.1:54184'})
    #proxy_handler = urllib2.ProxyHandler({"http" : 'http://127.0.0.1:1080'})

    null_proxy_handler = urllib2.ProxyHandler({})
     
    if enable_proxy:
        opener = urllib2.build_opener(proxy_handler)
    else:
        opener = urllib2.build_opener(null_proxy_handler)
        
     
    urllib2.install_opener(opener)

    i=0
    while True:
        i+=1

        try:
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req,context=context,timeout=2)
            text = (response.read())
        except urllib2.urlerror as e:
            if hasattr(e,'code'):
                print ('error code:',e.code)
                return
            elif hasattr(e,'reason'):
                print 'reason:',e.reason
                return
        finally:
            if response:
                response.close()            
   
 
        pattern = re.compile(r'(https://\S+.live.fc2.com/\S+&hash=\w+)')
        ts_list = pattern.findall(text)

        reg = re.compile(r'https://hls.live.fc2.com/hls/(\d+)/32/\S+')

        channel= reg.findall(url)[0]

       
        

   


        thread_list=[]
        for singer_url in range(len(ts_list)):
            #print ts_list[singer_url]
            t = Thread(target=down_file,args=((ts_list[singer_url]),channel,))
            thread_list.append(t)


        for t_p in thread_list:
            t_p.start()
        for t_p in thread_list:
            t_p.join()

def read_list():
    with open("url.txt","rb") as f:
        txt_list=f.readlines()
    return txt_list
def chanel_list(txt):
    channel_list=[]
    for url in txt:
        reg = re.compile(r'https://hls.live.fc2.com/hls/(\d+)/32/\S+')
        channel= reg.findall(url)[0]
        channel_list.append(channel)
    return channel_list

def display_menu(channel,data):
    i=0
    print (u"请选择channel:\n")
    for c in channel:
        print ("    %d --> %s\n"% (i,c))
        i+=1
    num=input("请从上面选择一个数字：\n")
    url=data[num]
    return url

             
        
if __name__ == "__main__":
    data=read_list()
    channel=chanel_list(data)
    url=display_menu(channel,data)
    get_down_data(url)           


    








