from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import math

# Initialize Perlin noise
noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))

# Create an instance of the Ursina app
if not application.base:
    app = Ursina()

# Define game variables
selected_block = "grass"

# Load block textures
block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png")
}

# Define Block class
class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model="assets/models/block_model",  # Use your block model
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(block_type),
            collider="box",
            backface_culling=True # Enable backface culling here
        )
        self.block_type = block_type

# Function to create the world
def create_world(min_height=-5, size=20):
    blocks = [] #keep track of the blocks
    for x in range(-size, size):
        for z in range(-size, size):
            height = noise([x * .02, z * .02])
            height = math.floor(height * 7.5)
            for y in range(height, min_height - 1, -1):
                if y == min_height:
                    block = Block((x, y + min_height, z), "bedrock")
                elif y == height:
                    block = Block((x, y + min_height, z), "grass")
                elif height - y > 2:
                    block = Block((x, y + min_height, z), "stone")
                else:
                    block = Block((x, y + min_height, z), "dirt")
                blocks.append(block) # Add the block to the list
    return blocks # return the list of blocks.

if __name__ == "__main__":
    app = Ursina()
    create_world()
    app.run()
