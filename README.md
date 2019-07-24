# flairdetectionproject




**The directory structure:**    
app.py() is the main python file that runs the web app.    
templates folder contains all the html files.   
static folder contains the images that have been uploaded on the website.   
My mchine learning model has been made using Flair Detection.ipynb    
My machine learning model is saved as model.joblib   
All the training data is in posts.bson and testing data is in train.bson. These are the mongodb dumps of my data.   

**Commands to run my project:**   
Visit the website at: https://flair-detector-oshhh.herokuapp.com/    
Enter the link to any Reddit post in the textbox and click submit to view the predicted and the actual flair of the post.


**The dependency libraries used:**     
flask   
praw   
nltk   
sklearn   
joblib   
gunicorn   
pandas   
numpy   

**The approach I followed:**   
In order to go through the approach I followed, please visit : https://flair-detector-oshhh.herokuapp.com/modelv2   
