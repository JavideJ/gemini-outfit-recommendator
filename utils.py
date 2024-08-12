from vertexai.preview.generative_models import Image
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps
import IPython.display
import io
import typing
import urllib.request
import http.client
import os
import json

def image_to_bytes(image_path: str) -> bytes:
    # Abrir la imagen usando PIL
    img = PIL_Image.open(image_path)

    # Convertir la imagen a bytes
    with io.BytesIO() as output:
        img.save(output, format=img.format)
        image_bytes = output.getvalue()

    return image_bytes


def load_image_from_url(image_url: str) -> Image:
    image_bytes = get_image_bytes_from_url(image_url)
    return Image.from_bytes(image_bytes)


def get_image_bytes_from_url(image_url: str) -> bytes:
    with urllib.request.urlopen(image_url) as response:
        response = typing.cast(http.client.HTTPResponse, response)
        if response.headers["Content-Type"] not in ("image/png", "image/jpeg"):
            raise Exception("Image can only be in PNG or JPEG format")
        image_bytes = response.read()
    return image_bytes


def load_image_from_path(image_path: str) -> Image:
    image_bytes = image_to_bytes(image_path)
    return Image.from_bytes(image_bytes)


def display_image(image: Image,
                  max_width: int = 600,
                  max_height: int = 350) -> None:
    pil_image = typing.cast(PIL_Image.Image, image._pil_image)
    if pil_image.mode != "RGB":
        # Modes such as RGBA are not yet supported by all Jupyter environments
        pil_image = pil_image.convert("RGB")
    image_width, image_height = pil_image.size
    if max_width < image_width or max_height < image_height:
        # Resize to display a smaller notebook image
        pil_image = PIL_ImageOps.contain(pil_image, (max_width, max_height))
    display_image_compressed(pil_image)


def display_image_compressed(pil_image: PIL_Image.Image) -> None:
    image_io = io.BytesIO()
    pil_image.save(image_io, "jpeg", quality=80, optimize=True)
    image_bytes = image_io.getvalue()
    ipython_image = IPython.display.Image(image_bytes)
    IPython.display.display(ipython_image)
    
    
def print_multimodal_prompt(contents: list):
    """
    Given contents that would be sent to Gemini,
    output the full multimodal prompt for ease of readability.
    """
    for content in contents:
        if isinstance(content, Image):
            display_image(content)
        else:
            print(content)

            
def image_to_bytes(image_path: str) -> bytes:
    # Abrir la imagen usando PIL
    img = PIL_Image.open(image_path)

    # Convertir la imagen a bytes
    with io.BytesIO() as output:
        img.save(output, format=img.format)
        image_bytes = output.getvalue()

    return image_bytes


def load_image_from_path(image_path: str) -> Image:
    image_bytes = image_to_bytes(image_path)
    return Image.from_bytes(image_bytes)


def get_file_names_from_path(path):
    ext = ('.jpg', '.jpeg', '.png')
    filenames = [name for name in os.listdir(path) if name.lower().endswith(ext)]
    return filenames
            
            
def ask_gemini(img_url, prompt, multimodal_model):
    """
    Provide an image url of some clothes and a prompt to get the outfit reccommendation.
    
    Parameters:
    - img_url: str with the link
    - prompt: str with the query
    - multimodal_model: vertexai.preview.generative_models.GenerativeModel
    """
    # urls for room images
    room_image_url = f"{img_url}"

    # load room images as Image Objects
    room_image = load_image_from_url(room_image_url)

    prompt = f"{prompt}"
    contents = [
        prompt,
        room_image,
    ]

    responses = multimodal_model.generate_content(contents, stream=True)

    print("-------Prompt--------")
    print_multimodal_prompt(contents)

    print("\n-------Response--------")
    for response in responses:
        print(response.text, end="")


def order_dict(outfit_path_dict, user_image_path):
    """
    Returns the clothing dict in the proper order to be printed.
    
    Parameters:
    - outfit_path_dict: dict with the kind of clothing item and its path to the image
    - user_image_path: str with the link to the image of the purchasing item
    """
    
    clothing_types_order = ['shirts', 'tshirts', 'trousers', 'shoes']
    # Get the type of clothe of the item to buy
    clothing_img_type = list(set(clothing_types_order)-set(outfit_path_dict.keys()))[0]
    outfit_path_dict[clothing_img_type] = user_image_path
    
    # Create a new ordered dict
    clothing_dic_ordered = {}
    
    for key in list(clothing_types_order):
        if key in outfit_path_dict:
            clothing_dic_ordered[key] = outfit_path_dict[key]
    return clothing_dic_ordered


def import_json(filename):
    """
    Import a json file.
    
    Parameters:
    - filename: str path to file
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)  # Carga el JSON directamente en un diccionario

    return data
    