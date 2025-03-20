# Pokefun.gg Gradio App created by Cassy Miller

# Import Dependencies

import gradio as gr
import pokefun.gg_module.py

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