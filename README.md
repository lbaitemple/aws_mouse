# aws_mouse
```
git clone -b saveimage  https://github.com/lbaitemple/aws_mouse/ 
cd aws_mouse
chmod +x updateos.sh
./updateos.sh
```
If you see any lock error, please try
```
sudo rm -r /var/lib/dpkg/lock*
sudo dpkg --configure -a
./updateos.sh
```

### compile ROS
```
rosdep install --from-paths src --ignore-src -r -y
colcon build
source install/setup.bash
```

### open virtual desktop
```
export DISPLAY=:0
roslaunch maze_demo explore_world.launch
```
###### if load an empty world with rose, you can use
```
roslaunch maze_demo explore_world.launch worldfile:=empty_rose.world
```


##### see what camera sees
###### open another terminal
```
source install/setup.bash
export DISPLAY=:0
rqt_image_view 
```
##### if you want to show laser scan (help to see if the robot hits the wall)
```
roslaunch maze_demo explore_world.launch laser_visualize:=true 
```
##### if you want to show camera scan (may be combined with laser visualization)
```
roslaunch maze_demo explore_world.launch camera_visualize:=true
```

### running the robot. [node_follow_wall2.py has the cmd_vel topic to move the robot]
#####  open another terminal 

```
source install/setup.bash
rosrun maze_demo maze_runner.py
```
### or choose a different position or pose
```
roslaunch maze_demo explore_world.launch x:=-0.75 y:=-2.25 Y:=0.00
```
### running deep learning inferencing
#### open another terminal 
##### to run the classifier using deep learning neural network
```
source install/setup.bash
roslaunch img_recognition infer.launch 
```

#### open another terminal 
##### to run the following command to get prediction/inference
```
source install/setup.bash
rostopic echo -n1 /prediction
rostopic echo -n1 /inference 
```

#### open one more terminal to save images for training
```
source install/setup.bash
roslaunch img_recognition save_rosimage.launch
```

#### add image to an labelled folder
```
source install/setup.bash
rosservice call /save_image/save_image_action  true
```
#### You can stop the collection
```
rosservice call /save_image/save_image_action  false
```
