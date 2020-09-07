#-*- coding:utf-8 -*-
#*******************************************************************
#*******************************************************************
#*************************导入模块***********************************
#*******************************************************************
#*******************************************************************
from  PyQt4.QtGui  import *
from  PyQt4.QtCore  import *
from threading import Thread
import shutil
import math

import sys
import re
import urllib3
import os
import json
import urllib
import urllib2
import requests
import subprocess
import random

m4s_v=1
m4s_a=1
reload(sys)
sys.setdefaultencoding("utf-8")

ffmpeg="E:/bilibili_down/ffmpeg/bin/ffmpeg.exe"
ffplay="E:/bilibili_down/ffmpeg/bin/ffplay.exe"
ffprobe="E:/bilibili_down/ffmpeg/bin/ffprobe=.exe"
#*************************表头参数**************************
img_pos=""

global image_name
image_name=""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.bilibili.com/video/av17600853?from=search^&seid=14315525695693146901',
    'Origin': 'https://www.bilibili.com',
}

params = (
    ('e', 'ig8euxZM2rNcNbhzhwdVhoMzhzdVhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==^'),
    ('deadline', '1562133968^'),
    ('gen', 'playurl^'),
    ('nbs', '1^'),
    ('oi', '3659290398^'),
    ('os', 'cosu^'),
    ('platform', 'pc^'),
    ('trid', '5fd0f0bb71b94113babda9dc59275c83^'),
    ('uipk', '5^'),
    ('upsig', '01e98eff2f5db5f51baa8258235d7d30^'),
    ('uparams', 'e,deadline,gen,nbs,oi,os,platform,trid,uipk^'),
    ('mid', '0'),
)



#*******************************************************************
#*******************************************************************
#***************************布局类**********************************
#*******************************************************************
#*******************************************************************
class graphicsView(QGraphicsView):
    def __init__(self,parent=None):
        super(graphicsView,self).__init__(parent)
        #QObject.connect(self, SIGNAL('mousePressEvent()'),self.mousePressEvent)
        self.image=""
        QObject.connect(self, SIGNAL('mousePressEvent()'),self.mousePressEvent)

        

        
    def wheelEvent(self, event):
        
        global image_name
        self.image=image_name
        if(image_name!=""):
            value=event.delta()
            if event.delta() >= 0:
                self.width =self.image.width()
                self.height=self.image.height()
                if self.width< 1200:
                    self.width =self.width*1.5
                    self.height=self.height*1.5
                    pic=self.image.scaled(self.width,self.height,aspectRatioMode=Qt.KeepAspectRatio)
                    self.graphicsView.removeItem(self.item)
                    item1= QGraphicsPixmapItem(pic)

                    self.graphicsView= QGraphicsScene()
                    self.graphicsView.addItem(item1)                
                    self.setScene(self.graphicsView)
                    #self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                    self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setFrameShape(QFrame.NoFrame)
                    #self.setBackgroundBrush(QBrush(QColor(70, 170, 80)))
                            
                    self.item=item1
                    
                elif self.width< 300:
                    self.width =self.width*1.2
                    self.height=self.height*1.2
                    pic=self.image.scaled(self.width,self.height,aspectRatioMode=Qt.KeepAspectRatio)
                    self.graphicsView.removeItem(self.item)

                    self.graphicsView= QGraphicsScene()
                    item1= QGraphicsPixmapItem(pic)               
                    self.graphicsView.addItem(item1)                
                    self.setScene(self.graphicsView)
                    #self.setAlignment(Qt.AlignCenter and Qt.AlignTop)
                    self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setFrameShape(QFrame.NoFrame)
                    #self.setBackgroundBrush(QBrush(QColor(70, 170, 80)))
                    self.item=item1
            elif event.delta() <=  0:
                
        
                self.width =self.image.width()
                self.height=self.image.height()
                if self.width>800:
                    self.width =self.width*0.5
                    self.height=self.height*0.5
                    pic=self.image.scaled(self.width,self.height,Qt.IgnoreAspectRatio)
                    
                    self.graphicsView.removeItem(self.item)
            
             
                    self.graphicsView= QGraphicsScene()
                    
                    item1 = QGraphicsPixmapItem(pic)               
                    self.graphicsView.addItem(item1)
                    
                    self.setScene(self.graphicsView)
                    #self.setAlignment(Qt.AlignCenter or Qt.AlignTop)
                    self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setFrameShape(QFrame.NoFrame)
                    #self.setBackgroundBrush(QBrush(QColor(50, 200, 100)))
                    
                    
                    self.item=item1
                    
                    
                elif self.width>400:
                    self.width =self.width*0.75
                    self.height=self.height*0.75
                    pic=self.image.scaled(self.width,self.height,Qt.IgnoreAspectRatio)
                    
                    self.graphicsView.removeItem(self.item)
            
             
                    self.graphicsView= QGraphicsScene()
                    
                    item1 = QGraphicsPixmapItem(pic)               
                    self.graphicsView.addItem(item1)

                    self.setScene(self.graphicsView)
                    #self.setAlignment(Qt.AlignCenter or Qt.AlignTop)
                    self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                    self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    self.setFrameShape(QFrame.NoFrame)
                    #self.setBackgroundBrush(QBrush(QColor(50, 200, 100)))
                    
                    
                    self.item=item1
                    


            

        
 

                

           
                
#*******************************************************************
#*******************************************************************
#***************************拖拽类**********************************
#*******************************************************************
#*******************************************************************

class MyLineEdit(QLineEdit):
        def __init__( self, parent=None ):
            super(MyLineEdit, self).__init__(parent)
            self._parent=parent
        def dragEnterEvent( self, event ):
            
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()
        def dragMoveEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                event.acceptProposedAction()

        def dropEvent( self, event ):
            data = event.mimeData()
            urls = data.urls()
            if ( urls and urls[0].scheme() == 'file' ):
                filepath = str(urls[0].path())[1:]
                filepath=filepath.decode('utf-8')
                self.setText(filepath)
                name=filepath.split("/")[-1]+"_"+self._parent.createRandomString(5)
                self._parent.file_name.setText(name)

#*******************************************************************
#*******************************************************************
#***************************功能类**********************************
#*******************************************************************
#*******************************************************************
class bilibili_gui(QWidget):
    
    def __init__(self):
        super(bilibili_gui,self).__init__()

        #self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u"Vedio Download Tool_a")
        
        self.initUI()
    def initUI(self):
        #人员信息统计并从空添加，使用列表即可。
        #self._tree=Treeview()
        #self._list=Listview()

        down_address=QLabel(u'输入下载地址：')
        self.down_address=QLineEdit()
        analyze=QPushButton(u"解析")

        
        
        self._tree=graphicsView(self)
 
        
        
        save_adrss=QLabel(u'下载位置：')
        self.save_address=MyLineEdit(self)
        self.save_adrss_look=QPushButton(u"==>：")
        
        start_down=QPushButton(u"下载视频")
        comp_video =QPushButton(u"合并视频")
        del_viedo=QPushButton(u"清除缓存")
        open_video =QPushButton(u"缓存位置")

        file_name=QLabel(u'视频名称：')
        self.file_name=QLineEdit(u"")
        self.file_name.setPlaceholderText(u'自动获取')
        time_pos=QLabel(u"进度")
        self.time_pos=QLineEdit(u"0")
        self.pbar = QProgressBar()

        #print dir(self.pbar)

        
        #groupNameData.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        

        
        laty_1=QHBoxLayout()
        laty_1.addWidget(down_address)
        laty_1.addWidget(self.down_address)
        laty_1.addWidget(analyze)
     

        laty_2=QHBoxLayout()
        laty_2.addWidget(self._tree)
        
        
      

        laty_3=QHBoxLayout()
        laty_3.addWidget(save_adrss)
        laty_3.addWidget(self.save_address)
        laty_3.addWidget(self.save_adrss_look)


        laty_4=QHBoxLayout()
        laty_4.addWidget(file_name,1)
        laty_4.addWidget(self.file_name,7)
        laty_4.addWidget(time_pos,1)
        laty_4.addWidget(self.pbar ,2)

        laty_5=QHBoxLayout()
        laty_5.addWidget(start_down)
        laty_5.addWidget(comp_video)
        laty_5.addWidget(del_viedo)
        laty_5.addWidget(open_video)


        all_lay=QVBoxLayout()
        all_lay.addLayout(laty_1)
        all_lay.addLayout(laty_2)
        all_lay.addLayout(laty_3)
        all_lay.addLayout(laty_4)
        all_lay.addLayout(laty_5)


      
        self.setLayout(all_lay)
        
        self.resize(800,550)

        analyze.clicked.connect(self.resolve)
        self.save_adrss_look.clicked.connect(self.saveAdrss)
        start_down.clicked.connect(self.startDownload)
        comp_video.clicked.connect(self.compVideo)
        del_viedo.clicked.connect(self.delVideo)
        open_video.clicked.connect(self.openVideo)


        self.show()



    def down_load(self,www,i,exr,l):
        global m4s_v
        global m4s_a
        try:
            downpos=str(self.save_address.text()).decode('utf-8')
            
            if "http://upos-hz-mirrorbosu" in www: 
                new_name=downpos+"/" + self.SixNumber1(m4s_a)+str(exr)
                m4s_a=m4s_a+1
                print new_name+" \n"
            else: 
                new_name=downpos+"/" + self.SixNumber(m4s_v)+str(exr)
                m4s_v=m4s_v+1
                print new_name+" \n"
            if not os.path.exists(new_name):  
                request =  urllib2.Request(url=www, headers=headers)
                response = urllib2.urlopen(request)
                with open(new_name, "wb") as f:
                    f.write(response.read())
                    self.time_pos.setText(str(i)+"/"+str(l))
                    self.pbar.setValue(i)


        except Exception as e:
                print e
    def SixNumber(self,str_number):
        str_number=str(str_number)
        while(len(str_number)<4):
            str_number='0'+str_number
        return str_number
    def SixNumber1(self,str_number):
        str_number=str(str_number)
        while(len(str_number)<6):
            str_number='0'+str_number
        return str_number

    def startDownload(self):
        
        if str(self.down_address.text())=="" or str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入网址和下载地址，视频名称可不写")
            return

        currentPos=os.path.abspath(os.path.dirname(__file__))

        
        os.chdir(currentPos)
        url=str(self.down_address.text())
        
        response = requests.get(url, headers=headers, params=params)
        #reg=re.compile(r'(http://upos-hz-mirrorcosu.acgvideo.com.*?flv.*?uipk&mid=0|http://upos-hz-mirrorks3u.acgvideo.com.*?m4s.*?uipk&mid=0|http://upos-hz-mirrorbosu.acgvideo.com.*?m4s.*?uipk&mid=0|\
        #http://upos-hz-mirrorbosu.acgvideo.com.*?mp4.*?uipk&mid=0|http://upos-hz-mirrorcosu.acgvideo.com.*?mp4.*?uipk&mid=0|http://cn.*?.acgvideo.com.*?m4s.*?uipk&mid=0)')

        reg=re.compile(r'(http://upos-hz-mirrorcosu.acgvideo.com.*?flv.*?uipk&mid=0|http://upos-hz-mirrorks3u.acgvideo.com.*?m4s.*?uipk&mid=0|\
http://upos-hz-mirrorbosu.acgvideo.com.*?m4s.*?uipk&mid=0|http://cn-.*?-cu-v-\d{2}\.acgvideo.com.*?m4s.*?mid=0)')
        lt=re.findall(reg,response.text)

        lt=list(set(lt))
  
            
        title=re.findall("<title .*?>(.*?)</title>",response.text)

        title = re.sub("[~ ゜-゜&;❤？()]+".decode("utf8"), "".decode("utf8"),title[0])

        if title!="" and lt!=[]:
            self.file_name.setText(str(title).decode("utf-8"))
        else:
            QMessageBox.information(self,u"提示", u"解析失败，无法下载")
            return
        self.pbar .setMinimum(0)  
        self.pbar .setMaximum(len(lt))
            
        ttt=[]
        #print len(lt)
        reg=re.compile(r'http://.*?(.m4s).*?mid=0|http://.*?(.flv).*?uipk&mid=0|http://.*?(.mp4).*?uipk&mid=0')
        exrt=re.findall(reg,lt[0])[0]


        file_name=str(self.save_address.text())+"/"+ str(self.file_name.text())+".mp4"
        file_name=file_name.decode("utf-8")
        if os.path.exists(file_name):
            QMessageBox.information(self,u"提示", u"该文件已下载，请查看")
            return
            
        for ep in exrt:
            if ep!="":
                exr=ep

  
        if len(lt)<16:
            for i in range(len(lt)):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
        elif len(lt)<32:
            for i in range(0,16):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(16,len(lt)):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
        elif len(lt)<48:
            for i in range(0,16):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(16,32):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(32,len(lt)):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
        elif len(lt)<68:
            for i in range(0,16):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(16,32):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(32,48):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()
            ttt=[]
            for i in range(48,len(lt)):
                #down(lt[i],fort)
                t = Thread(target=self.down_load,args=(lt[i],i,exr,len(lt)))
                ttt.append(t)
            for tt in ttt:
                tt.start()
            for tt in ttt:
                tt.join()


        self.pbar.setValue(len(lt))
        history=[str(self.save_address.text()),str(title)]

        with open(ffpmpegRoot+"/cache/history.part", "w") as films:
            end = json.dumps(history, indent=4)
            films.write(end)

        self.time_pos.setText(u"完成")
        self.compVideo()
   
        #QMessageBox.information(self,u"提示", u"下载成功")
             

    def resolve(self):
        
        if str(self.down_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入网址")
            return
        currentPos=os.path.abspath(os.path.dirname(__file__))
        os.chdir(currentPos)
        url=str(self.down_address.text())
        response = requests.get(url, headers=headers, params=params)
        title=re.findall("<title .*?>(.*?)</title>",response.text)
        title = re.sub("[~ ゜-゜&;？❤()]+".decode("utf8"), "".decode("utf8"),title[0])
        name="cache/text.html"
        with open(name, "wb") as f:
            f.write((response.text).encode("utf-8"))
        
        
        reg = re.compile(r'(http://upos-hz-mirrorcosu.acgvideo.com.*?flv.*?uipk&mid=0|http://upos-hz-mirrorks3u.acgvideo.com.*?m4s.*?uipk&mid=0|\
http://upos-hz-mirrorbosu.acgvideo.com.*?m4s.*?uipk&mid=0|http://cn-.*?-cu-v-\d{2}\.acgvideo.com.*?m4s.*?mid=0)')
        
        lt= re.findall(reg,response.text)

        lt=set(lt)

        #for t in lt:
            #print t

        if title!="" and lt!=[]:
            self.loadImage(url)
            self.file_name.setText(str(title).decode("utf-8"))
            #QMessageBox.information(self,u"提示", u"解析完成")
        else:
            QMessageBox.information(self,u"提示", u"解析失败，无法下载")
            
            
    def loadImage(self,url):
        reg = re.compile(r'https.*?av(\d+)?.*?')
        try:
            av=re.findall(reg,url)[0]
            use_url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % (av,)
            urllib3.disable_warnings() 
            response = requests.get(use_url, headers=headers, verify=False) 
            content = json.loads(response.text)
            statue_code = content.get('code')
            if statue_code == 0:
                img_url=(content.get('data').get('pic'))
                exr=img_url.split(".")[-1]
                name=ffpmpegRoot+"/cache/image."+exr
                request =  urllib2.Request(url=img_url, headers=headers)
                response = urllib2.urlopen(request)
                with open(name, "wb") as f:
                    f.write(response.read())
            if os.path.exists(name):
                self._tree.image=QPixmap(name)
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)               
                self._tree.graphicsView.addItem(self._tree.item)                
                self._tree.setScene(self._tree.graphicsView)
                global image_name
                image_name=self._tree.image

                    
        except Exception as e:
            QMessageBox.information(self,u"提示", u"图像解析失败")

    def createRandomString(self,len):
        print ('wet'.center(10,'*'))
        raw = ""
        range1 = range(58, 65) # between 0~9 and A~Z
        range2 = range(91, 97) # between A~Z and a~z

        i = 0
        while i < len:
            seed = random.randint(48, 122)
            if ((seed in range1) or (seed in range2)):
                continue;
            raw += chr(seed);
            i += 1
        return raw
            
    def compVideo(self):

      
        title=str(self.file_name.text()).decode("utf-8")
        currentVideoPath = str(self.save_address.text()).decode("utf-8")

        
        video_list=os.listdir(currentVideoPath)

        #print video_list
        tag=0
        for ts in video_list:
            if ts.split(".")[-1]=="ts":
                if re.findall("(\d+_\d+.ts)",ts)!=[]:
                    f=open(currentVideoPath +"/file.txt","a+")
                    f.write("file \'"+ts+"\' \n")
                    f.close()
                    tag=1
            else:
                pass
                

        if tag==0:
            QMessageBox.information(self,u"提示", u"不存在合成列表")
            return

        os.chdir(currentVideoPath)
       
        
        save_pos=os.path.abspath(os.path.dirname(currentVideoPath))+"/"+title+".mp4"

        print save_pos

        if os.path.exists("file.txt"):
            if len(video_list) >= 1:
                cmd= ffmpeg+" -y -f concat -safe 0 -i file.txt  -c copy  "+save_pos
                
                #cmd=cmd.encode(sys.getfilesystemencoding())




                if "?" in cmd:
                    cmd=cmd.replace("?","")

                #print os.path.exists(title)

                print cmd
        
                
                if not os.path.exists(currentVideoPath+"/"+title+".mp4"):
                    subprocess.call(cmd.encode(sys.getfilesystemencoding()) , shell=True)
                    print('[视频合并完成]'.encode(sys.getfilesystemencoding()))
                    os.remove("file.txt")
                else:
                    reply = QMessageBox.question(self,u"提示",u"已存在是否覆盖？", QMessageBox.Yes|QMessageBox.No,QMessageBox.No)


                    if reply == QMessageBox.Yes:
                        subprocess.call(cmd.encode(sys.getfilesystemencoding()) , shell=True)
                        print('[视频合并完成]'.encode(sys.getfilesystemencoding()))
                        os.remove("file.txt")
                    else:
                        os.remove("file.txt")
                        return
                    QMessageBox.information(self,u"提示", u"合成成功")
                     
        else:

            
                QMessageBox.information(self,u"提示", u"错误！")
                
            
            
       
    def delVideo(self):

        if str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入视频储存目录")
            return
        
        currentVideoPath = str(self.save_address.text()).decode("utf-8")
        print currentVideoPath 
        
        os.chdir(currentVideoPath)
        
        video=os.listdir(currentVideoPath)
        del_video=[]
        for v in video:
            ts =re.findall("(\d+_\d+.ts|\d+_\d+.m4s|\d+_\d+.m4s|\d+_\d+.mp4|\d+_\d+.flv)",v)
            if ts!=[]:
                del_video.append(ts[0])

        #print del_video
        if del_video==[]:
            QMessageBox.information(self,u"提示", u"不存在可清除文件")
            return
        else:
            for d in del_video:
                os.remove(d)
                

        QMessageBox.information(self,u"提示", u"清除成功")
            

                
           
    def openVideo(self):
        
        if os.path.exists(ffpmpegRoot+"/cache/history.part"):
            with open(ffpmpegRoot+"/cache/history.part") as file:
                filedata= json.loads(file.read())
                filepos=filedata[0]
                filename= filedata[1]
        else:
            filepos=""
            filename=""
        if str(self.save_address.text())!="" and str(self.file_name.text())!="":
            path= str(self.save_address.text()).decode("utf-8")
            if os.path.isdir(path):
                os.startfile(path)
        elif str(self.save_address.text())!='' and str(self.file_name.text())=="":
            path= str(self.save_address.text()).decode("utf-8")
            self.file_name.setText(filename)
        elif str(self.save_address.text())=='' and str(self.file_name.text())!="":
            self.save_address.setText(filepos)
        else:
            self.save_address.setText(filepos)
            self.file_name.setText(filename)
            #os.startfile(filepos)

            
            

            
        
 
   
    def saveAdrss(self):
        #利用文件保存对话框获取文件的路径名称，将存在的json,txt文件拷贝至指定位置。
        
        
        filename = QFileDialog.getExistingDirectory()
        
        if filename:
            filename=str(filename).decode('utf-8')
            filename=filename.replace("\\",'/')
            self.save_address.setText(filename)
        else:
            pass
            #QMessageBox.information(self,u'提示页面',u'取消成功')



#*******************************************************************
#*******************************************************************
#***************************主函数***********************************
#*******************************************************************
#******************************************************************* 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    bili = bilibili_gui()
    bili.show()
    sys.exit(app.exec_())
