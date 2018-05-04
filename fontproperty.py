from PIL import ImageFont, Image
import json
import numpy

class Fontproperty:

    def __init__(self, simplifychinese, traditionchinese,english,symbol):
        with open(simplifychinese, 'r') as f:
            self.simplifychinese = json.load(f)
        
        with open(traditionchinese, 'r') as f:
            self.traditionchinese = json.load(f)

        with open(english, 'r') as f:
            self.english = json.load(f)

        with open(symbol, 'r') as f:
            self.symbol = json.load(f)


    def __call__(self, text, font_size):
        pass

    def choose_font(self, text):
        pass