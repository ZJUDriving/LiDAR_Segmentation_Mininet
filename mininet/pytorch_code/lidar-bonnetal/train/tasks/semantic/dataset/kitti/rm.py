import os 

velo_path = '/home/dhz/dataset/semantic_kitti/dataset/sequences/00/velodyne/'
label_path = '/home/dhz/dataset/semantic_kitti/dataset/sequences/00/labels/'

velos = []
labels = []

for velo, label in zip(os.listdir(velo_path),os.listdir(label_path)):
    # print(velo.split(".")[0])
    # print(label.split(".")[0])
    velos.append(velo)
    labels.append(label)

cnt = 0
for label in labels:
    if label.split(".")[0]+".bin" not in velos :
        print(label.split(".")[0]+".bin")
        os.remove(label_path+label)
        print(label_path+label+" removed.")
        cnt += 1

print(cnt)
