import os
import json
import requests
from io import BytesIO
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def link_genshin_art(name):
    return f'https://enka.network/ui/UI_Gacha_AvatarImg_{name}.png'

def link_genshin_icon(name):
    return f'https://enka.network/ui/UI_AvatarIcon_{name}.png'

def link_starrail_art(id):
    return f'https://enka.network/ui/hsr/SpriteOutput/AvatarDrawCard/{id}.png'

def link_starrail_icon(id):
    return f'https://raw.githubusercontent.com/FortOfFans/HSR/main/spriteoutput/avatarshopicon/{id}.png'

# -------------------------------------------------------------------------------------------------
# Version Check
# -------------------------------------------------------------------------------------------------
def version_check():
    return_data = []
    url = 'https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?launcher_id=VYTpXlbWo8'
    response = requests.get(url)
    data = response.json().get('data').get('game_packages')

    for games in data:
        game = games.get('game')
        game_name = game.get('biz')

        main = games.get('main').get('major')
        game_version = main.get('version')

        if game_name != 'hk4e_global' and game_name != 'hkrpg_global':
            continue
        else:
            return_data.append({ game_name: game_version })
    
    return return_data

def update():
    latest_versions = version_check()
    
    try:
        with open('version.json', 'r') as file:
            current_versions = json.load(file)
    except FileNotFoundError:
        current_versions = {}
    except json.JSONDecodeError:
        print("Error decoding JSON file.")
        current_versions = {}
    
    latest_versions_dict = {list(version.keys())[0]: list(version.values())[0] for version in latest_versions}

    for game, new_version in latest_versions_dict.items():
        current_version = current_versions.get(game)
        if current_version != new_version:            
            if game == 'hk4e_global':
                update_genshin()
            elif game == 'hkrpg_global':
                update_starrail()

            current_versions[game] = new_version
    
    with open('version.json', 'w') as file:
        json.dump(current_versions, file, indent=4)

# -------------------------------------------------------------------------------------------------
# GENSHIN IMPACT
# -------------------------------------------------------------------------------------------------
def update_genshin():
    with open('gi_characters.json', 'r') as file:
        data = json.load(file)

    progress_bar = tqdm(total=len(data), desc="Updating Genshin Impact characters", unit="character")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    def process_character(id_str, name):
        genshin_icon_art(current_dir, name, id_str)
        genshin_splash_art(current_dir, name, id_str)
        genshin_wish_art(current_dir, name, id_str)
        return id_str

    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(process_character, id_str, name) for id_str, name in data.items()]
        
        for future in as_completed(futures):
            future.result()
            progress_bar.update(1)

    progress_bar.close()
    print(f"Finished updating {len(data)} Genshin Impact characters")

def genshin_icon_art(current_dir, character, id):
    try:
        response = requests.get(link_genshin_icon(character))
        character_icon = Image.open(BytesIO(response.content))

        text_files_dir = os.path.join(current_dir, "genshin", "icon")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        character_icon.save(output_path)
    except Exception as e:
        print(f"Failed to create icon art for {character}: {str(e)}")

def genshin_splash_art(current_dir, character, id):
    try:
        response = requests.get(link_genshin_art(character))
        character_art = Image.open(BytesIO(response.content))

        text_files_dir = os.path.join(current_dir, "genshin", "splash")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        character_art.save(output_path)
    except Exception as e:
        print(f"Failed to create splash art for {character}: {str(e)}")

def genshin_wish_art(current_dir, character, id):
    try:
        response = requests.get(link_genshin_art(character))
        character_image = Image.open(BytesIO(response.content))

        new_width = character_image.height * 0.3125 # 5:16 ratio

        left = (character_image.width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = character_image.height

        cropped_image = character_image.crop((left, top, right, bottom))

        text_files_dir = os.path.join(current_dir, "genshin", "wish")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        cropped_image.save(output_path)
    except Exception as e:
        print(f"Failed to create wish art for {character}: {str(e)}")

# -------------------------------------------------------------------------------------------------
# HONKAI: STAR RAIL
# -------------------------------------------------------------------------------------------------
def update_starrail():
    with open('hsr_characters.json', 'r') as file:
        data = json.load(file)

    progress_bar = tqdm(total=len(data), desc="Updating Star Rail characters", unit="character")
    current_dir = os.path.dirname(os.path.abspath(__file__))

    def process_character(id_str, name):
        starrail_icon_art(current_dir, name, id_str)
        starrail_splash_art(current_dir, name, id_str)
        starrail_wish_art(current_dir, name, id_str)
        return id_str

    with ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(process_character, id_str, name) for id_str, name in data.items()]

        for future in as_completed(futures):
            future.result()
            progress_bar.update(1)

    progress_bar.close()
    print(f"Finished updating {len(data)} Star Rail characters")

def starrail_icon_art(current_dir, character, id):
    try:
        response = requests.get(link_starrail_icon(id))
        character_icon = Image.open(BytesIO(response.content))

        text_files_dir = os.path.join(current_dir, "starrail", "icon")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        character_icon.save(output_path)
    except Exception as e:
        print(f"Failed to create icon art for {character}: {str(e)}")

def starrail_splash_art(current_dir, character, id):
    try:
        response = requests.get(link_starrail_art(id))
        character_art = Image.open(BytesIO(response.content))

        text_files_dir = os.path.join(current_dir, "starrail", "splash")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        character_art.save(output_path)
    except Exception as e:
        print(f"Failed to create splash art for {character}: {str(e)}")

def starrail_wish_art(current_dir, character, id):
    try:
        response = requests.get(link_starrail_art(id))
        character_image = Image.open(BytesIO(response.content))

        new_width = character_image.height * 0.3125 # 5:16 ratio

        left = (character_image.width - new_width) // 2
        top = 0
        right = left + new_width
        bottom = character_image.height

        cropped_image = character_image.crop((left, top, right, bottom))

        text_files_dir = os.path.join(current_dir, "starrail", "wish")
        os.makedirs(text_files_dir, exist_ok=True)

        output_path = os.path.join(text_files_dir, f'{id}.png')
        cropped_image.save(output_path)
    except Exception as e:
        print(f"Failed to create wish art for {character}: {str(e)}")