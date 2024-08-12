## gemini-outfit-recommendator
_Buy what you like, match it with your own clothes_

# Description
The Gemini Outfit Recommender (GOR) offers an innovative online tool designed for clothing retailers. Simply choose an item you’re interested in, and Gemini will provide you with a stylish outfit that complements your new purchase with your existing wardrobe.

This user-friendly app enhances the shopping experience by helping customers make more informed decisions, boosting their confidence, and reducing the likelihood of returns. Future updates will introduce features allowing users to interact with Gemini in real-time to refine outfits or manually select different clothing items.

Powered by the Gemini Pro Vision model, this app is able to analyse images and deliver insightful recommendations.  Due to the current model´s limit of processing 16 images, it iterates over various type of clothing (such as shirts Tshirts, trousers, and shoes) and multiple pictures of each type in each iteration, selecting the most suitable items for the outfit.

# How to use it
Make sure you have python (version 3.11.7 was used for this project) and pip installed.<br>
1) Once you have downloaded all the files, **open the terminal in the same location as app.py**

2) **Install depencies**. In your terminal, run:<br>
```pip install -r requirements.txt```

4) **Run app.py** In your terminal, run:<br>
```python app.py```

# Try with your own clothes!
If you want to create outfits with pictures of your own clothes, upload png or jpg files to "static/my_closet".<br>
Take into account that the app is prepared to give you an outfit composed by 4 items (shirt, Tshirt, trousers and shoes).<br>
Also, you can change the "static/imagen1.jpg" file to the clothing item you would like to buy.
<br><br><br>
You can contact me on my [Linkedin](https://www.linkedin.com/in/javier-de-juan-portela/?locale=en_US)<br>
Check the demo video [YouTube](https://www.youtube.com/watch?v=4fN7KtNrWFw)
