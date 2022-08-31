import zmq
import math

context = zmq.Context()
motor_0 = context.socket(zmq.REQ)
motor_0.connect("tcp://localhost:5550")

motor_1 = context.socket(zmq.REQ)
motor_1.connect("tcp://localhost:5551")

STEPS_PER_MM = (16 * 3.1415926) / 200

cur_pos = [0, 0]
cur_motors = [0, 0]

def go_to_position(position):
	global cur_pos
	
	dx = position[0] - cur_pos[0]
	dy = position[1] - cur_pos[1]
	
	d0 = (dx + dy) / STEPS_PER_MM
	d1 = (dx - dy) / STEPS_PER_MM

	print("Moving to " + str(position))
	print(d0)
	print(d1)
	
	motor_0.send_string(str(d0))
	motor_1.send_string(str(d1))
	delta_0f = int(motor_0.recv())
	delta_1f = int(motor_1.recv())

	#dx = 1/2 * (delta_0f + delta_1f)
	#dy = 1/2 * (delta_0f - delta_1f)
	
	#cur_pos = [cur_pos[0] + dx, cur_pos[1] + dy]
	
	cur_pos = position
	
	print("Move finished, now at " + str(cur_pos))
	
square_size = 50
waypoints = [[0, square_size], [square_size, square_size], [square_size, 0], [0, 0]]

#waypoints = []
#for i in range(0, 10):
#	waypoints.append([i*10, math.sin(i)*50])

#octogon
size = 100
rt = (math.sqrt(2)/2) * size
#waypoints = [[size, 0], [rt, rt], [0, size], [-rt, rt], [-size, 0], [-rt, -rt], [0, -size], [rt, -rt]]


#waypoints = [[100, 50], [-100, 20], [-50, 0], [20, 100]]

for waypoint in waypoints:
	go_to_position(waypoint)
