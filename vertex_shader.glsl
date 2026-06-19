#version 120

varying vec3 fragNormal;
varying vec3 fragPosition;
varying vec2 fragTexCoord;

void main() {
    
    fragNormal = normalize(gl_NormalMatrix * gl_Normal);
    
    
    fragPosition = vec3(gl_ModelViewMatrix * gl_Vertex);
    
   
    fragTexCoord = vec2(gl_MultiTexCoord0);
    
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}