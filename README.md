# LiDAR_Segmentation_Mininet

Segmentation of LiDAR Pointcloud for gy



For the limitation of computation resources, we use 3dmininet for pointcloud segmentation



Certain topic is subscibed, see `sub_pc.py`

```bash
cd gy_pc_seg/scripts
./clear.sh
./run_infer.sh
```

In parallel, run:

```bash
./run_subscribe.sh
./run_vis.sh
./run_delete.sh
```



The segmentation results are published in ros topic `point_cloud2`, and you can visualize them in rviz.
