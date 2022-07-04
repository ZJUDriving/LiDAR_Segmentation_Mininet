#!/usr/bin/env python3
# This file is covered by the LICENSE file in the root of this project.

import argparse
import subprocess
import datetime
import yaml
from shutil import copyfile
import os
import shutil
import __init__ as booger

from tasks.semantic.modules.user import *

import os
import pyinotify

class OnWriteHandler(pyinotify.ProcessEvent):

  def process_IN_CREATE(self, event): #函数名以"process_"开头,后面跟注册的监测类型
      # os.system('echo '+'create file:%s'%(os.path.join(event.path,event.name))) #之后用于nohup输出
      print("create file: %s " % os.path.join(event.path,event.name)) #打印
      user = User(ARCH, DATA, FLAGS.dataset, FLAGS.log, FLAGS.model)
      user.infer()

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

if __name__ == '__main__':
  parser = argparse.ArgumentParser("./infer.py")
  parser.add_argument(
      '--dataset', '-d',
      type=str,
      required=True,
      help='Dataset to train with. No Default',
  )
  parser.add_argument(
      '--log', '-l',
      type=str,
      default=os.path.expanduser("~") + '/logs/' +
      datetime.datetime.now().strftime("%Y-%-m-%d-%H:%M") + '/',
      help='Directory to put the predictions. Default: ~/logs/date+time'
  )
  parser.add_argument(
      '--model', '-m',
      type=str,
      required=True,
      default=None,
      help='Directory to get the trained model.'
  )
  global FLAGS
  FLAGS, unparsed = parser.parse_known_args()

  # print summary of what we will do
  print("----------")
  print("INTERFACE:")
  print("dataset", FLAGS.dataset)
  print("log", FLAGS.log)
  print("model", FLAGS.model)
  print("----------\n")
  print("Commit hash (training version): ", str(
      subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()))
  print("----------\n")

  # open arch config file
  try:
    print("Opening arch config file from %s" % FLAGS.model)
    global ARCH
    ARCH = yaml.safe_load(open(FLAGS.model + "/arch_cfg.yaml", 'r'))
  except Exception as e:
    print(e)
    print("Error opening arch yaml file.")
    quit()

  # open data config file
  try:
    print("Opening data config file from %s" % FLAGS.model)
    global DATA
    DATA = yaml.safe_load(open(FLAGS.model + "/data_cfg.yaml", 'r'))
  except Exception as e:
    print(e)
    print("Error opening data yaml file.")
    quit()

  # create log folder
  try:
    if os.path.isdir(FLAGS.log):
      shutil.rmtree(FLAGS.log)
    os.makedirs(FLAGS.log)
    os.makedirs(os.path.join(FLAGS.log, "sequences"))
    # for seq in DATA["split"]["train"]:
    #   seq = '{0:02d}'.format(int(seq))
    #   print("train", seq)
    #   os.makedirs(os.path.join(FLAGS.log, "sequences", seq))
    #   os.makedirs(os.path.join(FLAGS.log, "sequences", seq, "predictions"))
    for seq in DATA["split"]["valid"]:
      seq = '{0:02d}'.format(int(seq))
      print("valid", seq)
      os.makedirs(os.path.join(FLAGS.log, "sequences", seq))
      os.makedirs(os.path.join(FLAGS.log, "sequences", seq, "predictions"))
    # for seq in DATA["split"]["test"]:
    #   seq = '{0:02d}'.format(int(seq))
    #   print("test", seq)
    #   os.makedirs(os.path.join(FLAGS.log, "sequences", seq))
    #   os.makedirs(os.path.join(FLAGS.log, "sequences", seq, "predictions"))
  except Exception as e:
    print(e)
    print("Error creating log directory. Check permissions!")
    raise

  except Exception as e:
    print(e)
    print("Error creating log directory. Check permissions!")
    quit()

  # does model folder exist?
  if os.path.isdir(FLAGS.model):
    print("model folder exists! Using model from %s" % (FLAGS.model))
  else:
    print("model folder doesnt exist! Can't infer...")
    quit()

  #n_gpu = 0
  #os.environ["CUDA_VISIBLE_DEVICES"] = str(n_gpu)

  # create user and infer dataset
  # global user
  # user = User(ARCH, DATA, FLAGS.dataset, FLAGS.log, FLAGS.model)
  # user.infer()
  auto_compile()
