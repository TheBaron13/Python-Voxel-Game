from ursina import Ursina, Entity, camera, raycast, destroy, Vec2, window, mouse # Import mouse
from ursina.prefabs.first_person_controller import FirstPersonController
from world_generation import create_world, block_textures, Block

# Create an instance of the Ursina app
app = Ursina()

# Window controls
window.title = 'My Game'           # The window title
window.borderless = False         # Show a border
window.fullscreen = False         # Do not go Fullscreen
window.exit_button.visible = False    # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True      # Show the FPS (Frames per second) counter
window.exit_button.visible = True
window.resolution = (720, 480)         # Set the window resolution

# Define game variables
selected_block = "grass"

# Create player
player = FirstPersonController(mouse_sensitivity=Vec2(100, 100), position=(0, 5, 0))

# Create mini block for player inventory
mini_block = Entity(
    parent=camera,
    model="assets/models/block_model",
    texture=block_textures.get(selected_block),
    scale=0.2,
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)

# Create world
blocks = create_world() # Store the returned blocks

# Define input function for placing and breaking blocks
def input(key):
    global selected_block
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block)
            blocks.append(block) # Add new block to the list
    if key == 'right mouse down' and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)
            blocks.remove(mouse.hovered_entity) # Remove destroyed block from list
    if key == '1':
        selected_block = "grass"
    if key == '2':
        selected_block = "dirt"
    if key == '3':
        selected_block = "stone"

# Update mini block texture
def update():
    mini_block.texture = block_textures.get(selected_block)

# Run the app
app.run()
