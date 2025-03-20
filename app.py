# Pokefun.gg Gradio App created by Cassy Miller

# Import Dependencies

import gradio as gr
import requests
import random
from PIL import Image
from io import BytesIO

# Function to fetch Poke data
def get_poke_data(poke_name):
    """
    Fetches poke data from the PokeAPI using the poke name.

    Args:
        poke_name(str): Name of the poke to fetch.
    Returns:
        dict or None: poke data if found otherwise none  
    """

    if not poke_name:
        print("Poke not found.")
        return
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to fetch species data (for catch rate, gender rate, and variants)
def get_species_data(poke_name):
    """
    Fetches species data for a poke from the PokeAPI using the poke name.

    Args:
        poke_name(str): Name of the poke to fetch species data for.

    Returns:
        dict or None: poke species data if found otherwise none.
    """
    if not poke_name:
        return
    url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
# Function to fetch Poke picture
def get_poke_pic(poke_data):
    """
    Fetches and resizes a poke sprite.

    Args:
        poke_data(dict): Dict containing poke data including the sprite url.
    
    Returns:
        PIL.img or None: resized sprite img if avail, otherwise none.
    """

    if not poke_data:
        return None

    # Get the sprite URL
    sprite_url = poke_data['sprites']['front_default']
    if not sprite_url:
        return None

    # Fetch the image from the URL
    response = requests.get(sprite_url)
    if response.status_code == 200:
        # Resizing img
        try:
            img = Image.open(BytesIO(response.content))
            img = img.resize((365,365))
            return img
        except Exception as e:
            print(f"Error opening image: {e}")
            return None
    else:
        return None

#Function to get a random poke
def get_random_poke():
    """
    Fetches a random poke by generating its random ID between 1-1025 and returning the poke name.

    Returns: 
        str or None: Name or random poke
    """
    random_id = random.randint(1, 1025)  # 1025 pokes
    poke_data = get_poke_data(random_id) 
    if poke_data:
        return poke_data['name']
    else:
        return None
    
# Function for compiling and displaying the pokemon info
def display_poke_info(poke_name):
    """
    Gathers and compiles basic poke info based on the poke name.
    
    Args: 
        poke_name(str): name of poke to gather poke and species data with.
    
    Returns:
        info(str): the compiled poke info prepped for printing inside gradio app.
    """

    if not poke_name:
        return "Poke not found!"
    
    poke_data = get_poke_data(poke_name)
    species_data = get_species_data(poke_name)
    
    # Gather name and stats and store as a variable
    info = f"Name: {poke_data['name'].capitalize()} \n"
    info += "Type(s): " + " | ".join([t['type']['name'].capitalize() for t in poke_data['types']]) + "\n"
    
    # Abilities info, with seperation for regular and hidden abilities.
    reg_ab = []
    hid_ab = []
    for ability in poke_data['abilities']:
        if ability['is_hidden']:
            hid_ab.append(ability['ability']['name'].capitalize())
        else:
            reg_ab.append(ability['ability']['name'].capitalize())
    info += "Abilities: " + " | ".join(reg_ab) + "\n"
    if hid_ab:
        info += "Hidden Ability: " + " | ".join(hid_ab) + "\n" 

    #Gen info
    generation_url = species_data['generation']['url']
    generation_name = generation_url.split("/")[-2].replace("-", " ").title()
    info += f"Generation: {generation_name}\n"

    # Add height and weight
    info += f"Height: {poke_data['height'] / 10} meters | Weight: {poke_data['weight'] / 10} kg\n"

    # Add stats
    info += "Base Stats:\n"
    for stat in poke_data['stats']:
        info += f"  {stat['stat']['name'].capitalize()}: {stat['base_stat']}\n"


    return info

# Function to handle Gradio app logic
def pokefun(poke_name):
    """
    Function for use within gradio app. 

    Args:
        poke_name(str): the poke name.
    
    Returns:
        info(str): the poke info as described in the display_poke_info() func
        img(PIL.img): the poke sprite as described in the get_poke_pic() func
    """
    # Get Pokémon info
    info = display_poke_info(poke_name)

    # Get Pokémon picture
    poke_data = get_poke_data(poke_name)
    img = get_poke_pic(poke_data)
    if not img:
        return info, None

    return info, img


# Create Gradio app with info and image
with gr.Blocks() as demo:
    gr.Markdown("# Welcome to Pokefun.gg (demo)")
    gr.Markdown("Enter the name of a Poke to see its info and sprite!")
    
    # Input section
    with gr.Row():
        pokemon_name_or_id = gr.Textbox(label ="Enter Poke name.", placeholder = "ex. Umbreon")
        with gr.Column():
            submit_button = gr.Button("go!")
            random_button = gr.Button("Random Poke")

    # Output section with info and image side by side
    with gr.Row():  
        info_output = gr.Textbox(label="Poke Info", lines=15)
        image_output = gr.Image(label="Poke Sprite")

    # Connect the buttons to the functions
    submit_button.click(
        fn=pokefun,
        inputs=pokemon_name_or_id,
        outputs=[info_output, image_output]
    )
    random_button.click(
        fn=lambda: pokefun(get_random_poke()),
        inputs=[],
        outputs=[info_output, image_output]
    )

# Launch the app
demo.launch()