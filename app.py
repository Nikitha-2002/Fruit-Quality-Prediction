from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


import os, sys, glob, re

app = Flask(__name__)

model_path = "FruitNet.h5"



classes = {0:"Low_quality_Apple:-{ Rice,Wheat,Sugarcane,Maize,Cotton,Soyabean,Jute }",1:"Low_quality_mango:-{ Virginia, Wheat , Jowar,Millets,Linseed,Castor,Sunflower} ",2:"Quality_Apples:-{ Rice,Lettuce,Chard,Broccoli,Cabbage,Snap Beans }",3:"Quality_Mangoes:{ Cotton,Wheat,Pilses,Millets,OilSeeds,Potatoes }"}

def model_predict(image_path):
    print("Predicted")
    image = load_img(image_path,target_size=(150,150))
    image = img_to_array(image)
    image = image/255
    image = np.expand_dims(image,axis=0)
    model = load_model(model_path)
    result = np.argmax(model.predict(image))
    prediction = classes[result]
    
    
    if result == 0:
        print("Alluvial.html")
        
        return "Low_quality_Apple","LowqualityApple.html"
    elif result == 1:
        print("Black.html")
        
        return "Low_quality_mango", "Lowqualitymango.html"
    elif result == 2:
        print("Clay.html")
        
        return "Quality_Apples" , "QualityApples.html"
    elif result == 3:
        print("Red.html")
        
        return "Quality_Mangoes" , "QualityMangoes.html"
    


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')



@app.route('/predict',methods=['GET','POST'])
def predict():
    print("Entered")
    if request.method == 'POST':
        print("Entered here")
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)

        print("@@ Predicting class......")
        pred, output_page = model_predict(file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    


if __name__ == '__main__':
    app.run(debug=True,threaded=False)
    
