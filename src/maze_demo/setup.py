from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup
d = generate_distutils_setup(
    packages=['mouse_common', 'rospy_message_converter', 'pyamaze'],
    package_dir={'': 'src'}
)
setup(**d)
