# important imports
import pygame

import Utils
# The Frog Character class
class Frog:
    # Initalization
    def __init__(self,x,y,draw_sensor):
        # img
        self.img = Utils.FROG_IMG
        # start position
        self.x = x - self.img.get_width()
        self.y = y - self.img.get_height() - 7
        # velocity
        self.VEL = 20
        # velocity if on a log and motion
        self.log_vel = 0
        self.move_ticks = 0
        self.move_direction = 0
        # varible to disable motion in another direction, NO diangle movements
        self.is_moving = False
        self.on_log = False
        # lets to know when to remove frog from frogs
        self.game_over = False
        '''
        SENSORS
        -------
        '''
        # IMG t_s : top sensor, r_s : right sensor, l_s : left sensor
        self.draw_sensor = draw_sensor
        self.t_s = Utils.SENSOR_SAFE_IMG
        self.r_s = Utils.SENSOR_SAFE_IMG
        self.l_s = Utils.SENSOR_SAFE_IMG
        # sensor check. This is to say if a sensor is flagged but not detected in colision already
        self.tsc = False
        self.rsc = False
        self.lsc = False
        # sensor value. This is to return a value to the AI
        self.tsv = 0
        self.rsv = 0
        self.lsv = 0

    # A function to set motion, the frog moves on update
    def move(self,direction):
        if not self.is_moving:
            self.is_moving = True
            self.move_ticks = 0
            self.move_direction = direction
    
    # A function to actually move the frog, other stuff goes into place
    def update(self):
        # Moving the frog from input
        if self.is_moving:
            # moving to the right
            if self.move_direction == 1: self.x += self.VEL if self.x + self.VEL < Utils.WINDOW_WIDTH - self.img.get_width() else 0
            # moving to the left
            elif self.move_direction == 2: self.x -= self.VEL if self.x - self.VEL > 0 else 0
            # moving up
            elif self.move_direction == 3: self.y -= self.VEL
            # moving down (this is not something that the AI can do, but was in during testing)
            elif self.move_direction == 4: self.y += self.VEL
            # The move ticks is how long the frog will be locked into the move. Currently its 2 30fps
            self.move_ticks += 1
            if self.move_ticks == 2: self.is_moving = False
        # If the frog is on a log, move the frog with the log if possible
        if (self.x + self.log_vel < Utils.WINDOW_WIDTH - self.img.get_width() and 
            self.x + self.log_vel > 0):
            self.x += self.log_vel
        # reseting the sensor checks and the log check
        self.tsc = False
        self.rsc = False
        self.lsc = False
        self.on_log = False
    
    # Drawling the frog and the sensors *optional
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
        if self.draw_sensor: window.blit(self.t_s,(self.x,self.y-self.img.get_height()))
        if self.draw_sensor: window.blit(self.l_s,(self.x-self.img.get_width(),self.y))
        if self.draw_sensor: window.blit(self.r_s,(self.x+self.img.get_width(),self.y))
    
    # checking if the frog of its sensors collided with an object
    def colission(self,obj):
        '''
        MASKS
        -----
        '''
        obj_mask = obj.get_mask()
        frog_mask = pygame.mask.from_surface(self.img)
        ts_mask = pygame.mask.from_surface(self.t_s)
        rs_mask = pygame.mask.from_surface(self.r_s)
        ls_mask = pygame.mask.from_surface(self.l_s)
        '''
        OFFSETS
        -------
        '''
        ts_offset = (int(obj.x - self.x), int(obj.y - (self.y - self.img.get_height() )))
        ls_offset = (int(obj.x - (self.x - self.img.get_width())), int(obj.y - self.y))
        rs_offset = (int(obj.x - (self.x + self.img.get_width())), int(obj.y - self.y))
        obj_offest = (int(obj.x - self.x), int(obj.y - self.y))

        # Frog colission
        if frog_mask.overlap(obj_mask,obj_offest):
            if obj.name == 'log':
                self.log_vel = obj.VEL
                self.on_log = True
                self.game_over = False
            if obj.name == 'truck':
                self.game_over = True
        elif not self.on_log: 
            self.log_vel = 0
            if self.y < 320:
                self.game_over = True
        
        # Top Sensor Colission
        if ts_mask.overlap(obj_mask,ts_offset): 
            if obj.name == 'truck':
                self.t_s = Utils.SENSOR_DANGER_IMG
                self.tsv = -1
            elif obj.name == 'log':
                self.t_s = Utils.SENSOR_SAFE_IMG
                self.tsv = 1
            self.tsc = True
        elif not self.tsc:
            if (self.y - self.img.get_height()) > 120 and (self.y - self.img.get_height()) < 320:
                self.t_s = Utils.SENSOR_DANGER_IMG
                self.tsv = -1
            else: 
                self.t_s = Utils.SENSOR_SAFE_IMG
                self.tsv = 1

        # Right Sensor Colission
        if rs_mask.overlap(obj_mask,rs_offset): 
            if obj.name == 'truck':
                self.r_s = Utils.SENSOR_DANGER_IMG
                self.rsv = -1
            elif obj.name == 'log':
                self.r_s = Utils.SENSOR_SAFE_IMG
                self.rsv = 1
            self.rsc = True
        elif not self.rsc: 
            if self.y > 120 and self.y < 320:
                self.r_s = Utils.SENSOR_DANGER_IMG
                self.rsv = -1
            else: 
                self.r_s = Utils.SENSOR_SAFE_IMG
                self.rsv = 1

        # Left Sensor Colission
        if ls_mask.overlap(obj_mask,ls_offset): 
            if obj.name == 'truck':
                self.l_s = Utils.SENSOR_DANGER_IMG
                self.lsv = -1
            elif obj.name == 'log':
                self.l_s = Utils.SENSOR_SAFE_IMG
                self.lsv = 1
            self.lsc = True
        elif not self.lsc: 
            if self.y > 120 and self.y < 320:
                self.l_s = Utils.SENSOR_DANGER_IMG
                self.lsv = -1
            else: 
                self.l_s = Utils.SENSOR_SAFE_IMG
                self.lsv = 1