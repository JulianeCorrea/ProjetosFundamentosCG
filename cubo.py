import numpy as np
from OpenGL.GL import *

class Cubo:
    def __init__(self):
        
        self.vertices = [
            [-0.5, -0.5,  0.5], [ 0.5, -0.5,  0.5], [ 0.5,  0.5,  0.5], [-0.5,  0.5,  0.5], # Frente
            [-0.5, -0.5, -0.5], [ 0.5, -0.5, -0.5], [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5]  # Trás
        ]
        
       
        self.faces = [
            {'indices': [0, 1, 2, 2, 3, 0], 'cor': [1.0, 0.0, 0.0]}, 
            {'indices': [1, 5, 6, 6, 2, 1], 'cor': [0.0, 1.0, 0.0]}, 
            {'indices': [7, 6, 5, 5, 4, 7], 'cor': [0.0, 0.0, 1.0]}, 
            {'indices': [4, 0, 3, 3, 7, 4], 'cor': [1.0, 1.0, 0.0]}, 
            {'indices': [3, 2, 6, 6, 7, 3], 'cor': [1.0, 0.0, 1.0]}, 
            {'indices': [4, 5, 1, 1, 0, 4], 'cor': [0.0, 1.0, 1.0]}  
        ]
        
        
        self.posicao = [0.0, 0.0, 0.0]
        self.escala = [1.0, 1.0, 1.0]
        self.rotacao = [0.0, 0.0, 0.0]

def desenhar_cubo(cubo):
    glPushMatrix()
   
    glTranslatef(cubo.posicao[0], cubo.posicao[1], cubo.posicao[2])
    glRotatef(cubo.rotacao[0], 1, 0, 0)
    glRotatef(cubo.rotacao[1], 0, 1, 0)
    glRotatef(cubo.rotacao[2], 0, 0, 1)
    glScalef(cubo.escala[0], cubo.escala[1], cubo.escala[2])
    
    glBegin(GL_TRIANGLES)
    for face in cubo.faces:
        glColor3f(*face['cor'])
        for idx in face['indices']:
            glVertex3fv(cubo.vertices[idx])
    glEnd()
    glPopMatrix()