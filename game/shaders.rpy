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
            // УБРАЛИ функцию nSin, чтобы не ломать компилятор
            
            float t = u_time;
            vec2 u = v_tex_coord;
            float intensity = u_intensity;

            // 1. Плавное плавание
            u += vec2(sin(t * 0.4), sin(t * 0.6)) * 0.03 * intensity;

            // 2. Пульсация масштаба
            u.x = (u.x - 0.5) * (1.0 + sin(t * 0.4) * 0.15 * intensity) + 0.5;
            u.y = (u.y - 0.5) * (1.0 + sin(t * 0.1) * 0.15 * intensity) + 0.5;

            // 3. Волновое искажение
            u.x += sin(u.y * 3.0 + t) * 0.02 * intensity;
            u.y += cos(u.x * 4.5 + t) * 0.02 * intensity;

            // 4. Радиальное искажение
            float w = sin(t * 0.5) * 0.2 * intensity;
            vec2 p = u - 0.5;
            vec2 pu = vec2(length(p), atan(p.y, p.x));
            pu.x *= (1.0 / w * clamp(pu.x, 0.0, w));
            u = vec2(pu.x * cos(pu.y), pu.x * sin(pu.y)) + 0.5;

            // 5. Вибрация (ЗДЕСЬ мы просто вставили формулу nSin напрямую)
            float vibration = (sin(t * 0.8) * 0.5 + 0.5) * (sin(t * 0.2) * 0.5 + 0.5) * intensity;
            vec2 vibU = u;
            vibU.x += vibration * sin(t * 99.0) * vibration * 0.03;
            vibU.y += vibration * sin(t * 24.0) * vibration * 0.03;

            // 6. Основной сэмпл
            vec4 c = texture2D(tex0, u);

            // 7. Первый цветовой эффект
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

            gl_FragColor = vec4(c.r, c.g, c.b, c.a);
        """
    )

    def buzz_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = store.buzz_intensity
        return 0

    def buzz_mild_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 0.3
        return 0

    def buzz_strong_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 1.0
        return 0

default buzz_intensity = 0.5

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

init python:
    renpy.register_shader(
        "vape.smoke",
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
            
                // Базовые координаты и время
                vec2 st = v_tex_coord * 5.0; // Масштаб дыма
                float t = u_time * 0.3;      // Скорость

                // === СЛОЙ 1: Крупные клубы (базовый шум) ===
                vec2 i1 = floor(st);
                vec2 f1 = fract(st);
                vec2 u1 = f1 * f1 * (3.0 - 2.0 * f1);
                float h1_00 = fract(sin(dot(i1 + vec2(0.0, 0.0), vec2(12.9898, 78.233))) * 43758.5453);
                float h1_10 = fract(sin(dot(i1 + vec2(1.0, 0.0), vec2(12.9898, 78.233))) * 43758.5453);
                float h1_01 = fract(sin(dot(i1 + vec2(0.0, 1.0), vec2(12.9898, 78.233))) * 43758.5453);
                float h1_11 = fract(sin(dot(i1 + vec2(1.0, 1.0), vec2(12.9898, 78.233))) * 43758.5453);
                float n1 = mix(mix(h1_00, h1_10, u1.x), mix(h1_01, h1_11, u1.x), u1.y);

                // === СЛОЙ 2: Средние детали (искажается первым слоем для эффекта вихрей) ===
                vec2 st2 = st * 2.0 + vec2(n1 * 2.5, n1 * -2.5) + t;
                vec2 i2 = floor(st2);
                vec2 f2 = fract(st2);
                vec2 u2 = f2 * f2 * (3.0 - 2.0 * f2);
                float h2_00 = fract(sin(dot(i2 + vec2(0.0, 0.0), vec2(37.113, 53.771))) * 43758.5453);
                float h2_10 = fract(sin(dot(i2 + vec2(1.0, 0.0), vec2(37.113, 53.771))) * 43758.5453);
                float h2_01 = fract(sin(dot(i2 + vec2(0.0, 1.0), vec2(37.113, 53.771))) * 43758.5453);
                float h2_11 = fract(sin(dot(i2 + vec2(1.0, 1.0), vec2(37.113, 53.771))) * 43758.5453);
                float n2 = mix(mix(h2_00, h2_10, u2.x), mix(h2_01, h2_11, u2.x), u2.y);

                // === СЛОЙ 3: Мелкая детализация (убирает "пластиковость" и волны) ===
                vec2 st3 = st * 4.0 + vec2(n2 * 1.5, n2 * -1.5) - t * 0.5;
                vec2 i3 = floor(st3);
                vec2 f3 = fract(st3);
                vec2 u3 = f3 * f3 * (3.0 - 2.0 * f3);
                float h3_00 = fract(sin(dot(i3 + vec2(0.0, 0.0), vec2(89.432, 17.891))) * 43758.5453);
                float h3_10 = fract(sin(dot(i3 + vec2(1.0, 0.0), vec2(89.432, 17.891))) * 43758.5453);
                float h3_01 = fract(sin(dot(i3 + vec2(0.0, 1.0), vec2(89.432, 17.891))) * 43758.5453);
                float h3_11 = fract(sin(dot(i3 + vec2(1.0, 1.0), vec2(89.432, 17.891))) * 43758.5453);
                float n3 = mix(mix(h3_00, h3_10, u3.x), mix(h3_01, h3_11, u3.x), u3.y);

                // === Комбинируем слои (FBM) ===
                // n1 дает форму, n2 и n3 добавляют органичный хаос, убивая волны
                float smoke = n1 * 0.5 + n2 * 0.3 + n3 * 0.2;

                // Делаем края мягкими и пушистыми
                smoke = smoothstep(0.35, 0.85, smoke);

                // Цвет пара: светлый, белесый, с легким холодным оттенком
                vec3 fogColor = vec3(0.85, 0.88, 0.92);

                // Оригинальная сцена
                vec4 sceneColor = texture2D(tex0, v_tex_coord);

                // Смешиваем сцену и дым
                float density = smoke * u_intensity;
                vec3 finalColor = mix(sceneColor.rgb, fogColor, density);

                gl_FragColor = vec4(finalColor, sceneColor.a);
            
        """
    )

    # АВТОМАТИЧЕСКАЯ функция анимации: 1 сек появление, 3 сек рассеивание
    def vape_auto_puff(trans, st, at):
        trans.u_time = st
        
        if st < 1.0:
            trans.u_intensity = st * 0.8
        elif st < 4.0:
            progress = (st - 1.0) / 3.0
            trans.u_intensity = 0.8 * (1.0 - progress)
        else:
            trans.u_intensity = 0.0
            
        return 0

# Готовый трансформ "затяжка"
transform vape_puff:
    mesh True
    shader "vape.smoke"
    u_intensity 0.0
    function vape_auto_puff

init python:
    renpy.register_shader(
        "alcohol.party",
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
            
                vec2 uv = v_tex_coord;
                vec2 center = uv - 0.5;
                float dist = length(center); // Расстояние от центра (для виньетки и аберрации)

                // 1. Волновое искажение (пол "плывет", усиливается с опьянением)
                float wave = sin(uv.y * 12.0 + u_time * 1.5) * 0.004 * u_intensity;

                // 2. Хроматическая аберрация (раздвоение, растет от центра к краям)
                float aberration = dist * 0.035 * u_intensity;

                // Сэмплим RGB каналы со сдвигом
                float r = texture2D(tex0, uv + vec2(aberration, wave)).r;
                float g = texture2D(tex0, uv).g;
                float b = texture2D(tex0, uv - vec2(aberration * 0.5, wave)).b;
                vec3 color = vec3(r, g, b);

                // 3. Цветокоррекция: повышение насыщенности (эффект вечеринки)
                float lum = dot(color, vec3(0.299, 0.587, 0.114));
                color = mix(vec3(lum), color, 1.0 + (0.4 * u_intensity));

                // Легкий пульсирующий неоновый тинт (маджента/циан)
                color.r += sin(u_time * 0.8) * 0.06 * u_intensity;
                color.b += cos(u_time * 0.8) * 0.06 * u_intensity;

                // 4. Виньетка (туннельное зрение, края темнеют при сильном опьянении)
                float vignette = 1.0 - (dist * 0.9 * u_intensity);
                color *= clamp(vignette, 0.5, 1.0);

                // 5. Сохраняем оригинальную прозрачность сцены
                vec4 sceneColor = texture2D(tex0, uv);
                gl_FragColor = vec4(color, sceneColor.a);
            
        """
    )

    # Функция обновления для СЛАБОЙ стадии
    def alcohol_mild_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 0.35  # Легкое раздвоение, тепло, почти незаметная виньетка

    # Функция обновления для СИЛЬНОЙ стадии
    def alcohol_strong_update(trans, st, at):
        trans.u_time = st
        trans.u_intensity = 1.0   # Мир плывет, сильная аберрация, туннельное зрение

# Трансформы для удобного вызова
transform alcohol_mild:
    mesh True
    shader "alcohol.party"
    function alcohol_mild_update

transform alcohol_strong:
    mesh True
    shader "alcohol.party"
    function alcohol_strong_update

init python:
    # ==========================================
    # ШЕЙДЕР 1: Постоянный легкий шум (VHS)
    # ==========================================
    renpy.register_shader(
        "glitch.subtle",
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
           
                vec2 uv = v_tex_coord;
                vec2 uvR = uv;
                vec2 uvG = uv;
                vec2 uvB = uv;

                float r_y = fract(sin(u_time + uv.y) * 10000.0);
                float r_0 = fract(sin(u_time) * 10000.0);
                
                // Интенсивность низкая (например, 0.15), но постоянная
                float glitch_amount = 0.015 * u_intensity;

                uvR.x = uv.x - r_y * glitch_amount;
                uvB.y = uv.y + r_y * glitch_amount;

                if (uvG.y < r_y && uvB.y > r_0 - 0.2) {
                    uvG.x = uvG.x + r_y * glitch_amount;
                }

                vec4 c = vec4(
                    texture2D(tex0, uvR).r,
                    texture2D(tex0, uvG).g,
                    texture2D(tex0, uvB).b,
                    1.0
                );

                vec4 orig = texture2D(tex0, uv);
                gl_FragColor = mix(orig, c, u_intensity);
            
        """
    )

    # ==========================================
    # ШЕЙДЕР 2: Тяжелый глитч (Старый телефон)
    # ==========================================
init python:
    renpy.register_shader(
        "glitch.heavy",
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
            
                vec2 uv = v_tex_coord;
                float time = mod(u_time * 100.0, 32.0) / 110.0;
                
                float GLITCH = 0.1 + u_intensity; 
                float gnm = clamp(GLITCH, 0.0, 1.0);
                
                // Инлайн mytrunc и rand для rnd0
                vec2 trunc_time = floor(vec2(time, time) * 6.0) / 6.0;
                float rnd0 = fract(sin(dot(trunc_time, vec2(12.9898, 78.233))) * 43758.5453);
                float r0 = clamp((1.0 - gnm) * 0.7 + rnd0, 0.0, 1.0);
                
                // Инлайн mytrunc и rand для rnd1
                float trunc_x = floor(uv.x * (10.0 * r0)) / (10.0 * r0);
                float rnd1 = fract(sin(dot(vec2(trunc_x, time), vec2(12.9898, 78.233))) * 43758.5453);
                float r1 = 0.5 - 0.5 * gnm + rnd1;
                r1 = 1.0 - max(0.0, ((r1 < 1.0) ? r1 : 0.9999999));
                
                // Инлайн mytrunc и rand для rnd2
                float trunc_y1 = floor(uv.y * (40.0 * r1)) / (40.0 * r1);
                float rnd2 = fract(sin(dot(vec2(trunc_y1, time), vec2(12.9898, 78.233))) * 43758.5453);
                float r2 = clamp(rnd2, 0.0, 1.0);

                // Инлайн mytrunc и rand для rnd3
                float trunc_y2 = floor(uv.y * (10.0 * r0)) / (10.0 * r0);
                float rnd3 = fract(sin(dot(vec2(trunc_y2, time), vec2(12.9898, 78.233))) * 43758.5453);
                float r3 = (1.0 - clamp(rnd3 + 0.8, 0.0, 1.0)) - 0.1;

                // Инлайн rand для pxrnd
                float pxrnd = fract(sin(dot(uv + time, vec2(12.9898, 78.233))) * 43758.5453);

                float ofs = 0.05 * r2 * GLITCH * (rnd0 > 0.5 ? 1.0 : -1.0);
                ofs += 0.5 * pxrnd * ofs;

                uv.y += 0.1 * r3 * GLITCH;

                const int NUM_SAMPLES = 12;
                const float RCP_NUM_SAMPLES_F = 1.0 / float(NUM_SAMPLES);
                
                vec4 sum = vec4(0.0);
                vec3 wsum = vec3(0.0);
                
                for(int i = 0; i < NUM_SAMPLES; i++) {
                    float t_val = float(i) * RCP_NUM_SAMPLES_F;
                    float current_x = clamp(uv.x + ofs * t_val, 0.0, 1.0);
                    vec2 current_uv = vec2(current_x, uv.y);
                    
                    float lo = step(t_val, 0.5);
                    float hi = 1.0 - lo;
                    float remapped_t = clamp((t_val - 0.16666667) * 1.5, 0.0, 1.0);
                    float w = clamp(1.0 - abs(2.0 * remapped_t - 1.0), 0.0, 1.0);
                    float neg_w = 1.0 - w;
                    vec3 s = pow(vec3(lo, 1.0, hi) * vec3(neg_w, w, neg_w), vec3(1.0 / 2.2));
                    
                    // ИСПРАВЛЕНО: используем texture2D вместо texture
                    vec4 samplecol = texture2D(tex0, current_uv);
                    samplecol.rgb = samplecol.rgb * s;
                    sum += samplecol;
                    wsum += s;
                }
                
                sum.rgb /= wsum;
                sum.a *= RCP_NUM_SAMPLES_F;

                gl_FragColor = sum;
            
        """
    )
    def glitch_heavy_update(trans, st, at):
        trans.u_time = st
        return 0

# Трансформ для тяжелого глитча
transform glitch_heavy_fx:
    mesh True
    shader "glitch.heavy"
    u_intensity  0.85 # Сила эффекта (можно менять от 0.1 до 1.0)
    function glitch_heavy_update

init python:
    def glitch_subtle_update(trans, st, at):
        trans.u_time = st
        return 0

# Переменные состояния
default is_facetime = False
default facetime_caller = ""
default facetime_location = ""
default facetime_light = None
default facetime_emotion = "normal"
default facetime_heavy_glitch = False # Флаг для тяжелого глитча

# Трансформы
transform glitch_subtle_fx:
    mesh True
    shader "glitch.subtle"
    u_intensity 0.65 # Постоянная слабая интенсивность
    function glitch_subtle_update

