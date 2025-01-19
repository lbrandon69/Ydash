import json
import os

def load_coins():
    """
    Charge le nombre de pièces sauvegardées à partir du fichier JSON.

    Returns:
    - int: Le nombre de pièces disponibles. Retourne 0 si le fichier n'existe pas.
    """
    try:
        with open("data/json/coins.json", "r") as file:
            data = json.load(file)
            return data.get("coins", 0)
    except FileNotFoundError:
        return 0

def save_coins(coins):
    """
    Sauvegarde le nombre de pièces dans le fichier JSON.

    Args:
    - coins (int): Le nombre de pièces à sauvegarder.
    """
    directory = "data/json"
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(os.path.join(directory, "coins.json"), "w") as file:
            json.dump({"coins": coins}, file)
    except PermissionError:
        print("Erreur : permission refusée pour écrire dans le fichier coins.json.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

def load_skins():
    """
    Charge la liste des skins possédés à partir du fichier JSON.

    Returns:
    - list: Liste des skins possédés. Retourne une liste vide si le fichier n'existe pas.
    """
    try:
        with open("data/json/skins.json", "r") as file:
            data = json.load(file)
            return data.get("skins", [])
    except FileNotFoundError:
        return []

def save_skins(skin):
    """
    Sauvegarde un skin ajouté dans la liste des skins possédés.

    Args:
    - skin (str): Le nom du skin à ajouter à la liste des skins possédés.
    """
    skins = load_skins()
    if skin not in skins:
        skins.append(skin)
    with open("data/json/skins.json", "w") as file:
        json.dump({"skins": skins}, file)

def load_selected_skin():
    """
    Charge le skin sélectionné à partir du fichier JSON.

    Returns:
    - str: Le chemin du fichier image du skin sélectionné. Retourne le skin par défaut si le fichier n'existe pas.
    """
    try:
        with open("data/json/selected_skin.json", "r") as file:
            data = json.load(file)
            return os.path.join("./data/img/Players", data.get("selected_skin", "skin_01.png"))
    except FileNotFoundError:
        return os.path.join("./data/img/Players", "skin_01.png")

def save_selected_skin(skin):
    """
    Sauvegarde le skin sélectionné dans le fichier JSON.

    Args:
    - skin (str): Le nom du skin sélectionné à sauvegarder.
    """
    with open("data/json/selected_skin.json", "w") as file:
        json.dump({"selected_skin": skin}, file)


def select_skin_menu():
    """
    Affiche le menu de sélection de skin, permettant de choisir parmi les skins possédés.
    """
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