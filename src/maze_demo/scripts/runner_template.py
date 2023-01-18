#!/usr/bin/env python

# Importing packages will allow us to use specific functions to simplify our code
# sys: Allows us to interact more closely with the interpreter
import sys, time
# rospy: Allows for interaction with ROS nodes and topics 
import rospy
# Micromouse_Node: A Node to manage Micromouse behavior. More can be found on this in the maze_demo/src/mouse_common/utils.py file
from mouse_common.utils import Micromouse_Node
from pyamaze.pyamaze import maze
from pyamaze.aStarDemo import aStar
from geometry_msgs.msg import Twist

# Minimum Safety Range to Wall
wall_distance = 0.2

# Allowable Distance to Stop Moving Forward
wall_distance_forward = 0.15

# Allowable Distance to Stop Moving in Other Directions
wall_distance_side = 0.1

class MazeRunner(object):
    
    # A Python Class creates an object that we can provide with methods. These methods will allow our object to perform some tasks. 
    # MazeRunner is the name of our class, and we can instantiate a MazeRunner Object with the properties defined in the __init__
    
    def __init__(self, action, dist):

        # Every Python class must have an __init__(self) method to provide every object of that type with a set of properties

        # Start Mouse Node 
        rospy.init_node("mouse_node", anonymous=False)

        # Instantiate a new copy of the Micromouse_Node object 
        micromouse_node = Micromouse_Node()
        
        self.action = action
        self.argument = float(dist)
        self.maze = maze(16,16)

        # Rune Maze with out new object 
        self.runMaze(micromouse_node)
        
        # Shut down node when finished
        rospy.on_shutdown(micromouse_node.on_shutdown)   

        # Require ctrl+c to cancel process
        rospy.spin()    

    def moveOneCell(self, mn, distance=0.3, kp=80, DEBUG = False,):
    	rate = rospy.Rate(30)

    	mn._mved_distance.data = 0.0
    	mn.get_init_position()
    	
    	if distance < 0.0:
    	    mv_forward = False
    	else:
    	    mv_forward = True

    	while not rospy.is_shutdown():
            if mn.laser_sensors is not None:
    	        vel_msgl, leftd = mn.follow_left_wall(mv_forward, desired_dist = 0.13, kp = kp)
            	vel_msgr, rightd = mn.follow_right_wall(mv_forward, desired_dist = 0.13, kp = kp)
            	vel_msgc, centerd = mn.follow_both_wall(mv_forward, kp = kp)
            	
            	follow=''
            	if ((mn.laser_sensors['left']>0.3 and mn.laser_sensors['right']>0.3) or (mn.laser_sensors['frontleft']>0.3 and mn.laser_sensors['frontright']>0.3)): # no wall on both side
                    vel_msg = vel_msgl
                    vel_msg.angular.z =0 # no rotation
                    follow = 'no wall'
#                    print("no wall")
            	else:		    # if left side wall is closer, follow left
    	            if (rightd > leftd) and (mn.laser_sensors['frontleft']>0.07):  # follow left
                            vel_msg = vel_msgl
                            follow = 'left wall'
    	            elif (rightd > leftd) and (mn.laser_sensors['frontleft']<0.07):  # too close to the wall so follow center
                            vel_msg = vel_msgc
                            follow = 'center wall'
    	            elif (rightd < leftd) and (mn.laser_sensors['frontright']>0.07):  # follow right
                        vel_msg = vel_msgr
                        follow = 'right wall'
    	            else:
                        vel_msg = vel_msgc
                        follow = 'center wall'

            	mn.pub_msg.publish(vel_msg)
            	mn.print_walldistance(False, follow)
            	if (mn.laser_sensors['front']<wall_distance_forward):
            	    break
            	if (mn._mved_distance.data >abs(distance)):
            	    break
            	rate.sleep()
    	        vel_msg = Twist()
    	        vel_msg.linear.x = 0
    	        mn.pub_msg.publish(vel_msg)
    	        if (DEBUG):
    	            print("distance travelled {:.3f}".format(mn._mved_distance.data))
    	
    	vel_msg = Twist()
    	vel_msg.linear.x = 0
    	vel_msg.angular.z = 0
    	mn.pub_msg.publish(vel_msg)
   	
    	return mn._mved_distance.data
    	
    def shutdown(self):
        print("node is killed")

    def runMaze(self, mn):
        # Inputs: 
            # self: MazeRunner Object
            # mn: Mouse Node from MazeRunner Object
        # Function:
            # While rospy is running this method will check the left and front laser scan topics
            # and decide to move forward one cell or rotate 

        # Log Info 
        rospy.loginfo('**starting....')
        rate = rospy.Rate(1)

        # Start Counting
        step = 0

        # While ROS is running
        while not rospy.is_shutdown():
            # if all three side are great thant the threshold, should go forward
 #           if (mn.laser_sensors['left']>wall_distance_side):

                # Set Distance Moved With Each Forward Step  
            fdist=-0.3
            mn.log_info()
            if (self.action == 'forward'):
                mn.move_onecell(distance=self.argument, kp=80, DEBUG=True)
            if (self.action == 'oforward'):
                self.moveOneCell(mn, distance=self.argument, kp=80, DEBUG=True)
            if (self.action == 'turn'):
                mn.turnangle(self.argument, DEBUG=True)
            print("done action")
            rate.sleep()
            #rospy.on_shutdown(self.shutdown)
#            rospy.signal_shutdown('Quit')
#            mn.move_onecell(distance=fdist, DEBUG=True)
#            mn.move_onecell(distance=fdist, DEBUG=True)
#            mn.turnangle(90, DEBUG=True)
#            mn.move_onecell(distance=7*fdist, DEBUG=True)
#            mn.turnangle(90, DEBUG=True)
#            mn.move_onecell(distance=fdist, DEBUG=True)
#            mn.move_onecell(distance=fdist, DEBUG=True)
#            mn.move_onecell(distance=fdist, DEBUG=True)
            break   

                # This case statement will select what to do given sensor data 
#                if  (mn.laser_sensors['front']>fdist):
#                    # When there is room asdin front
                    # Use the move_oncecell function of our mn object
#                    dist=mn.move_onecell(fdist)
#                    # Add a count 
#                    step = step + 1
                    # Log this info to screen
#                    print("distance travelled in this cell is {:.4f}-{}".format(dist, step))
 #                   print("classfication is {} ".format(mn.getPredication()))

                # What can we do when the laser detects a wall in front of us?
 #               else:
 #                   dist = mn.laser_sensors['front'] 
 #                   mn.move_onecell(dist)	

# Run the MazeRunner
import sys

if __name__ == "__main__" :
    mr = MazeRunner(sys.argv[1], sys.argv[2])
    
    
    
