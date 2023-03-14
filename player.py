import pygame
import globals

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.width = globals.PLAYER_W
        self.height = globals.PLAYER_H
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        
    def drawPlayer(self, screen):
        pygame.draw.rect(screen, (255,0,0),  self.rect)

    def updatePlayerPosition(self,delta,hSpeed,vSpeed,keysPressed):
        resolvedHSpeed = delta * hSpeed
        resolvedVSpeed = delta * vSpeed
        if(keysPressed[globals.PressedKeys.LEFT]): self.rect.move_ip(-resolvedHSpeed, 0)
        if(keysPressed[globals.PressedKeys.RIGHT]): self.rect.move_ip(resolvedHSpeed, 0)
        if(keysPressed[globals.PressedKeys.UP]): self.rect.move_ip(0, -resolvedVSpeed)
        if(keysPressed[globals.PressedKeys.DOWN]): self.rect.move_ip(0, resolvedVSpeed)