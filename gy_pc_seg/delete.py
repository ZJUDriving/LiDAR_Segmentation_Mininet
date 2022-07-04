import os

from numpy import double
import rospy
import time
import pathlib

path = "/home/mars-nuc/gy_pc_seg/pcl/dataset/sequences/00/velodyne/"
pred_path = "/home/mars-nuc/gy_pc_seg/pcl/predictions/sequences/00/predictions/"
threshold = 10

def main():
    while True:
        pass
        try:
            # ti = rospy.get_rostime()
            ti = time.time()
            files = os.listdir(path)
            kpt_num = 15
            
            files = sorted(files,  key=lambda x: os.path.getmtime(os.path.join(path, x)))
       
            for i in range(len(files)):
                if i < len(files) - kpt_num:
                    fi = files[i]
                    os.chdir(path)
                    os.remove(fi)
                    if(pathlib.Path(pred_path+fi.split('.bin')[0]+'.label').exists()):
                        os.remove(pred_path+fi.split('.bin')[0]+'.label')
                        print(fi.split('.bin')[0]+'.label'+ ' removed!')
                    # os.chdir(pred_path)
                    # os.remove(fi.split('.bin')[0]+'.label')
                    print(fi+' removed!')
            # for fi in files:
            #     if double(fi.split('.bin')[0])/100 < ti - threshold:
            #         os.chdir(path)
            #         os.remove(fi)
            #         if(pathlib.Path(pred_path+fi.split('.bin')[0]+'.label').exists()):
            #             # os.chdir(pred_path)
            #             os.remove(pred_path+fi.split('.bin')[0]+'.label')
            #             print(fi.split('.bin')[0]+'.label'+ ' removed!')
            #         # os.chdir(pred_path)
            #         # os.remove(fi.split('.bin')[0]+'.label')
            #         print(fi+' removed!')
            
            # time.sleep(10)
        except KeyboardInterrupt:
            print("Exit!")
            break



if __name__ == "__main__":
    # rospy.init_node('delete', anonymous=True)

    main()
