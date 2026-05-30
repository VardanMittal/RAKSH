import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='rtabmap_odom',
            executable='stereo_odometry',
            name='stereo_odometry',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'frame_id': 'base_footprint',
                'odom_frame_id': 'odom',
                'publish_tf': False,
                'Reg/Force3DoF': 'true',
                'Vis/MinInliers': '10',
                'Stereo/MinDisparity': '1',
                'Stereo/MaxDisparity': '64',
                'OdomF2M/MaxSize': '1000',
                'Vis/MaxFeatures': '500',
            }],
            remappings=[
                ('left/image_rect',  '/camera/left/image_raw'),
                ('right/image_rect', '/camera/right/image_raw'),
                ('left/camera_info', '/camera/left/camera_info'),
                ('right/camera_info','/camera/right/camera_info'),
                ('odom',             '/vo'),
            ]
        ),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'frame_id': 'base_footprint',
                'odom_frame_id': 'odom',
                'map_frame_id': 'map',
                'subscribe_stereo': True,
                'subscribe_depth': False,
                'subscribe_odom_info': True,
                'publish_tf': True,
                'Reg/Force3DoF': 'true',
                'RGBD/AngularUpdate': '0.05',
                'RGBD/LinearUpdate': '0.1',
                'Kp/MaxFeatures': '500',
                'Grid/FromDepth': 'false',
                'Grid/RangeMin': '0.2',
                'Grid/RangeMax': '5.0',
                'Mem/IncrementalMemory': 'true',
                'Stereo/MinDisparity': '1',
                'Stereo/MaxDisparity': '64',
                'Vis/MinInliers': '10',
            }],
            remappings=[
                ('left/image_rect',  '/camera/left/image_raw'),
                ('right/image_rect', '/camera/right/image_raw'),
                ('left/camera_info', '/camera/left/camera_info'),
                ('right/camera_info','/camera/right/camera_info'),
                ('odom',             '/odometry/filtered'),
                ('odom_info',        '/odom_info'),
            ]
        ),

    ])