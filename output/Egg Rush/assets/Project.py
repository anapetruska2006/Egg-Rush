import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# --- Звук
click_sound = pygame.mixer.Sound("assets/sounds/click.mp3")
drop_sound = pygame.mixer.Sound("assets/sounds/drop.mp3")
open_inventory_sound = pygame.mixer.Sound("assets/sounds/inventory_open.mp3")
close_inventory_sound = pygame.mixer.Sound("assets/sounds/inventory_close.mp3")
purchase_success_sound = pygame.mixer.Sound("assets/sounds/purchase_success.mp3")
purchase_fail_sound = pygame.mixer.Sound("assets/sounds/purchase_fail.mp3")
multi_pop_sound = pygame.mixer.Sound("assets/sounds/multi_pop.mp3")

# --- Загрузка музыки
music_tracks = [
    "assets/music/musik_1.mp3",
    "assets/music/musik_2.mp3",
    "assets/music/musik_3.mp3",
    "assets/music/musik_4.mp3",
    "assets/music/musik_5.mp3",
    "assets/music/musik_6.mp3",
    "assets/music/musik_7.mp3",
    "assets/music/musik_8.mp3",
    "assets/music/musik_9.mp3",
    "assets/music/musik_10.mp3",
    "assets/music/musik_11.mp3",
    "assets/music/musik_12.mp3",
    "assets/music/musik_13.mp3",
    "assets/music/musik_14.mp3",
    "assets/music/musik_15.mp3"
]

current_track = 0  # Начинаем с первого трека

# --- Фоновая музыка
pygame.mixer.music.load(music_tracks[current_track])  # Загружаем первый трек
pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость музыки

# --- Окно
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Egg Rush")

# --- Загрузка изображений
background = pygame.image.load("assets/background.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

egg_images = [
    pygame.image.load("assets/egg1.png").convert_alpha(),
    pygame.image.load("assets/egg2.png").convert_alpha()
]
egg_index = 0
egg_center = (WIDTH // 2, HEIGHT // 2)

info_icon_img = pygame.image.load("assets/info_icon.png").convert_alpha()
info_icon_img = pygame.transform.scale(info_icon_img, (150, 150))
info_icon_rect = info_icon_img.get_rect(topleft=(WIDTH - 110, -30))

inventory_icon_empty = pygame.image.load("assets/inventory_icon.png").convert_alpha()
inventory_icon_full = pygame.image.load("assets/inventory_icon_full.png").convert_alpha()
inventory_icon_img = pygame.transform.scale(inventory_icon_empty, (150, 150))  # размер картинки
inventory_icon_rect = inventory_icon_img.get_rect(topleft=(WIDTH - 170, 230))  # повороти, спуск вниз.

map_icon_img = pygame.image.load("assets/map_icon.png").convert_alpha()
map_icon_img = pygame.transform.scale(map_icon_img, (150, 150))  # увеличенный размер
map_icon_rect = map_icon_img.get_rect(topleft=(WIDTH - 170, 360))  # под инвентарем

# --- Карты
map_images = [
    {"file": "assets/maps/mape2.jpg", "cost": 350},  # 350 - preis
    {"file": "assets/maps/mape3.jpg", "cost": 700},  # 700 - preis
    {"file": "assets/maps/mape4.jpg", "cost": 1650},  # 1650 - preis
    {"file": "assets/maps/mape5.jpg", "cost": 2680},  # 2680 - preis
    {"file": "assets/maps/mape6.jpg", "cost": 5999},  # 5999 - preis
    {"file": "assets/maps/mape7.jpg", "cost": 12000},  # 12000 - preis
]
selected_map_index = None
show_map_shop = False
purchased_maps = []  # Переменная для прорисовки названия (Куплено)
inventory_scroll_offset = 0  # скроллинг не работает!
inventory_max_scroll = 0

# --- Шрифт
font = pygame.font.SysFont("Arial", 25, bold=True)
small_font = pygame.font.SysFont("Arial", 13, bold=True)
big_font = pygame.font.SysFont(None, 36)

# --- Скины
penguin_skin = {"name": "Penguin", "main": "assets/skins/skin_penguin.png", "anim": "assets/skins/skin_penguin1.png",
                "rarity": "rare"}
baba_skin = {"name": "Baba", "main": "assets/skins/skin_baba.png", "anim": "assets/skins/skin_baba1.png"}
gena_skin = {"name": "Gena", "main": "assets/skins/Gena.png", "anim": "assets/skins/Gena1.png"}
larik_skin = {"name": "Larik", "main": "assets/skins/Larik.png", "anim": "assets/skins/Larik1.png"}
kalia_skin = {"name": "Kalia", "main": "assets/skins/Kalia.png", "anim": "assets/skins/Kalia1.png"}
mimi_ben_skin = {"name": "Mimi-Ben", "main": "assets/skins/mimi-ben.png", "anim": "assets/skins/mimi-ben1.png"}
jon_pro_skin = {"name": "Jon-Pro", "main": "assets/skins/jon-pro.png", "anim": "assets/skins/jon-pro1.png"}

all_skins = [penguin_skin, baba_skin, gena_skin, larik_skin, kalia_skin, mimi_ben_skin, jon_pro_skin]
unlocked_skins = []
active_skin = {"main": "assets/egg1.png", "anim": "assets/egg2.png"}
new_skin_popup = False
confirm_skin = None
show_confirm_popup = False
confirm_drop_skin = None

# --- Переменные
clicks = 0
show_info = False
show_inventory = False
current_inventory_page = 0
skins_per_page = 12
max_pages = 10

storm_rect = pygame.Rect(250, 20, 600, 50)
water_progress = 0
level = 1
button_rect = pygame.Rect(20, 20, 600, 600)  # невидимая кнопка для уровня 460,90,160,40

# --- Шанс выпадения
base_drop_chance = 0.0001  # начальный шанс 0.01%
max_drop_chance = 0.0200  # максимум 3%
clicks_since_last_drop = 0  # отслеживает клики между дропами
current_drop_chance = base_drop_chance  # начальный шанс выпадения

# --- Анимация тряски
shake_timer = 0
shake_duration = 15

running = True
clock = pygame.time.Clock()

while running:
    # --- Переменные для плавного увеличения и анимации иконок
    info_icon_scale = 1.0
    inventory_icon_scale = 1.0
    map_icon_scale = 1.0

    scale_speed = 0.05  # скорость изменения масштаба
    hover_scale = 1.15  # масштаб при наведении
    normal_scale = 1.0  # обычный масштаб

    screen.blit(background, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # Обработчик кликов
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # --- Воспроизведение фоновой музыки
        if not pygame.mixer.music.get_busy():  # Если музыка не играет
            current_track = (current_track + 1) % len(music_tracks)  # Переходим к следующему треку (по кругу)
            pygame.mixer.music.load(music_tracks[current_track])  # Загружаем новый трек
            pygame.mixer.music.play(+1,
                                    0.0)  # Запускаем его на повторе, +1 дальше трек по кругу, если -1 то повтор 1 трека!

            # Ваш основной игровой цикл:
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                show_info = not show_info

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            # Проверка на клик по кнопке уровня
            if not show_inventory and not show_map_shop and not new_skin_popup and not show_confirm_popup and not show_info and button_rect.collidepoint(
                    event.pos):  # Клик по кнопке, если инвентарь и карта не открыты

                if water_progress < 250:
                    water_progress += 1
                if water_progress >= 250:
                    water_progress = 0
                    level += 1

            # Получаем реальные скейлы кнопок
            info_scaled_rect = get_scaled_rect(info_icon_rect, info_icon_scale)
            inventory_scaled_rect = get_scaled_rect(inventory_icon_rect, inventory_icon_scale)
            map_scaled_rect = get_scaled_rect(map_icon_rect, map_icon_scale)

            # Обработка наведения мыши
            if info_scaled_rect.collidepoint(pos):
                info_icon_scale = min(hover_scale, info_icon_scale + scale_speed)
            else:
                info_icon_scale = max(normal_scale, info_icon_scale - scale_speed)

            if inventory_scaled_rect.collidepoint(pos):
                inventory_icon_scale = min(hover_scale, inventory_icon_scale + scale_speed)
            else:
                inventory_icon_scale = max(normal_scale, inventory_icon_scale - scale_speed)

            if map_scaled_rect.collidepoint(pos):
                map_icon_scale = min(hover_scale, map_icon_scale + scale_speed)
            else:
                map_icon_scale = max(normal_scale, map_icon_scale - scale_speed)

            # Обработка кликов по элементам интерфейса
            if info_scaled_rect.collidepoint(pos):
                show_info = not show_info
            elif inventory_scaled_rect.collidepoint(pos):  # Проверяем клик по иконке инвентаря
                if not show_inventory:
                    open_inventory_sound.play()  # Открытие инвентаря
                else:
                    close_inventory_sound.play()  # Закрытие инвентаря

                show_inventory = not show_inventory  # Переключаем состояние инвентаря
                inventory_icon_img = pygame.transform.scale(
                    inventory_icon_full if unlocked_skins else inventory_icon_empty, (150, 150))

            elif map_scaled_rect.collidepoint(pos):  # Проверка на клик по карте
                # Убрали звуковые эффекты на кнопке карты
                show_map_shop = not show_map_shop  # Переключаем отображение карты

            elif show_map_shop:
                # Если карта открыта, обрабатываем клики по элементам карты
                for idx, m in enumerate(map_images):
                    rect = pygame.Rect(200 + idx * 120, 440, 100, 100)
                    if rect.collidepoint(pos):
                        if idx in purchased_maps:
                            selected_map_index = idx
                            background = pygame.image.load(m["file"]).convert()
                            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                            multi_pop_sound.play()  # Воспроизведение звука при выборе карты
                            show_map_shop = False
                        elif clicks >= m["cost"]:
                            selected_map_index = idx
                            purchased_maps.append(idx)
                            background = pygame.image.load(m["file"]).convert()
                            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                            clicks -= m["cost"]
                            purchase_success_sound.play()  # Успешная покупка карты
                            show_map_shop = False
                        else:
                            purchase_fail_sound.play()  # Не хватает средств на карту

            elif new_skin_popup:
                # Добавим кнопку "Забрать" с координатами
                collect_btn_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 80, 150, 40)
                if collect_btn_rect.collidepoint(pos):
                    unlocked_skins.append(confirm_drop_skin)
                    new_skin_popup = False
                    confirm_drop_skin = None
                    purchase_success_sound.play()

            elif not show_inventory and not show_map_shop and not show_confirm_popup and not new_skin_popup:
                # Если инвентарь и карта не открыты, обрабатываем клики по скину
                egg_rect = pygame.image.load(active_skin["main"]).get_rect(center=egg_center)
                if egg_rect.collidepoint(pos):
                    clicks += 1
                    clicks_since_last_drop += 1

                    click_sound.play()

                    # Запускаем анимацию
                    egg_index = 1
                    shake_timer = shake_duration

                    # Обновляем шанс на выпадение
                    current_drop_chance = min(base_drop_chance + 0.00025 * clicks_since_last_drop, max_drop_chance)

                    # Пытаемся дропнуть скин
                    if clicks >= 20 and not new_skin_popup:
                        available_skins = [s for s in all_skins if s not in unlocked_skins and s != active_skin]
                        if available_skins and random.random() <= current_drop_chance:
                            confirm_drop_skin = random.choice(available_skins)
                            new_skin_popup = True
                            drop_sound.play()
                            clicks_since_last_drop = 0  # Сброс после дропа

            # Оставшиеся элементы, как показано выше

            elif show_inventory and not show_confirm_popup:
                for idx in range(skins_per_page):
                    real_idx = current_inventory_page * skins_per_page + idx
                    if real_idx < len(unlocked_skins):
                        col = idx % 3
                        row = idx // 3
                        rect = pygame.Rect(330 + col * 110, 210 + row * 110, 100, 100)
                        if rect.collidepoint(pos):
                            confirm_skin = unlocked_skins[real_idx]
                            show_confirm_popup = True
                for page in range(max_pages):
                    btn_rect = pygame.Rect(330 + page * 60, 600, 50, 30)
                    if btn_rect.collidepoint(pos) and page * skins_per_page < len(unlocked_skins):
                        current_inventory_page = page
            elif show_confirm_popup:
                yes_btn_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 40, 70, 40)
                no_btn_rect = pygame.Rect(WIDTH // 2 + 5, HEIGHT // 2 + 40, 70, 40)
                if yes_btn_rect.collidepoint(pos):
                    active_skin = confirm_skin  # Устанавливаем выбранный скин активным
                    show_confirm_popup = False
                    confirm_skin = None
                    click_sound.play()
                elif no_btn_rect.collidepoint(pos):
                    show_confirm_popup = False
                    confirm_skin = None
                    close_inventory_sound.play()

    if shake_timer > 0:
        shake_timer -= 1
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
    else:
        offset_x, offset_y = 0, 0
        egg_index = 0

    egg_img = pygame.image.load(active_skin["main" if egg_index == 0 else "anim"]).convert_alpha()  # отрисовка яйца
    egg_rect = egg_img.get_rect(center=(egg_center[0] + offset_x, egg_center[1] + offset_y))
    screen.blit(egg_img, egg_rect)


    # рисуем волну и уровень
    def blit_scaled(img, rect, scale):
        scaled_img = pygame.transform.smoothscale(img, (int(rect.width * scale), int(rect.height * scale)))
        new_rect = scaled_img.get_rect(center=rect.center)
        screen.blit(scaled_img, new_rect)


    # Отрисовка кнопок
    blit_scaled(info_icon_img, info_icon_rect, info_icon_scale)
    blit_scaled(inventory_icon_img, inventory_icon_rect, inventory_icon_scale)
    blit_scaled(map_icon_img, map_icon_rect, map_icon_scale)


    def get_scaled_rect(rect, scale):
        new_width = rect.width * scale
        new_height = rect.height * scale
        new_rect = pygame.Rect(0, 0, new_width, new_height)
        new_rect.center = rect.center
        return new_rect


    def draw_button(surface, rect, text):
        pygame.draw.rect(surface, (70, 130, 180), rect, border_radius=8)
        pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=8)
        label = font.render(text, True, (255, 255, 255))
        label_rect = label.get_rect(center=rect.center)
        surface.blit(label, label_rect)


    def draw_storm_wave(surface, rect, water_progress, level):
        wave_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        time = pygame.time.get_ticks() * 0.005

        # Рисуем волну с синим цветом
        for x in range(0, rect.width, 2):
            y = int(rect.height / 1.5 + 20 * math.sin(x * 100000 + time) + 10 * math.sin(x * 0.0100 + time * 0.9))
            r = max(0, min(255, int(150 + 100 * math.sin(time + x * 0.05))))
            g = max(0, min(255, int(100 + 20 * math.sin(time + x * 0.1 + 2))))
            b = 255
            pygame.draw.line(wave_surface, (r, g, b), (x, y), (x, rect.height))

        # Отображаем штормовую волну
        pygame.draw.rect(surface, (30, 30, 50), rect, border_radius=10)
        surface.blit(wave_surface, rect.topleft)

        # Прогресс волны
        fill_width = int((water_progress / 250) * rect.width)
        if fill_width > 0:
            water_surf = pygame.Surface((fill_width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(
                water_surf,
                (60, 130, 255, 120),
                (0, 0, fill_width, rect.height),
                border_top_left_radius=10,
                border_top_right_radius=10
            )
            surface.blit(water_surf, (rect.left, rect.top))
        if new_skin_popup and confirm_drop_skin:
            pygame.draw.rect(screen, (70, 130, 180), (WIDTH // 2 - 75, HEIGHT // 2 + 80, 150, 40), border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 2 - 75, HEIGHT // 2 + 80, 150, 40), 2, border_radius=8)
            label = font.render("Claim", True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100)))

        # Рисуем ячейку с уровнем
        cell_size = 30
        cell_rect = pygame.Rect(rect.left + 10, rect.top + 10, cell_size, cell_size)
        pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.002)
        yellow = (int(230 + 10 * pulse), int(200 + 20 * pulse), 50)
        pygame.draw.rect(surface, yellow, cell_rect, border_radius=5)

        # Отображаем уровень
        level_text = font.render(str(level), True, (20, 20, 20))
        level_text_rect = level_text.get_rect(center=cell_rect.center)
        surface.blit(level_text, level_text_rect)

        # Отображаем прогресс
        progress_text = big_font.render(f"{water_progress} / 250", True, (255, 255, 255))
        progress_rect = progress_text.get_rect(center=rect.center)
        surface.blit(progress_text, progress_rect)


    # Вызываем в основном игровом цикле:
    draw_storm_wave(screen, storm_rect, water_progress, level)

    counter_text = font.render(f"Clicks: {clicks}", True, (0, 0, 0))  # Валюта основная, не магазин.
    screen.blit(counter_text, (20, 20))

    if show_map_shop:
        pygame.draw.rect(screen, (255, 255, 255), (150, 410, 780, 250))
        pygame.draw.rect(screen, (0, 0, 0), (150, 410, 780, 250), 4)
        screen.blit(font.render("Select Map:", True, (0, 0, 0)), (WIDTH // 2 - 80, 420))
        for idx, m in enumerate(map_images):
            x = 200 + idx * 120
            img = pygame.image.load(m["file"]).convert()
            img = pygame.transform.scale(img, (64, 64))
            screen.blit(img, (x, 460))
            if idx in purchased_maps:  # Добавка для прорисовки названия (Куплено)
                cost_text = font.render("Owned", True, (0, 180, 0))
            else:
                cost_text = font.render(f"{m['cost']} Cl.", True, (0, 0, 0))  # Валюта магазина.
            screen.blit(cost_text, (x - 10, 530))

    if show_info:
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 280, 60, 240, 130))
        pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 280, 60, 240, 130), 2)
        screen.blit(small_font.render(f"Drop chance: {round(100 * current_drop_chance, 2)}%", True, (0, 0, 0)),
                    (WIDTH - 270, 70))
        screen.blit(small_font.render(f"Received: {len(unlocked_skins)}/{len(all_skins)}", True, (0, 0, 0)),
                    (WIDTH - 270, 100))

        screen.blit(small_font.render(f"Cards: {len(purchased_maps)}/{len(map_images)}", True, (0, 0, 0)),
                    (WIDTH - 270, 130))

    if new_skin_popup and confirm_drop_skin:
        pygame.draw.rect(screen, (255, 255, 255), (300, 150, 480, 400))
        pygame.draw.rect(screen, (0, 0, 0), (300, 150, 480, 400), 4)
        screen.blit(font.render("New Skin:", True, (0, 0, 0)), (440, 160))
        img = pygame.image.load(confirm_drop_skin["main"]).convert_alpha()
        screen.blit(pygame.transform.scale(img, (300, 300)), (390, 200))
        pygame.draw.rect(screen, (100, 200, 100), (440, 520, 200, 50))
        screen.blit(font.render("Claim", True, (255, 255, 255)), (500, 530))

    if show_inventory:
        # Фон и заголовок
        pygame.draw.rect(screen, (255, 255, 255), (300, 150, 480, 400))
        pygame.draw.rect(screen, (0, 0, 0), (300, 150, 480, 400), 4)
        screen.blit(font.render("Inventory:", True, (0, 0, 0)), (420, 160))

        inventory_start_x = WIDTH // 2 - (3 * 110 - 10) // 2  # центрируем 3 колонки
        total_rows = (len(unlocked_skins) + 2) // 3
        inventory_max_scroll = max(0, total_rows * 110 - 340)

        for idx, skin in enumerate(unlocked_skins):
            col = idx % 3
            row = idx // 3
            x = inventory_start_x + col * 110
            y = 210 + row * 110 - inventory_scroll_offset

            # Только если в зоне отображения
            if 150 < y + 100 < 550:
                rect = pygame.Rect(x, y, 100, 100)
                img = pygame.image.load(skin["main"]).convert_alpha()
                screen.blit(pygame.transform.scale(img, (100, 100)), rect.topleft)

                if pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
                    confirm_skin = skin
                    show_confirm_popup = True

        # Скроллбар
        if inventory_max_scroll > 0:
            scrollbar_height = max(40, 340 * 340 / (total_rows * 110))
            scrollbar_y = 210 + (inventory_scroll_offset / inventory_max_scroll) * (340 - scrollbar_height)
        else:
            scrollbar_height = 340
            scrollbar_y = 210

        pygame.draw.rect(screen, (200, 200, 200), (780, 210, 10, 340))
        pygame.draw.rect(screen, (80, 80, 255), (780, scrollbar_y, 10, scrollbar_height))

    if show_confirm_popup and confirm_skin:
        popup_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 100, 300, 200)
        pygame.draw.rect(screen, (70, 130, 180), popup_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), popup_rect, 3, border_radius=12)

        # Название скина
        label = font.render(f"Select Skin: {confirm_skin['name']}?", True, (255, 255, 255))
        screen.blit(label, (popup_rect.centerx - label.get_width() // 2, popup_rect.top + 30))

        # Кнопка "Да"
        yes_button = pygame.Rect(popup_rect.left + 40, popup_rect.bottom - 60, 80, 40)
        draw_button(screen, yes_button, "Yes")

        # Кнопка "Нет"
        no_button = pygame.Rect(popup_rect.right - 120, popup_rect.bottom - 60, 80, 40)
        draw_button(screen, no_button, "No")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
# 02.05.2025 /22:41 | @xg_code
# Duck, duck, kwa kwa! Когда жизнь не спрашивает, а утка просто квакнет!
