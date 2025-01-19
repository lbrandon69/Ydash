import json
import os

def load_coins():
    try:
        with open("data/json/coins.json", "r") as file:
            data = json.load(file)
            return data.get("coins", 0)
    except FileNotFoundError:
        return 0

def save_coins(coins):
    with open("data/json/coins.json", "w") as file:
        json.dump({"coins": coins}, file)

def load_skins():
    try:
        with open("data/json/skins.json", "r") as file:
            data = json.load(file)
            return data.get("skins", [])
    except FileNotFoundError:
        return []

def save_skins(skin):
    skins = load_skins()
    if skin not in skins:
        skins.append(skin)
    with open("data/json/skins.json", "w") as file:
        json.dump({"skins": skins}, file)

def load_selected_skin():
    try:
        with open("data/json/selected_skin.json", "r") as file:
            data = json.load(file)
            return os.path.join("./data/img/Players", data.get("selected_skin", "skin_01.png"))
    except FileNotFoundError:
        return os.path.join("./data/img/Players", "skin_01.png")

def save_selected_skin(skin):
    with open("data/json/selected_skin.json", "w") as file:
        json.dump({"selected_skin": skin}, file)


def select_skin_menu():
    running = True
    owned_skins = load_skins()
    selected_skin = load_selected_skin()
    skin_index = owned_skins.index(selected_skin) if selected_skin in owned_skins else 0

    while running:
        screen.fill(BLACK)
        draw_text("Select Your Skin", font, WHITE, screen, SCREEN_WIDTH // 2, 100)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]

        skin_image = pygame.image.load(os.path.join("./data/img/Players", owned_skins[skin_index])).convert_alpha()
        skin_image = pygame.transform.scale(skin_image, (100, 100))
        screen.blit(skin_image, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50))

        button_prev = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 50, 50)
        button_next = pygame.Rect(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2, 50, 50)
        button_select = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 50)

        if draw_button(screen, "<", button_prev, GRAY, BLUE, font, mouse_pos, mouse_click):
            skin_index = (skin_index - 1) % len(owned_skins)
        if draw_button(screen, ">", button_next, GRAY, BLUE, font, mouse_pos, mouse_click):
            skin_index = (skin_index + 1) % len(owned_skins)
        if draw_button(screen, "Select", button_select, GRAY, BLUE, font, mouse_pos, mouse_click):
            selected_skin = owned_skins[skin_index]
            save_selected_skin(selected_skin)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False