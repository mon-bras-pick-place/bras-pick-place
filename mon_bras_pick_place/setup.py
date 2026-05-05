from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'mon_bras_pick_place'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), 
         glob(os.path.join('launch', '*.[pxy][yma]*'))),
        (os.path.join('share', package_name, 'config'), 
         glob(os.path.join('config', '*.yaml'))),
        (os.path.join('share', package_name, 'worlds'), 
         glob(os.path.join('worlds', '*.*'))),
        (os.path.join('share', package_name, 'models'), 
         glob(os.path.join('models', '**', '*.*'), recursive=True)),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='yasmine',
    maintainer_email='yasmine@todo.todo',
    description='Pick and Place simulation with MuJoCo - 6DOF Robot Arm',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'pick_place = mon_bras_pick_place.pick_place_node:main',
            'ros_control = mon_bras_pick_place.ros_control_node:main',
        ],
    },
)