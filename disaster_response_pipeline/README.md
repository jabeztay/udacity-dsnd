# Disaster Response Pipeline Project

### Summary

During disaster events, many messages are sent out requesting for help. We implement a model to categorise messages based on their content, in order to highlight messages to the appropriate disaster relief agencies.

### Files

- data/process_data.py: ETL pipeline used to clean and process data
- models/train_classifier.py: ML pipeline used to implement a model for message classification
- app/run.py: Flask webapp which uses the trained model to classify messages

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/