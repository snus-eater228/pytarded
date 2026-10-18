# init python:
#     renpy.register_shader(
#         "fever.vision",
#         variables="""
#             uniform sampler2D u_tex0;           // Системное имя текстуры
#             uniform float u_fever_stage;
#             uniform float u_fever_intensity;
#             uniform float u_time;
#             varying vec2 v_tex_coord;
#         """,
#         fragment_300="""
#             float severity = clamp(u_fever_intensity, 0.0, 1.0);
#             float stage = clamp(u_fever_stage, 0.0, 1.0);

#             vec2 uv = v_tex_coord;
#             vec2 p = uv - vec2(0.5);
#             float radius = length(p);

#             float sway = sin(u_time * 0.53 + p.y * 3.0);
#             float driftX = sin(u_time * 0.43) + 0.35 * sin(u_time * 0.91 + 1.0);
#             float driftY = cos(u_time * 0.37 + 0.7) + 0.25 * sin(u_time * 0.67);

#             vec2 offset = vec2(
#                 sin(uv.y * 5.0 + u_time * 0.43),
#                 cos(uv.x * 4.0 + u_time * 0.37)
#             ) * severity * 0.0025;

#             offset += vec2(driftX, driftY) * severity * stage * 0.003;
#             offset += vec2(sway, -sway) * severity * stage * 0.0015;

#             float beat = 0.5 + 0.5 * sin(u_time * 1.1);
#             beat = pow(beat, 5.0);

#             float zoom = beat * severity * mix(0.002, 0.009, stage);

#             vec2 warped = (uv - 0.5) * (1.0 + zoom) + 0.5 + offset;
#             warped = clamp(warped, vec2(0.001), vec2(0.999));

#             float edge = smoothstep(0.12, 0.65, radius);
#             float ca = severity * edge * mix(0.001, 0.007, stage);

#             vec4 center = texture(u_tex0, warped);

#             float red = texture(u_tex0, clamp(warped + vec2(ca, 0.0), vec2(0.001), vec2(0.999))).r;
#             float blue = texture(u_tex0, clamp(warped - vec2(ca, 0.0), vec2(0.001), vec2(0.999))).b;

#             vec3 color = vec3(red, center.g, blue);

#             float temperature = 0.5 + 0.5 * sin(u_time * 0.23 + 0.8);
#             vec3 coldTint = vec3(0.94, 0.98, 1.035);
#             vec3 hotTint = vec3(1.06, 0.97, 0.90);
#             vec3 tint = mix(coldTint, hotTint, temperature);

#             color = mix(color, color * tint, severity * 0.8);

#             float lum = dot(color, vec3(0.299, 0.587, 0.114));
#             float desat = severity * mix(0.06, 0.22, stage);
#             color = mix(color, vec3(lum), desat);

#             float vignette = smoothstep(mix(0.72, 0.38, stage), mix(1.05, 0.78, stage), radius);
#             float fade = vignette * severity * stage * 0.48;

#             color *= 1.0 - fade;

#             // Вывод цвета по стандарту GLSL 3.00 в Ren'Py
#             fragment_color = vec4(color, center.a);
#         """
#     )

# init python:
#     # Основная функция для динамического управления
#     def fever_layer_update(trans, st, at):
#         trans.u_time = st
#         trans.u_fever_stage = store.fever_stage
#         trans.u_fever_intensity = store.fever_intensity
#         return 0  # 0 = обновлять каждый кадр

#     # Пресет: Легкая болезнь
#     def fever_mild_update(trans, st, at):
#         trans.u_time = st
#         trans.u_fever_stage = 0.0
#         trans.u_fever_intensity = 0.38
#         return 0

#     # Пресет: Тяжелая болезнь
#     def fever_severe_update(trans, st, at):
#         trans.u_time = st
#         trans.u_fever_stage = 1.0
#         trans.u_fever_intensity = 0.85
#         return 0

#     # Пресет: Нарастающая болезнь (за 12 секунд)
#     def fever_worsening_update(trans, st, at):
#         trans.u_time = st
#         # Плавная интерполяция значений на основе времени (st)
#         progress = min(st / 12.0, 1.0)
#         trans.u_fever_stage = progress
#         trans.u_fever_intensity = 0.25 + (0.60 * progress) # от 0.25 до 0.85
#         return 0

# # Если ты хочешь использовать готовые пресеты (как в твоем коде), они тоже должны выглядеть так:
# transform fever_mild:
#     mesh True
#     shader "fever.vision"
#     function fever_mild_update

# transform fever_severe:
#     mesh True
#     shader "fever.vision"
#     function fever_severe_update

# transform fever_worsening:
#     mesh True
#     shader "fever.vision"
#     function fever_worsening_update

init python:
    renpy.register_shader(
        "fever.dream",
        variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_intensity;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
            gl_Position = u_transform * vec4(a_position.xy, 0.0, 1.0);
        """,
        fragment_300="""

            float speed = 0.2;
            float time = u_time * speed;
            vec2 uv = v_tex_coord;
            
            // 1. Тряска и "дыхание"
            float shakingForce = 0.05 * u_intensity;
            uv += vec2(sin(uv.y + time), cos(uv.x + time)) * shakingForce;

            // 2. Волновое искажение
            float sizeWave = 5.0;
            float n = sin(uv.x * sizeWave + time) * sin(uv.y * sizeWave + time) * 0.01 * u_intensity;
            uv += n;

            // 3. Основной цвет (сразу берем альфа-канал)
            vec4 texColor = texture2D(tex0, uv);
            vec3 finalColor = texColor.xyz * 1.2;

            // 4. Хроматический сдвиг
            float shiftForCam = 0.01 * u_intensity;
            vec4 texColor2 = texture2D(tex0, uv + vec2(shiftForCam, 0.0));
            finalColor *= texColor2.xyz;

            // 5. Психоделический фильтр
            vec3 narcColor = 0.9 + 0.1 * cos(u_time + uv.xyx + vec3(0.0, 2.0, 4.0));
            finalColor *= narcColor * (1.0 + 0.1 * u_intensity);

            // ИСПРАВЛЕНО: передаем оригинальную прозрачность (texColor.a) вместо 1.0
            gl_FragColor = vec4(finalColor.r, finalColor.g, finalColor.b, texColor.a);
        """
    )

    # Функции обновления
    def fever_dream_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = store.fever_intensity
        return 0

    def fever_dream_mild_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 0.7
        return 0

    def fever_dream_severe_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 1.5
        return 0

# Глобальная переменная
default fever_intensity = 0.5

# Трансформы
transform fever_dream:
    mesh True
    shader "fever.dream"
    u_intensity 0.5
    function fever_dream_update

transform fever_dream_mild:
    mesh True
    shader "fever.dream"
    function fever_dream_mild_update

transform fever_dream_severe:
    mesh True
    shader "fever.dream"
    function fever_dream_severe_update

init python:
    renpy.register_shader(
        "buzz",
        variables="""
            uniform sampler2D tex0;
            uniform float u_time;
            uniform float u_intensity;
            varying vec2 v_tex_coord;
        """,
        vertex_300="""
            v_tex_coord = a_tex_coord;
            gl_Position = u_transform * vec4(a_position.xy, 0.0, 1.0);
        """,
        fragment_300="""
            precision mediump float;

            float nSin(float x) {
                return sin(x) * 0.5 + 0.5;
            }

            float t = u_time;
            vec2 u = v_tex_coord;

            // Масштабируем интенсивность
            float intensity = u_intensity;

            // 1. Плавное плавание
            u += vec2(sin(t * 0.4), sin(t * 0.6)) * 0.03 * intensity;

            // 2. Пульсация масштаба
            u.x = (u.x - 0.5) * (1.0 + sin(t * 0.4) * 0.15 * intensity) + 0.5;
            u.y = (u.y - 0.5) * (1.0 + sin(t * 0.1) * 0.15 * intensity) + 0.5;

            // 3. Волновое искажение
            u.x += sin(u.y * 3.0 + t) * 0.02 * intensity;
            u.y += cos(u.x * 4.5 + t) * 0.02 * intensity;

            // 4. Радиальное искажение (туннель/рыбий глаз)
            float w = sin(t * 0.5) * 0.2 * intensity;
            vec2 p = u - 0.5;
            vec2 pu = vec2(length(p), atan(p.y, p.x));
            pu.x *= (1.0 / w * clamp(pu.x, 0.0, w));
            u = vec2(pu.x * cos(pu.y), pu.x * sin(pu.y)) + 0.5;

            // 5. Вибрация/дрожание
            float vibration = nSin(t * 0.8) * nSin(t * 0.2) * intensity;
            vec2 vibU = u;
            vibU.x += vibration * sin(t * 99.0) * vibration * 0.03;
            vibU.y += vibration * sin(t * 24.0) * vibration * 0.03;

            // 6. Основной сэмпл
            vec4 c = texture2D(tex0, u);

            // 7. Первый цветовой эффект (пороговый)
            float r1 = 0.5 * sin(t * 4.0) + 0.6;
            float g1 = 0.1 * sin(t * 2.0) + 0.8;
            float b1 = 0.2 * sin(t * 3.51) + 0.2;
            float t1 = 0.5 * sin(t) + 1.0;
            float rc1 = 0.5 * sin(t * 4.0) + 0.6;
            float gc1 = 0.1 * sin(t * 2.0) + 0.8;
            float bc1 = 0.2 * sin(t * 3.51) + 0.2;

            if (r1 * c.r + g1 * c.g + b1 * c.b > t1) {
                c.r *= rc1;
                c.g *= gc1;
                c.b *= bc1;
            }

            // 8. Второй цветовой эффект
            float r2 = 0.3 * sin(t * 4.0) - 0.3;
            float g2 = 0.2 * sin(t * 2.0) + 0.8;
            float b2 = 0.1 * sin(t * 3.51) + 0.2;
            float t2 = 0.3 * sin(t * 0.9) + 0.9;
            float rc2 = 0.1 * sin(t * 2.0) + 0.6;
            float gc2 = 0.2 * sin(t * 1.0) + 0.8;
            float bc2 = 0.4 * sin(t * 0.51) + 0.2;

            if (r2 * c.r + g2 * c.g + b2 * c.b < t1) {
                c.r *= rc2;
                c.g *= gc2;
                c.b *= bc2;
            }

            // 9. Наложение вибрирующего сэмпла
            vec4 vibSamp = texture2D(tex0, vibU);
            c.rgb += vibSamp.rgb * vibration;

            // Сохраняем прозрачность
            gl_FragColor = vec4(c.r, c.g, c.b, c.a);
        """
    )

    # Функции обновления
    def buzz_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = store.buzz_intensity
        return 0

    def buzz_mild_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 0.3  # Лёгкое опьянение
        return 0

    def buzz_strong_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 1.0  # Сильный "приход"
        return 0

# Глобальная переменная
default buzz_intensity = 0.5

# Трансформы
transform buzz:
    mesh True
    shader "buzz"
    u_intensity 0.5
    function buzz_update

transform buzz_mild:
    mesh True
    shader "buzz"
    function buzz_mild_update

transform buzz_strong:
    mesh True
    shader "buzz"
    function buzz_strong_update