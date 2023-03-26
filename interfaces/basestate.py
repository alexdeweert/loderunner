from abc import abstractmethod
import quadtreenode
import pygame

class BaseState():
    @abstractmethod
    def enter(self):
        print("BasePlayerState::enter default implementation")

    @abstractmethod
    def exit(self):
        print("BasePlayerState::exit default implementation")
    
    #TODO: character should be character.Character (after we make it the base entity class)
    @abstractmethod
    def update(self, character):
        print("BasePlayerState::update default implementation")

    @abstractmethod
    def input(self, event):
        print("BasePlayerState::input default implementation")