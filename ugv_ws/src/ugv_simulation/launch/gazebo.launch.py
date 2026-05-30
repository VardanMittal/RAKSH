import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():

    desc_pkg = get_package_share_directory('ugv_description')
    sim_pkg  = get_package_share_directory('ugv_simulation')

    urdf_file  = os.path.join(desc_pkg, 'urdf', 'ugv.urdf.xacro')
    world_file = os.path.join(sim_pkg,  'worlds', 'farm.sdf')

    robot_description = Command(['xacro ', urdf_file])

    return LaunchDescription([

        # Start Gazebo with our farm world
        ExecuteProcess(
            cmd=['/opt/ros/jazzy/opt/gz_tools_vendor/bin/gz',
                 'sim', '-r', world_file],
            output='screen'
        ),

        # Publish robot TF tree
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': True
            }]
        ),

        # Wait 3s for Gazebo to load then spawn robot
        TimerAction(
            period=3.0,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-world', 'farm',
                        '-name', 'ugv',
                        '-topic', 'robot_description',
                        '-x', '0.0',
                        '-y', '0.0',
                        '-z', '0.15'
                    ],
                    output='screen'
                )
            ]
        ),

        # Bridge Gazebo topics to ROS2
        TimerAction(
            period=4.0,
            actions=[
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    name='gz_bridge',
                    output='screen',
                    arguments=[
                        '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                        '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                        '/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
                        '/camera/left/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                        '/camera/right/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                        '/camera/left/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
                        '/camera/right/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
                        '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                        '/tf@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                        '/tf_static@tf2_msgs/msg/TFMessage@gz.msgs.Pose_V',
                    ]
                )
            ]
        ),

    ])