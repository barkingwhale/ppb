#! /usr/bin/python3
#
# ppb.py - photo booth project

from picamera import PiCamera
from time import sleep
from datetime import datetime
from gpiozero import Button
from subprocess import Popen,PIPE
import glob
import ptvsd
import sys

#local modules
import debugger


#FIXME. create if it doesn't exist
photoPath = '/home/pi/share/ppb/'


#TODO - currently the preview needs to be full width OR full height.
# cannot have partial window.  find out why

#full screen for current monitor = (1440,900)
# but need to set the camera resolution for the 
#cameraResolution = (1920,1080)
#cameraResolution = (3280,2464)
cameraResolution = (1640,1232)

#3280 is highest resolution of camera for images
#1640 is highest resolution that also allows recording vids




def main(argv):    
    try:
        #debugger.attachDebugger()
        
        camera = PiCamera()
        button = Button(17)

        camera.rotation = 180
        camera.resolution = cameraResolution
        camera.framerate = 30

        # warm up camera - let autosettings adjust
        # TODO - see if this is necessary.  manual adjustments??
        sleep(2)

        camera.start_preview(fullscreen=False,window=(100,20,640,480))
        
        
        baseTime = str(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
        # this does have a parameter resize=(1920,1080), but we don't
        # want that.  the camera resolution was set to 4:3 above for the images
        # and resizing will just stretch the scene
        camera.start_recording(photoPath + '%s__vid.h264' %(baseTime))
        
        #while True:
        if True:

            camera.annotate_text = "Press Button!!"
            camera.annotate_text_size = 50
            print (camera.resolution)
        
            #button.wait_for_press()
            sleep(5)


            #startCaptureSeq()
            
            #createMontage(photoPath + baseTime)
            
    finally:
        #print ("finally")
        camera.stop_preview()

        # always attempt to stop the video recording, and handle/ignore
        # the exception if it wasn't recording
        try:
            camera.stop_recording()
        except:
            #print("camera stop recording exception")
            pass
            
        


def createMontage(baseName):
    path = baseName + '*.jpg'
    files = glob.glob(baseName + '__image*.jpg')
    files.sort()
    cmd = 'montage '
    cmd += ' '.join(files)
    cmd += ' -geometry 480x270+10+10 -shadow '
    cmd += baseName + '_montage.jpg'
    #FIXME add to log
    print(cmd)
    # fire and forget.. just let the process happen as the os see's fit
    proc = Popen(cmd,shell=True,stdout=PIPE,stderr=PIPE)


def StartCaptureSeq():
    """
    baseTime = str(datetime.now().strftime('%Y-%m-%d_%H%M%S'))
        
    for i in range(4):
        camera.annotate_text = "Taking picture " + str(i+1)
        sleep(3)
        camera.annotate_text = ""
        fileName = '%s%s__image%d.jpg' %(photoPath,baseTime,i+1)
        camera.capture(fileName)
        print("taking picture " + fileName)    
    """


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("main KeyboardInterrupt")
        pass    

