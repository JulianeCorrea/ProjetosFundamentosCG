#version 330 core

// Entradas vindas do Vertex Shader
in vec3 FragPos;      // Posição do fragmento no espaço do mundo
in vec3 Normal;       // Normal do fragmento (já rotacionada)
in vec2 TexCoords;    // Coordenadas de textura

// Saída de cor para a tela
out vec4 FragColor;

// Estrutura para os coeficientes do Material (.mtl)
struct Material {
    vec3 ka;          // Coeficiente ambiente
    vec3 kd;          // Coeficiente difuso
    vec3 ks;          // Coeficiente especular
    float shininess;  // Brilho/Polimento (ns)
};

// Estrutura para as Fontes de Luz (Iluminação de 3 Pontos)
struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    bool isActive;    // Teclado vai ligar/desligar aqui
};

// Uniforms enviados pelo C++/Python
uniform Material material;
uniform Light lights[3];      // Array com as 3 luzes (Key, Fill, Rim)
uniform vec3 viewPos;         // Posição da câmera no mundo
uniform sampler2D texture_diffuse; // A textura do objeto
uniform bool useTexture;      // Atalho de teclado para ligar/desligar textura

// Função auxiliar para calcular a luz de Phong para uma fonte individual
vec3 CalcLight(Light light, vec3 normal, vec3 fragPos, vec3 viewDir, vec3 baseColor) {
    if (!light.isActive) return vec3(0.0);

    // 1. Componente Ambiente
    vec3 ambient = light.ambient * material.ka;

    // 2. Componente Difusa
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = light.diffuse * (diff * baseColor); // Usa a cor base (textura ou kd)

    // 3. Componente Especular
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * (spec * material.ks);

    return (ambient + diffuse + specular);
}

void main() {
    // Normaliza os vetores de entrada
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(viewPos - FragPos);

    // Determina a cor base: Textura, cor Kd do material, ou ambos combinados
    vec3 baseColor = material.kd;
    if (useTexture) {
        baseColor = texture(texture_diffuse, TexCoords).rgb;
    }

    // Acumula o cálculo das 3 fontes de luz (Key, Fill, Rim)
    vec3 result = vec3(0.0);
    for(int i = 0; i < 3; i++) {
        result += CalcLight(lights[i], norm, FragPos, viewDir, baseColor);
    }

    // Aplica a cor final ao pixel
    FragColor = vec4(result, 1.0);
}
