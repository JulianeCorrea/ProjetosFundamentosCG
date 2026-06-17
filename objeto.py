# -*- coding: utf-8 -*-
import math
import os  
from OpenGL.GL import *

class ObjetoCarregado3D:
    def __init__(self, caminho_obj):
        self.caminho_obj = caminho_obj
        self.posicao = [0.0, 0.0, 0.0]
        self.rotacao = [0.0, 0.0, 0.0]
        self.escala = [1.0, 1.0, 1.0]
        self.id_textura = None
        self.arquivo_textura = None
        
        
        self.pontos_controle = []  
        self.t_atual = 0.0
        self.ponto_origem_idx = 0
        
        self.vertices = []
        self.texturas = []
        self.normais = []
        self.faces = []
        self.carregar_obj()

    def carregar_obj(self):
        """Lê o arquivo .obj e extrai vértices, texturas, normais e faces."""
        if not os.path.exists(self.caminho_obj):
            print(f"[ERRO] Arquivo não encontrado: {self.caminho_obj}")
            return

        with open(self.caminho_obj, "r") as f:
            for linha in f:
                if linha.startswith("#") or not linha.strip():
                    continue
                
                partes = linha.split()
                if not partes:
                    continue
                
                comando = partes[0]
                
                if comando == "v":
                    self.vertices.append([float(partes[1]), float(partes[2]), float(partes[3])])
                elif comando == "vt":
                    self.texturas.append([float(partes[1]), float(partes[2])])
                elif comando == "vn":
                    self.normais.append([float(partes[1]), float(partes[2]), float(partes[3])])
                elif comando == "map_Kd":
                    self.arquivo_textura = partes[1]
                elif comando == "f":
                    face_vertices = []
                    for vertice in partes[1:]:
                        indices = vertice.split("/")
                        idx_v = int(indices[0]) - 1
                        idx_t = int(indices[1]) - 1 if len(indices) > 1 and indices[1] else None
                        idx_n = int(indices[2]) - 1 if len(indices) > 2 and indices[2] else None
                        face_vertices.append((idx_v, idx_t, idx_n))
                    self.faces.append(face_vertices)

    def calcular_catmull_rom(self, p0, p1, p2, p3, t):
        """Calcula a equação polinomial exata do slide de Catmull-Rom."""
        t2 = t * t
        t3 = t2 * t
        
        
        resultado = [0.0, 0.0, 0.0]
        for i in range(3):
            termo_constante = 2.0 * p1[i]
            termo_t          = -p0[i] + p2[i]
            termo_t2         = 2.0 * p0[i] - 5.0 * p1[i] + 4.0 * p2[i] - p3[i]
            termo_t3         = -p0[i] + 3.0 * p1[i] - 3.0 * p2[i] + p3[i]
            
            resultado[i] = 0.5 * (termo_constante + termo_t * t + termo_t2 * t2 + termo_t3 * t3)
            
        return resultado

    def atualizar_trajetoria(self, passo_velocidade=0.01):
        """Move o objeto ao longo dos pontos de controle salvos de forma cíclica."""
        qtd_pontos = len(self.pontos_controle)
        if qtd_pontos < 4: 
            return
        self.t_atual += passo_velocidade
        if self.t_atual >= 1.0:
            self.t_atual = 0.0
            
            self.ponto_origem_idx = (self.ponto_origem_idx + 1) % qtd_pontos

        
        idx0 = (self.ponto_origem_idx - 1) % qtd_pontos
        idx1 = self.ponto_origem_idx
        idx2 = (self.ponto_origem_idx + 1) % qtd_pontos
        idx3 = (self.ponto_origem_idx + 2) % qtd_pontos

        p0 = self.pontos_controle[idx0]
        p1 = self.pontos_controle[idx1]
        p2 = self.pontos_controle[idx2]
        p3 = self.pontos_controle[idx3]

        
        self.posicao = self.calcular_catmull_rom(p0, p1, p2, p3, self.t_atual)

    def salvar_trajetoria_em_arquivo(self, indice_nome):
        """Salva a lista de pontos em um arquivo de texto plano (Persistência de Dados)."""
        nome_arquivo = f"trajetoria_obj{indice_nome}.txt"
        with open(nome_arquivo, "w") as f:
            for pt in self.pontos_controle:
                f.write(f"{pt[0]},{pt[1]},{pt[2]}\n")
        print(f"[ARQUIVO] Trajetória gravada com sucesso em: {nome_arquivo}")

    def carregar_trajetoria_de_arquivo(self, indice_nome):
        """Tenta ler um arquivo de configuração de pontos salvo anteriormente."""
        nome_arquivo = f"trajetoria_obj{indice_nome}.txt"
        if os.path.exists(nome_arquivo):
            self.pontos_controle = []
            with open(nome_arquivo, "r") as f:
                for linha in f:
                    if linha.strip():
                        coordenadas = [float(x) for x in linha.strip().split(",")]
                        self.pontos_controle.append(coordenadas)
            print(f"[ARQUIVO] Trajetória importada de {nome_arquivo} ({len(self.pontos_controle)} pontos).")

    def desenhar(self):
        """Aplica as transformações geométricas e renderiza as faces do objeto."""
        glPushMatrix()
        
        #
        glTranslatef(self.posicao[0], self.posicao[1], self.posicao[2])
        glRotatef(self.rotacao[0], 1, 0, 0)
        glRotatef(self.rotacao[1], 0, 1, 0)
        glScalef(self.escala[0], self.escala[1], self.escala[2])

        
        if self.id_textura is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.id_textura)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glDisable(GL_TEXTURE_2D)
            glColor3f(0.7, 0.7, 0.7)

        
        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            elif len(face) == 4:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_POLYGON)

            for vertice in face:
                idx_v, idx_t, idx_n = vertice
                if idx_n is not None and idx_n < len(self.normais):
                    glNormal3fv(self.normais[idx_n])
                if idx_t is not None and idx_t < len(self.texturas):
                    glTexCoord2fv(self.texturas[idx_t])
                glVertex3fv(self.vertices[idx_v])
                
            glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()