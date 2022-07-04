import os
import pyinotify

class OnWriteHandler(pyinotify.ProcessEvent):

    def process_IN_CREATE(self, event): #函数名以"process_"开头,后面跟注册的监测类型
        # os.system('echo '+'create file:%s'%(os.path.join(event.path,event.name))) #之后用于nohup输出
        print("create file: %s " % os.path.join(event.path,event.name)) #打印
        os.chdir('/home/mars-nuc/dhz/mininet/pytorch_code/lidar-bonnetal/train/tasks/semantic')
        # os.system('pwd')
        os.system('./infer.py -d /home/mars-nuc/gy_pc_seg/pcl/dataset -l /home/mars-nuc/gy_pc_seg/pcl/predictions -m /home/mars-nuc/dhz/mininet/pytorch_code/lidar-bonnetal/train/tasks/semantic/models/3D-MiniNet')
        # os.system('./visualize.py -d /home/mars-nuc/gy_pc_seg/pcl/dataset -p /home/mars-nuc/gy_pc_seg/pcl/predictions -s 00')

def auto_compile(path='/home/mars-nuc/gy_pc_seg/pcl/dataset/sequences/00/velodyne'):
    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE #监测类型，如果多种用|分开，pyinotify.IN_CREATE | pyinotify.IN_DELETE
    notifier = pyinotify.Notifier(wm, OnWriteHandler())
    wm.add_watch(path, mask,rec=True,auto_add=True)
    print('==> Start monitoring %s (type c^c to exit)' % path)
    while True:
        try:
            notifier.process_events()
            if notifier.check_events():
                notifier.read_events()
        except KeyboardInterrupt:
            notifier.stop()
            break

if __name__ == "__main__":
    auto_compile()