# Movie genre predictions
> Regression model that can predict a movie genres based on the plot

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Usage](#usage)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
This is a Flask based application for a trained regression model that can predict movie genres based on the plot.
The application is deployed using Heroku.

train_model.py file contains the code for training and saving the model.

database.py file contains code for creating required database.

app.py file contains the Flask API.
## Technologies
Project is created with:
* Python 3.9.0
* Flask 1.1.2
* Heroku

## Usage
The link to the application for predictions:

https://predict-movie-genres.herokuapp.com/predict

You can also see the top 10 most recent predictions:

https://predict-movie-genres.herokuapp.com/recent

Code Example:
```
requests.post("https://predict-movie-genres.herokuapp.com/predict", data=json.dumps({
    "input": [
         "A comedy centered on the life of Kate Reddy, a finance executive who is the breadwinner for her husband and two kids.", 
        "An American showgirl becomes entangled in political intrigue when the Prince Regent of a foreign country attempts to seduce her."
    ]
}))
```

## Status
Project is: _finished_

## Inspiration
Project created as a task for DS.2.4 project.

## Contact
Created by Dovilė Žaltauskaitė [@dovilez] 
