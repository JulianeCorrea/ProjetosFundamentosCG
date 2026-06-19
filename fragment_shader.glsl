#version 120

varying vec3 fragNormal;
varying vec3 fragPosition;
varying vec2 fragTexCoord;


uniform vec3 ka;
uniform vec3 kd;
uniform vec3 ks;
uniform float ns;
uniform bool tem_textura;
uniform sampler2D textura;

void main() {
    vec3 N = normalize(fragNormal);
    vec3 V = normalize(-fragPosition); 
    
    
    vec3 ambienteTotal = vec3(0.0);
    vec3 difusaTotal = vec3(0.0);
    vec3 especularTotal = vec3(0.0);

    
    for (int i = 0; i < 3; i++) {
        vec3 lightPos = vec3(gl_LightSource[i].position);
        vec3 L;
        float atenuacao = 1.0;

        if (gl_LightSource[i].position.w == 0.0) {
            L = normalize(lightPos); // Luz Direcional
        } else {
            L = normalize(lightPos - fragPosition); 
            float d = length(lightPos - fragPosition);
            atenuacao = 1.0 / (gl_LightSource[i].constantAttenuation + gl_LightSource[i].linearAttenuation * d);
        }

        
        ambienteTotal += vec3(gl_LightSource[i].ambient) * ka;

       
        float cosTheta = max(dot(N, L), 0.0);
        difusaTotal += vec3(gl_LightSource[i].diffuse) * kd * cosTheta * atenuacao;

        
        if (cosTheta > 0.0) {
            vec3 R = reflect(-L, N);
            float cosAlpha = max(dot(R, V), 0.0);
            especularTotal += vec3(gl_LightSource[i].specular) * ks * pow(cosAlpha, ns) * atenuacao;
        }
    }

    
    vec4 corBase = vec4(1.0);
    if (tem_textura) {
        corBase = texture2D(textura, fragTexCoord);
    }

    
    vec3 corFinal = ambienteTotal + (difusaTotal * corBase.rgb) + especularTotal;
    gl_FragColor = vec4(corFinal, corBase.a);
}