## Install Robomaker 
contribution from Mr. Nigel Gardiner from AWS
```
curl -fsSL "http://bit.ly/robomaker" | sudo -E bash -
```

#### 
#### create 20.04
```
sudo apt install python2 nodejs awscli -y
```
run the above code in ec2 before cloud9 is launched.
```
wget https://raw.githubusercontent.com/lbaitemple/aws_mouse/saveimage/ubuntu-2004-ros2-foxy-dcv.sh
```

# aws_mouse (only run once)
```
git clone -b saveimage  https://github.com/lbaitemple/aws_mouse/ 
cd aws_mouse
bash ./updateos.sh
```
If you see any lock error, please try
```
sudo rm -r /var/lib/dpkg/lock*
sudo dpkg --configure -a
bash ./updateos.sh
```

### compile ROS (only run once)
```
rosdep install --from-paths src --ignore-src -r -y
pip2 install -U PyYAML

```

### open virtual desktop 
```
colcon build
source install/setup.bash
export DISPLAY=:0
roslaunch maze_demo explore_world.launch
```

##### see what camera sees
###### open another terminal
```
source install/setup.bash
export DISPLAY=:0
rqt_image_view 
```


###### if load an empty world with flowers, you can use
```
roslaunch maze_demo explore_world.launch worldfile:=empty_flower.world x:=0 y:=0
```




### running the robot. [node_follow_wall2.py has the cmd_vel topic to move the robot]
#####  open another terminal 

```
source install/setup.bash
rosrun maze_demo test_runner.py oforward 0.1
rosrun maze_demo test_runner.py turn 90
```
### or choose a different position or pose
```
roslaunch maze_demo explore_world.launch x:=-0.75 y:=-2.25 Y:=0.00
```

### create a folder with label (ex. label = sunflower, daisy and background)
make sure you create a background folder first
```
rosrun img_recognition mkdir.py -n background
```
Then, you can create other folders based on target image labels
```
rosrun img_recognition mkdir.py -n rose
rosrun img_recognition mkdir.py -n sunflower
rosrun img_recognition mkdir.py -n daisy
```
### remove a folder
```
rosrun img_recognition rmdir.py --name rose
```

#### open one more terminal to save images for training
```
source install/setup.bash
roslaunch img_recognition save_rosimage.launch
```

#### open one more terminal to make the default label
```
rosservice call /save_image/select_label background
```
#### or make the  label for rose
```
rosservice call /save_image/select_label rose
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

#### make another target label sunflower
```
rosservice call /save_image/select_label sunflower
```
#### make another target label rose
```
rosservice call /save_image/select_label rose
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
### Backup configuration
```
bash ./saveconfig.sh backup
```

### Restore configuration
```
bash ./saveconfig.sh restore
```

### get a deep learning trained model
```
source install/setup.bash
roslaunch img_recognition train_rosmodel.launch

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



##### if you want to show laser scan (help to see if the robot hits the wall)
```
roslaunch maze_demo explore_world.launch laser_visualize:=true 
```
##### if you want to show camera scan (may be combined with laser visualization)
```
roslaunch maze_demo explore_world.launch camera_visualize:=true
```
