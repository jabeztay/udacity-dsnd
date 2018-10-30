import sys
import pandas as pd
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pickle


def load_data(database_filepath):
    '''
    Loads an sqlite database and returns X(features), Y(labels) and
    label names.
    '''
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql('messages', engine)
    X = df.iloc[:, 1].values
    Y = df.iloc[:, 4:].values
    category_names = df.columns[4:]
    return X, Y, category_names


def tokenize(text):
    '''
    Tokenizer function for CountVectorizer
    '''
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(token).lower().strip()
                    for token in tokens]
    return clean_tokens

def build_model():
    '''
    Returns a model pipeline
    '''
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(
            RandomForestClassifier(random_state=42)))
    ])

    param_grid = {
        'vect__ngram_range': [(1, 1), (1, 2)],
        'clf__estimator__n_estimators': [10, 50, 100]
    }

    cv = GridSearchCV(pipeline, param_grid=param_grid)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    Evaluates model, returning output accuracy, precision and recall
    for each category
    '''
    Y_pred = model.predict(X_test)
    for i in range(36):
        print('category: {}'.format(category_names[i]))
        print(classification_report(Y_test[:, i], Y_pred[:, i]))


def save_model(model, model_filepath):
    '''
    Saves model to a pickle file
    '''
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()