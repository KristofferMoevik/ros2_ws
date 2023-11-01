import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist 

class Controller(Node):
    # publishes velocities on a topic called
    # /cmd_topic of type ‘geometry_msgs/msg/Twist at a frequency of 1 Hz. The robot
    # always moves at 1 m/s, and its movement follows this rule:
    # 1. N seconds along the X-axis
    # 2. N seconds along the Y-axis
    # 3. N seconds opposite the X-axis
    # 4. N seconds opposite the Y-axis
    # N starts from 1 and increases by 1 after each set of movements

    def __init__(self):
        super().__init__('controller')
        self.vel_publisher_ = self.create_publisher(Twist, 'cmd_topic', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.step = 1
        self.N = 1
        self.count_N = 0

    def timer_callback(self):
        
        if self.count_N >= self.N:
            self.count_N = 0
            if self.step < 4:
                self.step += 1
            else:
                self.step = 1
                self.N += 1
                
        msg = Twist()
        if self.step == 1:
            msg.linear.x = float(1)
        elif self.step == 2:
            msg.linear.y = float(1)
        elif self.step == 3:
            msg.linear.x = float(-1)
        elif self.step == 4:
            msg.linear.y = float(-1)
        self.count_N += 1

        self.vel_publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.linear)




def main(args=None):
    rclpy.init(args=args)

    controller = Controller()

    rclpy.spin(controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
