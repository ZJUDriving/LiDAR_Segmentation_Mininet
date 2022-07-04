#! /usr/bin/env python

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import rospy
import time
import numpy as np
import math

def callback_pointcloud(data):
    assert isinstance(data, PointCloud2)
    gen = point_cloud2.read_points(data, field_names=("x", "y", "z", "intensity"), skip_nans=True)
    gen = np.asarray(list(gen), dtype = np.float32)
    for i in range(len(gen)):
        gen[i, 3] /= 100.0
        if gen[i, 3] > 1.:
            gen[i, 3] = 1.
    print(gen.shape)
    # print(str(rospy.get_rostime()))
    gen.tofile('/home/mars-nuc/gy_pc_seg/pcl/dataset/sequences/00/velodyne/' + str(math.floor(time.time()*100)) + '.bin')
    time.sleep(1)
    # for p in gen:
    #   print( "x: %.3f  y: %.3f  z: %.3f intensity: %.3f" %(p[0],p[1],p[2],p[3]))

def main():
    rospy.init_node('pcl_listener', anonymous=True)
    rospy.Subscriber('/lidar_center/velodyne_points', PointCloud2, callback_pointcloud)
    rospy.spin()

if __name__ == "__main__":
    main()
