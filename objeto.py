from OpenGL.GL import *
import os

class ObjetoCarregado3D:
    def __init__(self, caminho_obj):
        self.caminho_obj = caminho_obj
        self.vertices = []
        self.coordenadas_textura = []
        self.faces = []
        
        
        self.posicao = [0.0, 0.0, 0.0]
        self.rotacao = [0.0, 0.0, 0.0]
        self.escala = [1.0, 1.0, 1.0]
        
        
        self.arquivo_textura = None 
        self.id_textura = None
        
        self.carregar_obj()

    def carregar_obj(self):
        if not os.path.exists(self.caminho_obj):
            print(f"[ERRO] Arquivo nao encontrado: {self.caminho_obj}")
            return

        v_temporarios = []
        vt_temporarios = []

        with open(self.caminho_obj, 'r') as f:
            for linha in f:
                partes = linha.split()
                if not partes:
                    continue
                
                if partes[0] == 'v':
                    v_temporarios.append([float(partes[1]), float(partes[2]), float(partes[3])])
                
                elif partes[0] == 'vt':
                    vt_temporarios.append([float(partes[1]), float(partes[2])])
                
                elif partes[0] == 'mtllib':
                    pasta_origem = os.path.dirname(self.caminho_obj)
                    caminho_mtl = os.path.join(pasta_origem, partes[1])
                    self.carregar_mtl(caminho_mtl)

                elif partes[0] == 'f':
                    face_vertices = []
                    face_texturas = []
                    
                    for vertice_info in partes[1:]:
                        dados = vertice_info.split('/')
                        
                        idx_v = int(dados[0]) - 1
                        face_vertices.append(v_temporarios[idx_v])
                        
                        if len(dados) > 1 and dados[1] != '':
                            idx_vt = int(dados[1]) - 1
                            face_texturas.append(vt_temporarios[idx_vt])
                        else:
                            face_texturas.append([0.0, 0.0])
                    
                    self.faces.append((face_vertices, face_texturas))

        print(f"[OK] {self.caminho_obj} carregado.")

    def carregar_mtl(self, caminho_mtl):
        if not os.path.exists(caminho_mtl):
            return
        with open(caminho_mtl, 'r') as f:
            for linha in f:
                partes = linha.split()
                if not partes:
                    continue
                if partes[0] == 'map_Kd':
                    self.arquivo_textura = partes[1]

    def desenhar(self):
        """Renderiza a malha aplicando as coordenadas de textura e propriedades de iluminação"""
        glPushMatrix()
        
        
        glTranslatef(self.posicao[0], self.posicao[1], self.posicao[2])
        glRotatef(self.rotacao[0], 1, 0, 0)
        glRotatef(self.rotacao[1], 0, 1, 0)
        glRotatef(self.rotacao[2], 0, 0, 1)
        glScalef(self.escala[0], self.escala[1], self.escala[2])

       
        if self.id_textura is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.id_textura)
            glColor3f(1.0, 1.0, 1.0) 
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.7, 0.7, 0.7)

        
        glEnable(GL_RESCALE_NORMAL)

        
        for face_verts, face_texs in self.faces:
            glBegin(GL_POLYGON)
            
            
            if len(face_verts) >= 3:
                v0, v1, v2 = face_verts[0], face_verts[1], face_verts[2]
                ux, uy, uz = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
                vx, vy, vz = v2[0]-v0[0], v2[1]-v0[1], v2[2]-v0[2]
                nx = uy*vz - uz*vy
                ny = uz*vx - ux*vz
                nz = ux*vy - uy*vx
                glNormal3f(nx, ny, nz) 
            
            for i in range(len(face_verts)):
                if self.id_textura is not None:
                    glTexCoord2f(face_texs[i][0], face_texs[i][1])
                glVertex3fv(face_verts[i])
            glEnd()

        glPopMatrix()