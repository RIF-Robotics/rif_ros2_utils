#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class BoolPublisher(Node):
    def __init__(self):
        super().__init__('bool_publisher')
        self.publisher_ = self.create_publisher(Bool, 'bool_test', 10)

        self.total_count = 60

        # Timer triggers every 0.1 seconds (10Hz)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.publish_count = 0

    def timer_callback(self):
        if self.publish_count >= self.total_count:
            self.get_logger().info('Finished publishing. Shutting down.')
            self.timer.cancel()
            raise SystemExit

        msg = Bool()
        msg.data = self.publish_count < int(self.total_count / 2.)

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}" ({self.publish_count + 1}/{self.total_count})')

        self.publish_count += 1

def main(args=None):
    rclpy.init(args=args)
    node = BoolPublisher()

    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()
