#-*- coding:utf-8 -*-
#*******************************************************************
#*******************************************************************
#*************************导入模块***********************************
#*******************************************************************
#*******************************************************************
from  PyQt4.QtGui  import *
from  PyQt4.QtCore  import *
import re
import sys
import os
import json
import io
import urllib3
import requests
from io import BytesIO
from PIL import Image
from contextlib import closing
import threading

reload(sys)
sys.setdefaultencoding("utf-8")




global image_name
image_name=""

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.0',
    'Referer': 'https://www.bilibili.com/',

}




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
            #self.setDragEnabled(True)
            pass
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




       


#*******************************************************************
#*******************************************************************
#***************************功能类**********************************
#*******************************************************************
#*******************************************************************
class bilibili_(QWidget):
    
    def __init__(self):
        super(bilibili_,self).__init__()


        #self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u"Vedio Download Tool")

        
        self.initUI()
    def initUI(self):
        
        
        down_address=QLabel(u'输入下载地址：')
        self.down_address=QLineEdit()
        analyze=QPushButton(u"解析")

        
        
        self._tree=graphicsView(self)
 
        
        
        save_adrss=QLabel(u'下载位置：')
        self.save_address=MyLineEdit()
        self.save_adrss_look=QPushButton(u"==>：")
        
        self.start_down=QPushButton(u"下载视频")
        comp_video =QPushButton(u"合并视频")
        del_viedo=QPushButton(u"清除缓存")
        open_video =QPushButton(u"缓存位置")

        file_name=QLabel(u'视频名称：')
        self.file_name=QLineEdit(u"")
        self.file_name.setPlaceholderText(u'自动获取')
        time_pos=QLabel(u"进度")
        self.time_pos=QLineEdit(u"0")
        self.pbar = QProgressBar()





        
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
        laty_5.addWidget(self.start_down)
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
        self.start_down.clicked.connect(self.startDownload)
        comp_video.clicked.connect(self.compVideo)
        del_viedo.clicked.connect(self.delVideo)
        open_video.clicked.connect(self.openVideo)


    



        self.show()


    
    def print_file(self,video_address,new_name,headerss):
        
        self.start_down.setEnabled(False)
        print new_name
        try:
            if not os.path.exists(new_name):
                 with closing(requests.get(video_address,headers=headerss,stream=True)) as response:
                    chunk_size = 2048  # 单次请求最大值
                    content_size = int(response.headers['content-length'])  # 内容体总大小
                    data_count = 0
                    with open(new_name, "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            data_count = data_count + len(data)
                            now_jd = (float(data_count) / content_size) * 100
                            print("文件下载进度：%.2f%s".decode("utf-8") % (now_jd,"%"))
                 
                           
            self.pbar.setValue(100)
            self.start_down.setEnabled(True)
       
        except Exception as e:
                print e

        

    def startDownload(self):

        quality=720
        
        if str(self.down_address.text())=="" or str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入网址和下载地址，视频名称可不写")
            return

        url=str(self.down_address.text())
        title= str(self.file_name.text())
        response = requests.get(url, headers=headers)
    
        regt= re.compile(r'https://www.bilibili.com/video/av(\d+)/')
        av_num=re.findall(regt,response.text)

        aid=av_num[0]

        #print aid

        use_url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % (aid,)
        urllib3.disable_warnings() 
        response = requests.get(use_url, headers=headers, verify=False) 
        content = json.loads(response.text)

        cid = content["data"]["pages"][0]["cid"]

        #print cid

        url_api = 'https://api.bilibili.com/x/player/playurl?cid={}&avid={}&qn={}'.format(cid, aid, quality)
        #print url_api 
        htmls = requests.get(url_api, headers=headers).json()

       
        

        headerss={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36","Referer":"https://www.bilibili.com/video/"+aid}
        
        video_address = htmls['data']['durl'][0]['url']
        #print video_address

        downpos=str(self.save_address.text()).decode('utf-8')
        rstr = r"[\/\\\:\*\?\"\<\>\|♪]"  
        new_title = re.sub(rstr, "", title)  
        new_name=downpos+"/" + new_title+".flv"

        self.hide()
        

        t=threading.Thread(target=self.print_file,args=(video_address,new_name,headerss,))
        t.start()
        t.join()

        self.show()
        
        infoBox = QMessageBox(self)
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(u"下载完成！")
        infoBox.setWindowTitle("Information")
        infoBox.setStandardButtons(QMessageBox.Ok )
        infoBox.button(QMessageBox.Ok).animateClick(2*1000)      
        infoBox.exec_()


        


        
    def resolve(self):
        
        if str(self.down_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入网址！")
            return
        if str(self.save_address.text())=="":
            QMessageBox.information(self,u"提示", u"请输入下载地址！")
            return
        if "av" in str(self.down_address.text()):
            QMessageBox.information(self,u"提示", u"已解析完成！")
            return
        
        url=str(self.down_address.text())
        response = requests.get(url, headers=headers)
        
        title=re.findall("<title .*?>(.*?)</title>",response.text)
        title = re.sub("[~ ゜-゜&;？❤()]+".decode("utf8"), "".decode("utf8"),title[0])
        name="cache/text.html"
        with open(name, "wb") as f:
            f.write((response.text).encode("utf-8"))
        
        regt= re.compile(r'(https://www.bilibili.com/video/av\d+/)')
        av_num=re.findall(regt,response.text)

        aid=av_num[0]
        
        self.down_address.setText(aid)
        

 
        if title!="" and av_num!=[]:
            self.loadImage(av_num[0])
            self.file_name.setText(str(title).decode("utf-8"))
            history=[str(self.save_address.text()),str(title).decode("utf-8")]

            with open("cache/history.part", "w") as films:
                end = json.dumps(history, indent=4)
                films.write(end)
        else:
            QMessageBox.information(self,u"提示", u"解析失败，无法下载")
            
    def image_to_byte_array(self,html):
        byte_stream = BytesIO(html) 
        roiImg = Image.open(byte_stream)  
        imgByteArr = io.BytesIO()     
        roiImg.save(imgByteArr, format='PNG') 
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr

    def loadImage(self,url):
        try:
            reg = re.compile(r'https:/.*?av(\d+)/')
            av=re.findall(reg,url)[0]
            use_url = 'https://api.bilibili.com/x/web-interface/view?aid=%s' % (av,)
            urllib3.disable_warnings() 
            response = requests.get(use_url, headers=headers, verify=False) 
            content = json.loads(response.text)
  
            statue_code = content.get('code')
            if statue_code == 0:
                img_url=(content.get('data').get('pic'))
                #print img_url
                req = requests.get(img_url,headers=headers)
                html=req.content
                pic_address= self.image_to_byte_array(html)
            
                self._tree.image=QPixmap(self)
                self._tree.image.loadFromData(pic_address)
                self._tree.graphicsView= QGraphicsScene()            
                self._tree.item = QGraphicsPixmapItem(self._tree.image)               
                self._tree.graphicsView.addItem(self._tree.item)                
                self._tree.setScene(self._tree.graphicsView)
                global image_name
                image_name=self._tree.image
                    
        except Exception as e:
            QMessageBox.information(self,u"提示", u"图像解析失败")
            
    def compVideo(self):

        QMessageBox.information(self,u"提示", u"功能取消！")  
            
       
    def delVideo(self):
        QMessageBox.information(self,u"提示", u"功能取消！")  
                        
           
    def openVideo(self):
        
        if os.path.exists("cache/history.part"):
            with open("cache/history.part") as file:
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
    

            
            

            
        
 
   
    def saveAdrss(self):
        #利用文件保存对话框获取文件的路径名称，将存在的json,txt文件拷贝至指定位置。
        
        
        filename = QFileDialog.getExistingDirectory()
        
        if filename:
            filename=str(filename).decode('utf-8')
            filename=filename.replace("\\",'/')
            self.save_address.setText(filename)
        

#*******************************************************************
#*******************************************************************
#***************************主函数***********************************
#*******************************************************************
#******************************************************************* 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    bili = bilibili_()
    bili.show()
    sys.exit(app.exec_())
