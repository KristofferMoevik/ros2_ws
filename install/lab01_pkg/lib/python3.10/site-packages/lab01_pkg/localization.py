import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from geometry_msgs.msg import Pose 

class Localization(Node):
    # Create a node called /localization, which subscribes to the /cmd_topic and
    # estimates the robot's position starting from the axis's origin, considering the topic's period of
    # 1 s and the velocity of 1 m/s. Publish the obtained pose on a topic called /pose of type 
    # 7
    # geometry_msg/msg/pose. Each time you publish a new message, print it on the shell with
    # the logger as in Task 2.

    def __init__(self):
        super().__init__('localization')
        self.pose = Pose()
        self.pose.position.x = float(0)
        self.pose.position.y = float(0)
        self.vel_subscriber_ = self.create_subscription(Twist, 'cmd_topic', self.vel_subscriber_callback, 10)
        self.loc_publisher_ = self.create_publisher(Pose, 'pose', 10)

    def vel_subscriber_callback(self, msg):
        self.pose.position.x = float(self.pose.position.x) + float(msg.linear.x)
        self.pose.position.y = float(self.pose.position.y) + float(msg.linear.y)

        self.loc_publisher_.publish(self.pose)
        self.get_logger().info('Publishing: "%s"' % self.pose)


def main(args=None):
    rclpy.init(args=args)

    localization = Localization()

    rclpy.spin(localization)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    localization.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
