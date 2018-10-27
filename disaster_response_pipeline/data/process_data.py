import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    '''
    Takes two csv files (messages and categories) and returns a merged
    dataframe
    '''
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = pd.merge(messages, categories, how='inner', on='id')
    return df


def clean_data(df):
    '''
    Takes a dataframe made by load_data, then cleans and returns it
    '''
    # create individual columns for each category
    categories = df['categories'].str.split(';', expand=True)
    # get names for each category
    row = categories.iloc[0, :]
    category_names = row.apply(lambda x: x[:-2])
    categories.columns = category_names
    
    for column in categories:
        categories[column] = categories[column].str[-1]
        categories[column] = categories[column].astype('int64')
        categories[column] = categories[column].apply(lambda x:
                                                x if ((x == 0) or 
                                                      (x == 1)) else 1)

    df.drop(labels='categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)

    df.drop_duplicates(inplace=True)
    df.drop_duplicates('id', keep=False, inplace=True)

    assert(df.duplicated().sum() == 0)
    assert(df['id'].duplicated().sum() == 0)

    return df


def save_data(df, database_filename):
    '''
    Takes a dataframe and saves it to an sql database
    '''
    engine = create_engine('sqlite:///{}'.format(database_filename))
    df.to_sql('messages', engine, index=False, if_exists='replace')


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()