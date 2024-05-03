from geometry_msgs.msg import Point, Pose, PoseStamped, PoseWithCovarianceStamped, Quaternion, Twist
from pid_controller import PIDController
from rah01_people import RAH01People
import time
import pygame
from enum import Enum

class RAH01ActionStatus(Enum):
    READY = 0
    INTERACTING = 1
    TIMEOUT = 2


class RAH01Action:
    def __init__(self) -> None:
        self._people: RAH01People = None
        self._pid_angular = PIDController(0.04, 0.0001, 0.0001)
        self._pid_linear = PIDController(0.25, 0.0001, 0.0001)
        self._interaction_timeout = 0
        self._person_interaction_timer = 0
        self._trigger_interaction_timer = 0
        self._person_interaction_max_time = 10
        self._trigger_action_timer = 0
        self._max_angular_speed = 1.5
        self._max_lineal_speed = 1.5
        self._cmd_vel_pub = None
        self._scan_data = None
        self._tentative_action = False
        self._status: RAH01ActionStatus = RAH01ActionStatus.READY
        pygame.mixer.init()
        self._whatsapp_sound = pygame.mixer.Sound('/home/robot/rah01/sounds/whatsapp.mp3')
        self._blip_sound = pygame.mixer.Sound('/home/robot/rah01/sounds/blip.mp3')
        self._change_direction_sound = pygame.mixer.Sound('/home/robot/rah01/sounds/change_direction.mp3')
    
    @property
    def status(self):
        return self._status

    def set_people(self, people):
        self._people = people
    
    def set_cmd_vel_pub(self, pub):
        self._cmd_vel_pub = pub

    def update_scan(self, msg):
        self._scan_data = msg.ranges

    def waiting_movement(self):
        vel_command = Twist()
        vel_command.linear.x = 0
        vel_command.linear.y = 0   
        vel_command.linear.z = 0 

        vel_command.angular.x = 0 
        vel_command.angular.y = 0 
        vel_command.angular.z = 0.5

        self._cmd_vel_pub.publish(vel_command)

    def update_status(self):
        if time.time() - self._interaction_timeout < 25:
            self._status = RAH01ActionStatus.TIMEOUT
        else:
            self._status = RAH01ActionStatus.READY
            
    def play_change_direction_sound(self):
        self._change_direction_sound.play()
    
    def interact_with_person(self):
        self._blip_sound.play()
        self._status = RAH01ActionStatus.INTERACTING
        self._person_interaction_timer = time.time()
        while(time.time() - self._person_interaction_timer < self._person_interaction_max_time or self._status != RAH01ActionStatus.TIMEOUT):
            print(time.time()-self._person_interaction_timer)
            angle_diff = self._people.get_person_angle_diference()
            dis = self._people.get_person_distance()

            if dis is None:
                dis = 0
            if angle_diff is None:
                angle_diff = 0

            if dis <= 1.2 and angle_diff > -5 and angle_diff < 5:
                if not self._tentative_action:
                    self._tentative_action = True
                    self._trigger_action_timer = time.time()
                elif time.time() - self._trigger_action_timer > 1.5:
                    self._whatsapp_sound.play()
                    self._interaction_timeout = time.time()
                    self._status = RAH01ActionStatus.TIMEOUT
                    break
            else: 
                self._tentative_action = False
        
            lineal_error = (dis - 1) if dis > 1 else 0

            angular_velocity = self._pid_angular.calculate(angle_diff, 1)
            linear_velocity = self._pid_linear.calculate(lineal_error, 1)

            vel_command = Twist()
            vel_command.linear.x = 0

            if dis < 8 and dis > 1:
                vel_command.linear.x = linear_velocity 

            #Se comprueba que no choca por ninguno de los lados
            for angle in range(-90, 90, 1):
                if  self._scan_data[angle] < 0.5:
                    vel_command.linear.x = 0

            vel_command.linear.y = 0   
            vel_command.linear.z = 0 

            vel_command.angular.x = 0 
            vel_command.angular.y = 0 
            vel_command.angular.z = angular_velocity

            self._cmd_vel_pub.publish(vel_command)
            time.sleep(0.1)
        
        self._interaction_timeout = time.time()
        self._status = RAH01ActionStatus.TIMEOUT
        
        #Reiniciar el PID para evitar tener ruido en la siguiente iteración
        self._pid_angular = PIDController(0.04, 0.0001, 0.0001)
        self._pid_linear = PIDController(0.25, 0.0001, 0.0001)



    