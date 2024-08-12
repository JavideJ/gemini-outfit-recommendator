from vertexai.preview.generative_models import GenerativeModel
import utils
import ast

def gemini_outfit(img_url, folder_path):
    """
    Given an item of clothing you want to buy, Gemini recommends an outfit with your own clothes.
    
    Parameters:
    - img_url: str with a url to a website with a png or jpg image of clothing
    - folder_path: str with the path to the images of your own clothes. This folder has to be organised into shirts, shoes, trousers or tshirts folders.
    """
    
    multimodal_model = GenerativeModel("gemini-pro-vision")
    img_shop = utils.load_image_from_url(img_url)

    contents = [
        'Which category does this garment belong to? Say which one it most closely resembles: shirts, shoes, trousers, tshirts. Add the order in which you would choose the rest of the garments to create an outfit.\
        The format of the response will be like a python dictionary. For example: {0: "shirts", 1: "shoes", 2: "trousers", 3: "tshirts"}. The 0 will be the garment in the image.',
        img_shop,
        ]

    print("-------Prompt--------")
    utils.print_multimodal_prompt(contents)

    responses = multimodal_model.generate_content(contents, stream=True)
    print("\n-------Response--------")
    response_str = str()
    for response in responses:
        response_str += response.text
        print(response.text, end="")

    # Clean the str and convert it to dict
    response_str = response_str.strip().strip('```python\n```')
    clothes_order = ast.literal_eval(response_str)
    outfit_dict = {clothes_order[0]:img_shop}
    #########################################################################################################################################################################
    contents = ['I want to wear this garment:', img_shop]
    outfit_path_dict = dict()

    for i in range(1, len(clothes_order.keys())):
        contents.append('With which of the following does it suit me best?')
        # Load images of next clothes
        # Load images of next clothes
        next_clothes = clothes_order[i]
        local_path = f'{folder_path}/{next_clothes}'
        filenames_list = utils.get_file_names_from_path(local_path)
        clothes_images = [utils.load_image_from_path(local_path+'/'+filename) for filename in filenames_list]

        for filename, img in zip(filenames_list, clothes_images):
            contents.append(filename)
            contents.append(img)

        contents.append(f'Answer with a string separating by commas the models that fit. For example: {",".join(filenames_list[:2])}')

        # print("\n-------Prompt--------")
        # utils.print_multimodal_prompt(contents)

        responses = multimodal_model.generate_content(contents, stream=True)
        print("\n-------Response--------")
        response_str_2 = str()
        for response in responses:
            response_str_2 += response.text
            print(response.text, end="")

        chosen_list = response_str_2.strip().split(',')

        # Clean the contents
        content_to_remove = (len(clothes_images)*2)+2
        contents = contents[:-content_to_remove]

        # Add the new chosen clothe
        contents.append('Together with this one:')
        full_path = local_path+'/'+chosen_list[0]
        outfit_path_dict[next_clothes] = full_path
        chosen_clothe = utils.load_image_from_path(full_path)
        contents.append(chosen_clothe)
        outfit_dict[next_clothes] = chosen_clothe
    #########################################################################################################################################################################
    # Review if the tshirt and shirt are ok or choose just one
    content_review = ["We have chosen an outfit composed by some shoes, trousers, tshirt and shirt:",
                     'shirt:', outfit_dict['shirts'],
                     'tshirt:', outfit_dict['tshirts'],
                     'trouser:', outfit_dict['trousers'],
                     'shoe:', outfit_dict['shoes'],
                     "Check if the shirt and the t-shirt look good together or if only one of them looks better.\
    Respond 'tshirts' if just the tshirt looks better, 'shirts' if just the shirt looks better or 'both' if both at the same time are ok."]

    # print("\n-------Prompt--------")
    # utils.print_multimodal_prompt(content_review)

    responses = multimodal_model.generate_content(content_review, stream=True)
    print("\n-------Response--------")
    response_str_3 = str()
    for response in responses:
        response_str_3 += response.text
        print(response.text, end="")

    # Reorder dict and delete clothes in case Gemini does not like it
    custom_order = ['shirts', 'tshirts', 'trousers', 'shoes']
    outfit_dict = {key: outfit_dict[key] for key in custom_order}
    outfit_path_dict = {k: outfit_path_dict[k] for k in custom_order if k != clothes_order[0]}

    if response_str_3=='tshirts':
        value = outfit_dict.pop('shirts')
        value = outfit_path_dict.pop('shirts')
    elif response_str_3=='shirts':
        value = outfit_dict.pop('tshirts')
        value = outfit_path_dict.pop('tshirts')

    print('\nThe recommended outfit is as follows:')
    utils.print_multimodal_prompt(outfit_dict.values())

    return outfit_path_dict
    