import math
from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self, posicao=[0.0, 1.0, 5.0], up=[0.0, 1.0, 0.0], yaw=-90.0, pitch=0.0):
        
        self.posicao = posicao
        self.world_up = up
        
        
        self.yaw = yaw      
        self.pitch = pitch    
       
        self.front = [0.0, 0.0, -1.0]
        self.right = [1.0, 0.0, 0.0]
        self.up = [0.0, 1.0, 0.0]
        
       
        self.velocidade = 0.15
        self.sensibilidade = 1.0
        
       
        self.atualizar_vetores_camera()

    def atualizar_vetores_camera(self):
        
        front_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front_y = math.sin(math.radians(self.pitch))
        front_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        
        
        comprimento = math.sqrt(front_x**2 + front_y**2 + front_z**2)
        self.front = [front_x / comprimento, front_y / comprimento, front_z / comprimento]
        
       
        rx = self.front[1] * self.world_up[2] - self.front[2] * self.world_up[1]
        ry = self.front[2] * self.world_up[0] - self.front[0] * self.world_up[2]
        rz = self.front[0] * self.world_up[1] - self.front[1] * self.world_up[0]
        comp_r = math.sqrt(rx**2 + ry**2 + rz**2)
        self.right = [rx / comp_r, ry / comp_r, rz / comp_r] if comp_r != 0 else [1.0, 0.0, 0.0]
        
        
        self.up = [
            self.right[1] * self.front[2] - self.right[2] * self.front[1],
            self.right[2] * self.front[0] - self.right[0] * self.front[2],
            self.right[0] * self.front[1] - self.right[1] * self.front[0]
        ]

    def aplicar_view(self):
        """Aplica a matriz de visualização no pipeline do OpenGL baseada na câmera."""
        
        alvo = [
            self.posicao[0] + self.front[0],
            self.posicao[1] + self.front[1],
            self.posicao[2] + self.front[2]
        ]
        
        
        gluLookAt(
            self.posicao[0], self.posicao[1], self.posicao[2],  
            alvo[0], alvo[1], alvo[2],                          
            self.up[0], self.up[1], self.up[2]                  
        )

    def mover_frente_tras(self, direcao):
        """Move para frente (1) ou para trás (-1)."""
        self.posicao[0] += self.front[0] * self.velocidade * direcao
        self.posicao[1] += self.front[1] * self.velocidade * direcao
        self.posicao[2] += self.front[2] * self.velocidade * direcao

    def mover_laterais(self, direcao):
        """Move para a direita (1) ou para a esquerda (-1)."""
        self.posicao[0] += self.right[0] * self.velocidade * direcao
        self.posicao[1] += self.right[1] * self.velocidade * direcao
        self.posicao[2] += self.right[2] * self.velocidade * direcao

    def rotacionar(self, delta_yaw, delta_pitch):
        """Modifica os ângulos de visão olhando para os lados ou cima/baixo."""
        self.yaw += delta_yaw * self.sensibilidade
        self.pitch += delta_pitch * self.sensibilidade
        
       
        if self.pitch > 89.0:  self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0
        
        self.atualizar_vetores_camera()