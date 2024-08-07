import xacro
import launch
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare

def load_robot_description(context, *args, **kwargs):
    urdf_mappings = {
        'raspicam_mount'        : LaunchConfiguration('raspicam_mount').perform(context),
        'sonars_installed'      : LaunchConfiguration('sonars_installed').perform(context),
        'camera_extrinsics_file': LaunchConfiguration('camera_extrinsics_file').perform(context),
        'lidar_installed'       : LaunchConfiguration('lidar_installed').perform(context),
        'velodyne_installed'    : LaunchConfiguration('velodyne_installed').perform(context),
        'kinect_installed'      : LaunchConfiguration('kinect_installed').perform(context)
    }

    robot_desc = xacro.process_file(
        input_file_name=PathJoinSubstitution([FindPackageShare('magni_description'), 'urdf', 'magni.urdf.xacro']).perform(context),
        mappings=urdf_mappings
    ).toprettyxml(indent='  ')

    return [Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_desc}]
    )]

def generate_launch_description():

    launch_args = [
        DeclareLaunchArgument('raspicam_mount', default_value='forward'),
        DeclareLaunchArgument('sonars_installed', default_value='False'),
        DeclareLaunchArgument('lidar_installed', default_value='False'),
        DeclareLaunchArgument('camera_extrinsics_file', default_value='-'),
        DeclareLaunchArgument('velodyne_installed', default_value='True'),
        DeclareLaunchArgument('kinect_installed', default_value='False'),
    ]

    return launch.LaunchDescription([
        *launch_args,
        OpaqueFunction(function=load_robot_description)
    ])

