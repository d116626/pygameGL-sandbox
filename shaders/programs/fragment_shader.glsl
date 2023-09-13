#version 410
uniform vec2 iResolution; // Screen resolution in pixels
uniform float iTime;     // Time in seconds
out vec4 fragColor;

//https://iquilezles.org/articles/palettes/


void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    // Normalized pixel coordinates (from 0 to 1)
    // vec2 uv = fragCoord/iResolution.xy;
    vec2 uv = (fragCoord - iResolution.xy) / iResolution.y;

    float frequency = 2.0; // Adjust the frequency of the sine wave
    float amplitude = 0.2; // Adjust the amplitude of the sine wave
	float speed = 3 * iTime;
    float phase = 1.0; // Adjust the phase of the sine wave
    float sinWave = 0.0;

    for (int i = 0; i < 3; i++) {
        float chaos = (i * 0.27);
        sinWave += amplitude * sin(chaos * uv.x * frequency * 3.14159 - speed * phase * chaos);
    }




    vec2 sinCoordinate = vec2(uv.x,sinWave);
    float pct = distance(uv,sinCoordinate);
    pct = smoothstep(0.01,0.,pct);
    vec3 color = vec3(pct)*vec3(0.006,0.172,0.990);
    // Output to screen
    fragColor = vec4(color,1.0);
}


void main() {
    // Call the mainImage function with fragColor and gl_FragCoord
    mainImage(fragColor, gl_FragCoord.xy);
}
