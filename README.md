## 1. Install Robomaker 
contribution from Mr. Nigel Gardiner from AWS
```
curl -fsSL "http://bit.ly/robomaker" | sudo -E bash -
```
After about 10 minutes with ROS installed, you must reboot the system
```
sudo reboot
```

## 2. Setup aws_mouse 
### (only run once) ->aws management console -> cloud 9 
```
git clone -b saveimage  https://github.com/lbaitemple/aws_mouse/ 
cd aws_mouse
bash ./updateos.sh
```
Only when you see any lock error, please try
```
sudo rm -r /var/lib/dpkg/lock*
sudo dpkg --configure -a
bash ./updateos.sh
```

### compile ROS (only run once)
```
rosdep install --from-paths src --ignore-src -r -y
```

## 3. Run and program aws_mouse (when step 1 and step 2 are completed)
### 3a. run the following commands only when you changed the source code
```
colcon build
source install/setup.bash
```

### 3b.open virtual desktop 
```
cd ~/environment/aws_mouse
export DISPLAY=:0
source install/setup.bash
roslaunch maze_demo explore_world.launch
```
### 3c.open one more terminal to control the robot move forward for 1.2 meters
```
cd ~/environment/aws_mouse
source install/setup.bash
rosrun maze_demo runner_template.py oforward 1.2
```
### 3c.open one more terminal to control the robot rotate left for 90 degrees (right rotation is negative degrees)

```
cd ~/environment/aws_mouse
source install/setup.bash
rosrun maze_demo runner_template.py turn 90
```

### 4. see what camera sees
###### open another terminal
```
source install/setup.bash
export DISPLAY=:0
rqt_image_view 
```


##
##
## You can stop here .... 
##
##


## The following is for more advanced AI usages.
###### if load an empty world with flowers, you can use
```
roslaunch maze_demo explore_world.launch worldfile:=empty_flower.world x:=0 y:=0
```

### running the robot. [node_follow_wall2.py has the cmd_vel topic to move the robot]
#####  open another terminal 

```
cd ~/environment/aws_mouse
source install/setup.bash
rosrun maze_demo test_runner.py forward 0.1
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
cd ~/environment/aws_mouse
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
cd ~/environment/aws_mouse
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
cd ~/environment/aws_mouse
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
cd 
cd ~/environment/aws_mouse
source install/setup.bash
roslaunch img_recognition train_rosmodel.launch

```

### running deep learning inferencing
#### open another terminal 
##### to run the classifier using deep learning neural network
```
cd ~/environment/aws_mouse
source install/setup.bash
roslaunch img_recognition infer.launch 
```

#### open another terminal 
##### to run the following command to get prediction/inference
```
cd ~/environment/aws_mouse
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
