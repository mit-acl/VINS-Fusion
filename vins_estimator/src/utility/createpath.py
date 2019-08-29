#!usr/bin/env python

import rospy
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import tf_conversions
import tf2_ros
import geometry_msgs.msg


path = Path()

def callback(data): 
    global path
    pose = PoseStamped()
    pose.header = data.header
    pose.pose = data.pose
    path.header = pose.header
    path.poses.append(pose)
    pub.publish(path)

def handle_world_transform(msg):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "world"
    t.child_frame_id = "vinsworld"
    t.transform.translation.x = msg.x
    t.transform.translation.y = msg.y
    t.transform.translation.z = 0.0
    q = tf_conversions.transformations.quaternion_from_euler(0, 0, msg.theta)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    br.sendTransform(t)


if __name__ == '__main__':
    rospy.init_node('vicon_path_node', anonymous=True)
    rospy.init_node('world_broadcaster')
    pub = rospy.Publisher("/JA01/vicon/path", Path, queue_size=1)
    vicon_msg = PoseStamped()
    vicon_msg = rospy.Subscriber("/JA01/world", PoseStamped, callback)
    
    rospy.spin()
    try:
        while not rospy.is_shutdown():  
            pass
    except rospy.ROSInterruptException:
        pass

        
    
