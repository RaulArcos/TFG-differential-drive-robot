import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Twist
from std_msgs.msg import Header

def publish_odom_data():
    rospy.init_node('odom_publisher', anonymous=True)
    rate = rospy.Rate(1)  # Frecuencia de publicación en Hz

    odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)

    while not rospy.is_shutdown():
        # Crear un mensaje Odometry
        odom_msg = Odometry()
        odom_msg.header = Header()
        odom_msg.header.stamp = rospy.Time.now()
        odom_msg.header.frame_id = 'odom'

        # Configurar la posición y orientación ficticias
        odom_msg.pose.pose = Pose()
        odom_msg.pose.pose.position.x = 1.0
        odom_msg.pose.pose.position.y = 2.0
        odom_msg.pose.pose.position.z = 0.0
        odom_msg.pose.pose.orientation.x = 0.0
        odom_msg.pose.pose.orientation.y = 0.0
        odom_msg.pose.pose.orientation.z = 0.0
        odom_msg.pose.pose.orientation.w = 1.0

        # Configurar la velocidad ficticia
        odom_msg.twist.twist = Twist()
        odom_msg.twist.twist.linear.x = 0.5
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.angular.z = 0.1

        # Publicar el mensaje Odometry
        odom_pub.publish(odom_msg)

        rate.sleep()

if __name__ == '__main__':
    try:
        publish_odom_data()
    except rospy.ROSInterruptException:
        pass