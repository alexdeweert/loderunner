from abc import abstractmethod
import quadtreenode
import pygame

class IBaseState():
    @abstractmethod
    def enter(self):
        print("BasePlayerState::enter default implementation")

    @abstractmethod
    def exit(self):
        print("BasePlayerState::exit default implementation")
    
    @abstractmethod
    def update(self):
        print("BasePlayerState::update default implementation")

    @abstractmethod
    def input(self, event):
        print("BasePlayerState::input default implementation")