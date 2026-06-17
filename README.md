# ProjetosFundamentosCG

# Visualizador Espacial 3D Interativo: Da Geometria às Splines de Catmull-Rom

##  Sobre o Projeto
Este repositório contém o desenvolvimento de um **Visualizador Gráfico 3D Interativo** construído do zero utilizando **Python 3** e a API **OpenGL 2.1** (através das bibliotecas `PyOpenGL` e `GLFW`). 

O objetivo do projeto foi construir, de forma incremental, uma engine gráfica capaz de carregar malhas poligonais complexas, aplicar texturização mapeada, simular modelos físicos de iluminação dinâmica (Phong), implementar navegação virtual em primeira pessoa e automatizar movimentações procedurais através de curvas matemáticas suaves com persistência de dados.

---

##  Tecnologias, Dependências e Hardware de Execução

###  Hardware Utilizado no Ambiente de Testes
Para a validação e garantia de desempenho em tempo real (60 FPS estáveis) do pipeline gráfico, a aplicação foi executada no seguinte setup:
* **Processador (CPU):** Intel(R) Core(TM) i5-14600KF (3.50 GHz, 14 Núcleos físicos e 20 Processadores lógicos)
* **Placa Gráfica (GPU):** NVIDIA GeForce GT 210 (Suporte nativo à API base do OpenGL)
* **Placa-Mãe:** B760M GAMING WIFI (Arquitetura baseada em x64)

###  Bibliotecas e Tecnologias Core
* **Python 3.10+** (Ambiente de Execução)
* **GLFW** (Gerenciamento de janelas, contexto OpenGL e captura de eventos de teclado/mouse)
* **PyOpenGL / PyOpenGL_accelerate** (Interface de comunicação direta com o pipeline de hardware da GPU)
* **Pillow (PIL)** (Processamento e decodificação de imagens de textura em tempo de execução)

---

##  Estrutura Arquitetural do Código
O ecossistema do projeto foi modularizado para seguir boas práticas de engenharia de software, separando as responsabilidades de renderização, matemática vetorial e controle de estados:

* **`main.py`**: O núcleo da aplicação. Gerencia o ciclo de vida da janela GLFW, o loop principal de renderização, o mapeamento do teclado, a inicialização das fontes de luz e o pipeline de projeção.
* **`objeto.py`**: Classe encapsulada `ObjetoCarregado3D`. Contém o *parser* geométrico para arquivos `.obj`, gerencia os estados locais do objeto (posição, rotação, escala), implementa os cálculos matemáticos das Splines e realiza as chamadas de desenho do OpenGL.
* **`camera.py`**: Classe `Camera`. Controla a matriz de visualização (*View Matrix*) em primeira pessoa através de ângulos de Euler e vetores direcionais.

---

##  Detalhamento das Etapas de Desenvolvimento

### 1ª Parte - Configuração do Ambiente e Pipeline Gráfico
Inicialização do contexto gráfico utilizando GLFW. Configuração dos estados fundamentais do OpenGL, como o buffer de profundidade (`GL_DEPTH_TEST`), mapeamento de viewport e matriz de projeção perspectiva inicial utilizando `gluPerspective`.

### 2ª Parte - Primitivas e Transformações Lineares Estáticas
Implementação manual da geometria de um cubo indexado, associando cores hexadecimais distintas para cada face. Desenvolvimento das rotinas básicas de translação, rotação e escala aplicadas diretamente na matriz de modelagem (`glPushMatrix` / `glPopMatrix`), além do sistema de alternância de foco entre objetos via tecla `TAB`.

### 3ª Parte - Parser de Arquivos Wavefront (.OBJ)
Desenvolvimento de um interpretador de texto plano dentro do `objeto.py` para extrair a topologia de modelos 3D complexos. O interpretador isola:
* Vetores de vértices (`v`)
* Coordenadas de mapeamento de textura (`vt`)
* Vetores normais à superfície (`vn`)
* Definição de polígonos por mapeamento de índices de faces (`f`)

Nesta etapa, o modelo padrão utilizado para testes foi a malha clássica *Suzanne* (do Blender).

### 4ª Parte - Mapeamento de Texturas (Coordenadas UV)
Integração com a biblioteca Pillow para carregar imagens binárias (ex: `.png`) do disco rígido. O sistema realiza a inversão vertical dos pixels (alinhando o padrão de coordenadas de textura do OpenGL) e envia a textura para a memória de vídeo da GPU com geração de identificadores únicos (`glGenTextures`). Foram aplicados filtros lineares (`GL_LINEAR`) para suavizar o mapeamento sobre as coordenadas UV geradas pelo parser das faces.

### 5ª Parte - Sistema Cinematográfico de Iluminação (Três Pontos)
Modelagem de um sistema dinâmico de iluminação baseado em técnicas de fotografia de estúdio. Três fontes de luz (`GL_LIGHT0`, `GL_LIGHT1`, `GL_LIGHT2`) são recalculadas em tempo de execução ao redor do objeto focado:
* **Key Light (Luz Principal):** Fonte de alta intensidade, gerando contraste.
* **Fill Light (Luz de Preenchimento):** Fonte de menor intensidade e tom frio para suavizar sombras.
* **Back Light (Luz de Fundo):** Posicionada atrás do objeto para criar o efeito de silhueta (*rim light*).
O sistema implementa atenuação linear baseada na distância geométrica dos fótons até a malha.

### 6ª Parte - Sombreamento Físico de Phong
Aprofundamento do pipeline de iluminação calculando a equação matemática de Phong por vértice. O modelo computa e soma as três componentes de reflexão da luz:
1. **Ambiente ($I_a$):** Iluminação global constante que simula o rebatimento indireto da luz.
2. **Difusa ($I_d$):** Intensidade baseada no cosseno do ângulo entre a normal do vértice e o vetor da luz (Lei de Lambert).
3. **Especular ($I_s$):** Brilho reflexivo concentrado (hotspot), calculado a partir do vetor de reflexão e a direção do observador, utilizando o coeficiente de rugosidade do material.

### 7ª Parte - Câmera Sintética em Primeira Pessoa (FPS)
Criação de um sistema de navegação tridimensional livre. A classe `Camera` armazena a posição do observador e calcula dinamicamente três vetores ortogonais no espaço (`front`, `right`, `up`) usando coordenadas esféricas derivadas dos ângulos de inclinação (*Pitch*) e guinada (*Yaw*). Isso permite o deslocamento linear realista (*strafing*) e a rotação livre do olhar através do teclado.

### 8ª Parte - Trajetórias Cíclicas Procedurais e Persistência
A última etapa automatiza o movimento dos objetos através de curvas perfeitamente suavizadas. O sistema utiliza as **Splines de Catmull-Rom**, que garantem continuidade geométrica $C^1$ (velocidade e direção contínuas ao passar pelos nós). 

* **Cálculo Polinomial:** A posição tridimensional instantânea do objeto é calculada por parcelas de potências em função do progresso do tempo $t$:
$$[x,y,z] = 0.5 \cdot [ (2P_1) + (-P_0 + P_2)t + (2P_0 - 5P_1 + 4P_2 - P_3)t^2 + (-P_0 + 3P_1 - 3P_2 + P_3)t^3 ]$$
* **Ciclo Fechado:** Utilizando o operador de módulo (`%`), ao atingir o fim da trajetória, o objeto retorna de forma fluida ao ponto inicial sem interrupções bruscas.
* **Persistência em Arquivo:** O usuário pode mover o objeto manualmente e pressionar uma tecla para salvar o ponto no espaço. Esses pontos são escritos em arquivos `.txt` locais, garantindo que o circuito customizado seja recarregado automaticamente nas próximas execuções.

---

##  Mapeamento Completo de Controles

###  Modos de Transformação
* `T`: Ativa o Modo de **Translação**.
* `R`: Ativa o Modo de **Rotação**.
* `S`: Ativa o Modo de **Escala**.
* `I`, `K`, `J`, `L`: Modificadores universais (Eixos X e Y) aplicados ao objeto selecionado baseado no Modo ativo acima.
* `TAB`: Alterna a seleção de foco entre os objetos da cena.

###  Navegação da Câmera (FPS)
* `W` / `S`: Move a câmera para Frente / Trás.
* `A` / `D`: Move a câmera para a Esquerda / Direita (*Strafing*).
* `Seta para Esquerda` / `Seta para Direita`: Gira o olhar horizontalmente (*Yaw*).
* `Seta para Cima` / `Seta para Baixo`: Gira o olhar verticalmente (*Pitch*).

###  Gerenciamento de Luzes (On/Off)
* `1`: Liga/Desliga a Luz Principal (*Key Light*).
* `2`: Liga/Desliga a Luz de Preenchimento (*Fill Light*).
* `3`: Liga/Desliga a Luz de Fundo (*Back Light*).

###  Sistema de Trajetórias 
* `P`: Registra a coordenada tridimensional atual do objeto como um novo ponto na trajetória e atualiza o arquivo de configuração no disco.
* `O`: Limpa completamente o circuito do objeto selecionado e zera o arquivo de texto associado.
* `Espaço`: Dá Play / Pause na animação automática ao longo da Spline (Requer no mínimo 4 pontos salvos).
