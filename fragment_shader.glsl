#version 330 core

in vec3 vNormal;
in vec3 vFragPos;
in vec2 vTexCoord;

out vec4 fragColor;

// Propriedades do Material
uniform sampler2D textura;
uniform vec3 ka; // Coeficiente ambiente
uniform vec3 kd; // Coeficiente difuso
uniform vec3 ks; // Coeficiente especular
uniform float ns; // Brilho especular (shininess)

// Estrutura para representar as fontes de luz de 3 pontos
struct Luz {
    vec3 posicao;
    vec3 ambiente;
    vec3 difusa;
    vec3 especular;
    int ativa;
};

uniform Luz luzes[3];
uniform vec3 viewPos; // Posição da câmera para cálculo especular

void main() {
    vec3 corTextura = texture(textura, vTexCoord).rgb;
    vec3 resultadoIluminacao = vec3(0.0);
    
    vec3 normal = normalize(vNormal);
    vec3 viewDir = normalize(viewPos - vFragPos);

    for(int i = 0; i < 3; i++) {
        if(luzes[i].ativa == 0) continue;

        // 1. Componente Ambiente
        vec3 ambiente = luzes[i].ambiente * ka;

        // 2. Componente Difusa (Lambert)
        vec3 lightDir = normalize(luzes[i].posicao - vFragPos);
        float diff = max(dot(normal, lightDir), 0.0);
        vec3 difusa = luzes[i].difusa * (diff * kd);

        // 3. Componente Especular (Phong)
        vec3 reflectDir = reflect(-lightDir, normal);
        float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
        vec3 especular = luzes[i].especular * (spec * ks);

        resultadoIluminacao += (ambiente + difusa + especular);
    }

    fragColor = vec4(resultadoIluminacao * corTextura, 1.0);
}