import time
import sys
import RPi.GPIO as GPIO

from RpiMotorLib import RpiMotorLib
import zmq

motor_id = int(sys.argv[len(sys.argv) - 1])
print("running for motor " + str(motor_id))

MS_Pins = [(14, 15, 18), (14, 15, 18)]
DIR = [20, 24]
STEP = [21, 23]

current_position = 0

motor = RpiMotorLib.A4988Nema(DIR[motor_id], STEP[motor_id], MS_Pins[motor_id], "A4988")

context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:555" + str(motor_id))

while True:
	target = int(float(socket.recv()))
	print("motor " + str(motor_id) + " going to position: " + str(target))

	#delta = current_position + target 
	delta = target #we are just sending d0 and d1, not target pos
	current_position += delta

	motor.motor_go(delta < 0, "Full", abs(delta), 0.0005, False, 0.05)
	socket.send_string(str(current_position))
# motor.motor_go(False, "Full", 200, 0.001, False, 0.05)


# GPIO.cleanup()

