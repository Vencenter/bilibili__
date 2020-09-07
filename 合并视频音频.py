#!/usr/bin/env Python
#-*- coding:utf-8-*-
#*******************************************************************
#*******************************************************************
#*************************导入模块***********************************
#*******************************************************************
#*******************************************************************
from  PyQt4.QtGui  import *
from  PyQt4.QtCore  import *

import sys
import os
import subprocess

reload(sys)
sys.setdefaultencoding("utf-8")

ffmpeg="E:/pic_image/H_Player/ffmpeg/bin/ffmpeg.exe"

class MyLineEdit(QLineEdit):
        def __init__( self, parent=None ):
            super(MyLineEdit, self).__init__(parent)
            #self.setDragEnabled(True)
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
                if self._parent!=None:
                    self._parent.setData()




       


#*******************************************************************
#*******************************************************************
#***************************功能类**********************************
#*******************************************************************
#*******************************************************************
class CompFile_(QWidget):

    
    
    def __init__(self):
        super(CompFile_,self).__init__()
        self.setWindowTitle(u"Vedio Comp Tool")
        self.initUI()
        
    def initUI(self):
        
        
        vedio_address=QLabel(u'视频地址：')
        self.vedio_address=MyLineEdit(self)

        audio_address=QLabel(u'音频地址：')
        self.audio_address=MyLineEdit()

        save_address=QLabel(u'储存位置：')
        self.save_address=MyLineEdit()

        save_name=QLabel(u'视频名称：')
        self.save_name=QLineEdit()

        
        comp_button =QPushButton(u"合并视频")
        root_button =QPushButton(u"目录位置")

     





        
        laty_1=QHBoxLayout()
        laty_1.addWidget(vedio_address)
        laty_1.addWidget(self.vedio_address)

     

        laty_2=QHBoxLayout()
        laty_2.addWidget(audio_address)
        laty_2.addWidget(self.audio_address)
        
        
      

        laty_3=QHBoxLayout()
        laty_3.addWidget(save_address)
        laty_3.addWidget(self.save_address)
  


        laty_4=QHBoxLayout()
        laty_4.addWidget(save_name)
        laty_4.addWidget(self.save_name)

        laty_5=QHBoxLayout()
        laty_5.addWidget(comp_button)
        laty_5.addWidget(root_button)
  


        all_lay=QVBoxLayout()
        all_lay.addLayout(laty_1)
        all_lay.addLayout(laty_2)
        all_lay.addLayout(laty_3)
        all_lay.addLayout(laty_4)
        all_lay.addLayout(laty_5)


      
        self.setLayout(all_lay)
        
        self.resize(300,150)

        comp_button.clicked.connect(self.comp_video)
        root_button.clicked.connect(self.open_root)


      
    



        self.show()

    def setData(self):
        if (str(self.vedio_address.text())!=""):
            address=os.path.abspath(os.path.dirname(os.path.abspath(str(self.vedio_address.text()))))
            name=str(self.vedio_address.text()).split("/")[-1].split(".")[0]+".mp4"
            self.save_address.setText(address)
            self.save_name.setText(name)
        

    
    
    def comp_video(self):
        video_address=str(self.vedio_address.text())
        audio_address=str(self.audio_address.text())
        save_address=str(self.save_address.text())+"/"+str(self.save_name.text())

        cmd=ffmpeg+ " -i " + video_address + " -i "+ audio_address + " -c:v copy -c:a aac -strict experimental " + save_address
        print cmd
        self.hide()
        subprocess.Popen(cmd, shell=True)
        self.show()

        
        
        
        
       

    def open_root(self):
        if str(self.save_address.text())!="":
            path= str(self.save_address.text()).decode("utf-8")
            if os.path.isdir(path):
                os.startfile(path)


        

#*******************************************************************
#*******************************************************************
#***************************主函数***********************************
#*******************************************************************
#******************************************************************* 

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    obj= CompFile_()
    obj.show()
    sys.exit(app.exec_())
