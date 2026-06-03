import os
from OpenGL.GL import *

class ObjetoCarregado3D:
    def __init__(self, caminho_obj=None):
        self.vertices = []
        self.faces = [] 
        self.posicao = [0.0, 0.0, 0.0]
        self.escala = [1.0, 1.0, 1.0]
        self.rotacao = [0.0, 0.0, 0.0]
        
        if caminho_obj:
            self.carregar_obj(caminho_obj)

    def carregar_obj(self, caminho):
        if not os.path.exists(caminho):
            print(f"\n[ERRO] Arquivo '{caminho}' nao foi encontrado!")
            return

        with open(caminho, 'r') as f:
            for linha in f:
                if linha.startswith('#') or not linha.strip():
                    continue
                partes = linha.split()
                comando = partes[0]

                if comando == 'v':
                    self.vertices.append([float(partes[1]), float(partes[2]), float(partes[3])])
                elif comando == 'f':
                    face_vertices = []
                    for token in partes[1:]:
                        v_idx = int(token.split('/')[0]) - 1
                        face_vertices.append(v_idx)
                    
                    for i in range(1, len(face_vertices) - 1):
                        self.faces.append([face_vertices[0], face_vertices[i], face_vertices[i+1]])

def desenhar_objeto_malha(obj, selecionado=False):
    if not obj.vertices or not obj.faces:
        return

    glPushMatrix()
    glTranslatef(obj.posicao[0], obj.posicao[1], obj.posicao[2])
    glRotatef(obj.rotacao[0], 1, 0, 0)
    glRotatef(obj.rotacao[1], 0, 1, 0)
    glRotatef(obj.rotacao[2], 0, 0, 1)
    glScalef(obj.escala[0], obj.escala[1], obj.escala[2])

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    if selecionado:
        glColor3f(1.0, 1.0, 0.0)  # Amarelo para o selecionado
    else:
        glColor3f(0.0, 0.8, 0.8)  # Ciano para o objeto secundario

    glBegin(GL_TRIANGLES)
    for face in obj.faces:
        for v_idx in face:
            if v_idx < len(obj.vertices):
                glVertex3fv(obj.vertices[v_idx])
    glEnd()

    glDisable(GL_LIGHTING)
    glPopMatrix()