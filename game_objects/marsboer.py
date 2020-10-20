"""============================================================================

  Basic game object

  parameters:
    boundery  : boundary of movement
    position  : Start position. (default to center of boundry)
    speed     : Optional
    direction : in degrees 0-359 counting counter clockwise and 0 = right (optional)

============================================================================"""
import pygame
import math
from game_functions.gameobject import *

class BasicObject(Gameobject):
  # Variables to store animations and sounds common to all AlienAlvin1 object
  loaded = False
  sprite = None

  # === Initialize AlienAlvin1 ===
  def __init__(self, boundary = None, position = None, direction = 0, speed = 0, delay = 0):
    print("init marsboer")
    
    # Load animations and sounds first time this class is used
    if not BasicObject.loaded:
      # Run this the first time this class is used
      BasicObject.size = (100,100)
      BasicObject.sprite = self.Animation("marsboer.png", (100,100), BasicObject.size) # Load sprite map
      BasicObject.loaded = True # Indicate that all common external attributes are loaded

    # Inherit from game object class
    Gameobject.__init__(self, boundary, position, self.sprite.size, speed, direction)

    # Set charakteristica other than default
    self.type = self.Type.NEUTRAL # Type of object:   NEUTRAL, CGO, UNFREINDLY,  PLAYER, FREINDLY, PLAYER_OPPONENT

    # Delayed deployment
    self.delay = delay
    self.inactive = self.invisible = delay > 0
    

  # === Movement ===
  def update(self, scroll):
    if self.invisible: 
      # wait fro delay to activate
      if (pygame.time.get_ticks() - self.game_state.level_time) // 1000 > self.delay:
        self.inactive = self.invisible = False
      else:
        return

    if scroll[0] or scroll[1]:
      self.boundary.move(scroll)
      self.rect.move(scroll)

    # test if out of boundary and deflect sprite by mirroring direction
    if self.touch_boundary():
      self.mirror_direction()

    # Move sprite according to speed and direction
    self.move()

  # === Draw on game surface ===
  def draw(self, surface):
    if self.invisible:
      return

    # Flip image when direction is left
    surface.blit(self.sprite.get_surface(0),self.rect)


  # === When hit or hitting something ===
  def hit(self, obj):
    if self.invisible:
      return 
    if obj.type == self.Type.PLAYER or obj.type == self.Type.FREINDLY:
      print("Alien hit by",obj.__class__.__name__)
      self.health -= obj.impact_power

    # Check if i'm dead
    if self.health <=0:  
      self.delete = True
      self.game_state.score += 1
