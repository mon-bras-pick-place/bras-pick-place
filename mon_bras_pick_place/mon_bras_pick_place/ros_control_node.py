#!/usr/bin/env python3
"""
ROS 2 node to send a pick-and-place trajectory command.
"""
import rclpy # type: ignore
from rclpy.node import Node # type: ignore
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint # type: ignore
import time

class PickAndPlaceCommander(Node):
    def __init__(self):
        super().__init__('pick_and_place_commander')
        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        time.sleep(2)

    def send_joint_command(self, positions, duration_sec=3.0):
        """Sends a single joint configuration to the robot."""
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = duration_sec
        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent command: {positions}')
        time.sleep(duration_sec)

    def run_sequence(self):
        """Defines and executes the pick-and-place sequence."""
        self.send_joint_command([0.0, -0.5, 0.8, 0.0, 1.2, 0.0])
        self.send_joint_command([0.0, -0.8, 1.0, 0.0, 1.2, 0.0])
        self.get_logger().info('Gripper closed (simulated)')
        self.send_joint_command([0.0, -0.5, 0.8, 0.0, 1.2, 0.0])
        self.send_joint_command([1.0, -0.5, 0.8, 0.0, 1.2, 0.0])
        self.send_joint_command([1.0, -0.8, 1.0, 0.0, 1.2, 0.0])
        self.get_logger().info('Gripper opened (simulated)')
        self.send_joint_command([1.0, -0.5, 0.8, 0.0, 1.2, 0.0])

def main(args=None):
    rclpy.init(args=args)
    node = PickAndPlaceCommander()
    node.run_sequence()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()