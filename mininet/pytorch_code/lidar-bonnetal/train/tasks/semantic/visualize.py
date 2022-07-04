#!/usr/bin/env python3
# This file is covered by the LICENSE file in the root of this project.

import argparse
from enum import auto
import os
import yaml
import __init__ as booger
import _thread
import sys

from common.laserscan import LaserScan, SemLaserScan
from common.laserscanvis import LaserScanVis
# import Pathlib
# from icecream import ic as print
import pyinotify

class OnWriteHandler(pyinotify.ProcessEvent):

  def process_IN_CREATE(self, event): #函数名以"process_"开头,后面跟注册的监测类型
    os.system('echo '+'create file:%s'%(os.path.join(event.path,event.name))) #之后用于nohup输出
    # vis.append_label_names(os.path.join(event.path,event.name))
    # scan_name = event.name.split('.label')[0] + '.bin'
    # vis.append_scan_names(scan_path+scan_name)

    label_path = '/home/mars-nuc/gy_pc_seg/pcl/predictions/sequences/00/predictions/'
    scan_path = '/home/mars-nuc/gy_pc_seg/pcl/dataset/sequences/00/velodyne/'

    label_names = []
    scan_names = []
    for fi in os.listdir(label_path):
      label_names.append(os.path.join(label_path,fi))
      scan_name_part = fi.split('.label')[0]+'.bin'
      # if(Pathlib.Path(os.path.join(scan_path,scan_name_part).exists())):
      scan_names.append(os.path.join(scan_path,scan_name_part))

    label_names.sort()
    scan_names.sort()
    vis.append_label_names(label_names)
    vis.append_scan_names(scan_names)

    # vis.update_scan_and_display() //modified by dhz, 2022.7.4, for remote display
    vis.update_scan_and_broadcast()


def auto_compile(path='/home/mars-nuc/gy_pc_seg/pcl/predictions/sequences/00/predictions'):
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
            # notifier.stop()
            os._exit(0)
            break



if __name__ == '__main__':
  parser = argparse.ArgumentParser("./visualize.py")
  parser.add_argument(
      '--dataset', '-d',
      type=str,
      required=True,
      help='Dataset to visualize. No Default',
  )
  parser.add_argument(
      '--config', '-c',
      type=str,
      required=False,
      default="config/labels/semantic-kitti.yaml",
      help='Dataset config file. Defaults to %(default)s',
  )
  parser.add_argument(
      '--sequence', '-s',
      type=str,
      default="00",
      required=False,
      help='Sequence to visualize. Defaults to %(default)s',
  )
  parser.add_argument(
      '--predictions', '-p',
      type=str,
      default=None,
      required=False,
      help='Alternate location for labels, to use predictions folder. '
      'Must point to directory containing the predictions in the proper format '
      ' (see readme)'
      'Defaults to %(default)s',
  )
  parser.add_argument(
      '--ignore_semantics', '-i',
      dest='ignore_semantics',
      default=False,
      action='store_true',
      help='Ignore semantics. Visualizes uncolored pointclouds.'
      'Defaults to %(default)s',
  )
  parser.add_argument(
      '--offset',
      type=int,
      default=0,
      required=False,
      help='Sequence to start. Defaults to %(default)s',
  )
  parser.add_argument(
      '--ignore_safety',
      dest='ignore_safety',
      default=False,
      action='store_true',
      help='Normally you want the number of labels and ptcls to be the same,'
      ', but if you are not done inferring this is not the case, so this disables'
      ' that safety.'
      'Defaults to %(default)s',
  )
  FLAGS, unparsed = parser.parse_known_args()

  # print summary of what we will do
  print("*" * 80)
  print("INTERFACE:")
  print("Dataset", FLAGS.dataset)
  print("Config", FLAGS.config)
  print("Sequence", FLAGS.sequence)
  print("Predictions", FLAGS.predictions)
  print("ignore_semantics", FLAGS.ignore_semantics)
  print("ignore_safety", FLAGS.ignore_safety)
  print("offset", FLAGS.offset)
  print("*" * 80)

  # open config file
  try:
    print("Opening config file %s" % FLAGS.config)
    CFG = yaml.safe_load(open(FLAGS.config, 'r'))
  except Exception as e:
    print(e)
    print("Error opening yaml file.")
    quit()

  # fix sequence name
  FLAGS.sequence = '{0:02d}'.format(int(FLAGS.sequence))

  # does sequence folder exist?
  scan_paths = os.path.join(FLAGS.dataset, "sequences",
                            FLAGS.sequence, "velodyne")
  if os.path.isdir(scan_paths):
    print("Sequence folder exists! Using sequence from %s" % scan_paths)
  else:
    print("Sequence folder doesn't exist! Exiting...")
    quit()

  # populate the pointclouds
  scan_names = [os.path.join(dp, f) for dp, dn, fn in os.walk(
      os.path.expanduser(scan_paths)) for f in fn]
  scan_names.sort()

  # does sequence folder exist?
  if not FLAGS.ignore_semantics:
    if FLAGS.predictions is not None:
      label_paths = os.path.join(FLAGS.predictions, "sequences",
                                 FLAGS.sequence, "predictions")
    else:
      label_paths = os.path.join(FLAGS.dataset, "sequences",
                                 FLAGS.sequence, "labels")
    if os.path.isdir(label_paths):
      print("Labels folder exists! Using labels from %s" % label_paths)
    else:
      print("Labels folder doesn't exist! Exiting...")
      quit()
    # populate the pointclouds
    label_names = [os.path.join(dp, f) for dp, dn, fn in os.walk(
        os.path.expanduser(label_paths)) for f in fn]
    label_names.sort()
    print(label_names)

    # check that there are same amount of labels and scans
    if not FLAGS.ignore_safety:
      pass
      # print(scan_names)
      # print(label_names)
      # assert(len(label_names) == len(scan_names)) #modified by dhz

  # create a scan
  if FLAGS.ignore_semantics:
    scan = LaserScan(project=True)  # project all opened scans to spheric proj
  else:
    color_dict = CFG["color_map"]
    scan = SemLaserScan(color_dict, project=True)

  # create a visualizer
  semantics = not FLAGS.ignore_semantics
  if not semantics:
    label_names = None
  vis = LaserScanVis(scan=scan,
                     scan_names=scan_names,
                     label_names=label_names,
                     offset=FLAGS.offset,
                     semantics=semantics,
                     instances=False)

  # print instructions
  print("To navigate:")
  print("\tb: back (previous scan)")
  print("\tn: next (next scan)")
  print("\tq: quit (exit program)")

  # vispy visualization version

  # _thread.start_new_thread(auto_compile,())
  # # auto_compile()

  # # run the visualizer
  # vis.run() #modified by dhz, 2022.7.4, for remote display

  try:
    auto_compile()
  except KeyboardInterrupt:
    os._exit(0)

  
