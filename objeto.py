from OpenGL.GL import *
import os

class ObjetoCarregado3D:
    def __init__(self, caminho_obj):
        self.caminho_obj = caminho_obj
        self.vertices = []
        self.coordenadas_textura = []
        self.normais = []
        self.faces = []
        
        
        self.posicao = [0.0, 0.0, 0.0]
        self.rotacao = [0.0, 0.0, 0.0]
        self.escala = [1.0, 1.0, 1.0]
        
        
        self.arquivo_textura = None 
        self.id_textura = None
        
       
        self.ka = [0.2, 0.2, 0.2]
        self.kd = [0.8, 0.7, 0.6] 
        self.ks = [1.0, 1.0, 1.0]
        self.ns = 32.0
        
        self.carregar_obj()

    def carregar_obj(self):
        if not os.path.exists(self.caminho_obj):
            print(f"[ERRO] Arquivo OBJ nao encontrado: {self.caminho_obj}")
            return

        v_temporarios = []
        vt_temporarios = []
        vn_temporarios = []

        with open(self.caminho_obj, 'r') as f:
            for linha in f:
                partes = linha.split()
                if not partes:
                    continue
                
                if partes[0] == 'v':
                    v_temporarios.append([float(partes[1]), float(partes[2]), float(partes[3])])
                elif partes[0] == 'vt':
                    vt_temporarios.append([float(partes[1]), float(partes[2])])
                elif partes[0] == 'vn':
                    vn_temporarios.append([float(partes[1]), float(partes[2]), float(partes[3])])
                elif partes[0] == 'mtllib':
                    try:
                        pasta_origem = os.path.dirname(self.caminho_obj)
                        caminho_mtl = os.path.join(pasta_origem, partes[1])
                        self.carregar_mtl(caminho_mtl)
                    except Exception as e:
                        print(f"[AVISO] Nao foi possivel processar o arquivo .mtl: {e}")
                elif partes[0] == 'f':
                    face_vertices = []
                    face_texturas = []
                    face_normais = []
                    
                    for vertice_info in partes[1:]:
                        dados = vertice_info.split('/')
                        
                        
                        idx_v = int(dados[0]) - 1
                        face_vertices.append(v_temporarios[idx_v])
                        
                        
                        if len(dados) > 1 and dados[1] != '':
                            idx_vt = int(dados[1]) - 1
                            face_texturas.append(vt_temporarios[idx_vt])
                        else:
                            face_texturas.append([0.0, 0.0])
                            
                       
                        if len(dados) > 2 and dados[2] != '':
                            idx_vn = int(dados[2]) - 1
                            face_normais.append(vn_temporarios[idx_vn])
                        else:
                            face_normais.append([0.0, 1.0, 0.0])
                    
                    self.faces.append((face_vertices, face_texturas, face_normais))

        print(f"[OK] {self.caminho_obj} carregado com sucesso.")

    def carregar_mtl(self, caminho_mtl):
        
        if not os.path.exists(caminia_mtl := caminho_mtl):
            print(f"[AVISO] Arquivo .mtl nao localizado em: {caminho_mtl}. Usando valores padrão.")
            return
            
        with open(caminho_mtl, 'r') as f:
            for linha in f:
                partes = linha.split()
                if not partes:
                    continue
                if partes[0] == 'Ka':
                    self.ka = [float(partes[1]), float(partes[2]), float(partes[3])]
                elif partes[0] == 'Kd':
                    self.kd = [float(partes[1]), float(partes[2]), float(partes[3])]
                elif partes[0] == 'Ks':
                    self.ks = [float(partes[1]), float(partes[2]), float(partes[3])]
                elif partes[0] == 'Ns':
                    self.ns = float(partes[1])
                elif partes[0] == 'map_Kd':
                    self.arquivo_textura = partes[1]

    def desenhar(self, shader_program=None):
        glPushMatrix()
        glTranslatef(self.posicao[0], self.posicao[1], self.posicao[2])
        glRotatef(self.rotacao[0], 1, 0, 0)
        glRotatef(self.rotacao[1], 0, 1, 0)
        glRotatef(self.rotacao[2], 0, 0, 1)
        glScalef(self.escala[0], self.escala[1], self.escala[2])

        
        if shader_program is not None and shader_program > 0:
            try:
                glUniform3fv(glGetUniformLocation(shader_program, "ka"), 1, self.ka)
                glUniform3fv(glGetUniformLocation(shader_program, "kd"), 1, self.kd)
                glUniform3fv(glGetUniformLocation(shader_program, "ks"), 1, self.ks)
                glUniform1f(glGetUniformLocation(shader_program, "ns"), self.ns)
                glUniform1i(glGetUniformLocation(shader_program, "tem_textura"), 1 if self.id_textura else 0)
            except Exception:
                pass

        if self.id_textura is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.id_textura)
        else:
            glDisable(GL_TEXTURE_2D)

       
        for face_verts, face_texs, face_norms in self.faces:
            glBegin(GL_POLYGON)
            for i in range(len(face_verts)):
                glNormal3fv(face_norms[i])
                glTexCoord2f(face_texs[i][0], face_texs[i][1])
                glVertex3fv(face_verts[i])
            glEnd()

        glPopMatrix()