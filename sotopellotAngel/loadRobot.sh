rosservice call gazebo/delete_model fw_robot
rosrun gazebo_ros spawn_model -file models/fw_robot_model.sdf -sdf -model fw_robot -y 0 -x 0 -z 1.0