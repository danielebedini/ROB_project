==INSTALLATION==

- We assume you have succesfully installed gazebo, ros and python3 on your device

- You will also need ultralytics in order to use the human recognizer

`pip install ultralytics`

- Copy the content of the Models directory to $GAZEBO_MODEL_PATH 


==BUILDING THE WORKSPACE==

- Build the workspace in ROSPlugin\catkin_ws (catkin_make), then source catkin_ws/devel/setup.bash 


==RUNNING==

- Start roscore (on a new terminal)

`roscore`
`rosparam set use_sim_time true`

- Run gazebo server (on a new terminal)

rosrun gazebo_ros gzserver --verbose [-u] <PATH TO mazefinal.sdf> to use the final version of the sdf file

The [-u] will start the simulation paused

- Run gazebo client (on a new terminal)

`gzclient` (then press play once the simulation is started if you started it with [-u])

- Things you can visualize with rqt (run rqt in a new terminal)

	- Visualize the camera at the topic husky_model/husky/camera topic

	- Visualize the rectangles around the human with the topic /yolo_human_detection/human_rectangle1

	- Control velocity and twist publishing the husky_model/husky/cmd_vel


==LAUNCH==

- Once the simulation has started (and is not paused) you can launch the package with the launch file (on a new terminal)

`roslaunch husky_gazebo_plugins start_all.launch`
