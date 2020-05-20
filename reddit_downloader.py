import praw
from psaw import PushshiftAPI
import json
import sqlite3
from sqlite3 import Error
import datetime as dt
import pandas as pd
import csv

    #Creating connection with sqlite database
def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    #Creating tables in the database
def create_table(conn, table_sql):
        try:
            c = conn.cursor()
            c.execute(table_sql)
        except Error as e:
            print(e)

def scrape():
    ##### CONFIG ######
    keys = {}
    with open("key.json","r") as f:
        keys= json.loads(f.read())

    #Setting up the API by reading values from JSON file
    Client_id = keys["client_id"] 
    Client_secret = keys["client_secret"]

    r_api = praw.Reddit(client_id = Client_id, client_secret = Client_secret, user_agent = "NYU-Analysis")
    api = PushshiftAPI(r_api)

    #Setting up database table
    sql_create_user_table = """CREATE TABLE IF NOT EXISTS user(
                                name text Primary Key, 
                                flair text, 
                                created_utc float NOT NULL
                                );"""

    sql_create_post_table = """ CREATE TABLE IF NOT EXISTS post(
                                id text Primary Key, 
                                name text NOT NULL, 
                                url text, 
                                title text, 
                                content text, 
                                score integer NOT NULL,
                                created_utc float NOT NULL,
                                permalink text,
                                link_flair_text text,
                                FOREIGN KEY (name) REFERENCES user (name)
                                );"""


    sql_create_comment_table =  """ CREATE TABLE IF NOT EXISTS comment(
                                    id text Primary Key, 
                                    name text NOT NULL, 
                                    content text, 
                                    score integer NOT NULL,
                                    comment_id text NOT NULL,
                                    link_id text NOT NULL,
                                    created_utc float NOT NULL, 
                                    FOREIGN KEY (name) REFERENCES user(name),
                                    FOREIGN KEY (comment_id) REFERENCES comment(id),
                                    FOREIGN KEY (link_id) REFERENCES post (id)
                                    );"""

    #Creating the sql table in the database
    conn = create_connection('R_NYU.db')
    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_post_table)
        create_table(conn, sql_create_comment_table)
        conn.close()
    else:
        print("Error! Can't create the database connection")

    conn = create_connection('R_NYU.db')
    #NYU subreddit was created on Nov 4th, 2009. All the data will be from the very beginning 
    if conn is not None:
        birthdate = int(dt.datetime(2009,1,1).timestamp())
        results = api.search_submissions(after = birthdate, subreddit = 'NYU', 
                                        filter = ['url','author','title', 'subreddit'], 
                                        limit = None)
        #Putting user and post data into the database
        for res in results:
            user = (str(res.author), res.created_utc)
            user_sql = """ INSERT INTO user(name, created_utc) VALUES (?,?)"""
            
            post = (res.id, str(res.author), str(res.url), str(res.title), str(res.selftext), 
                    res.score, res.created_utc, str(res.permalink), str(res.link_flair_text))
            post_sql = """INSERT OR IGNORE INTO post(id, name, url, title, content, score, 
                        created_utc, permalink, link_flair_text) VALUES (?,?,?,?,?,?,?,?,?)"""
            print(post)
            cur = conn.cursor()
            try:
                conn.execute(user_sql, user)
                conn.execute(post_sql, post)
            except:
                cur.close()
            conn.commit()
            
        conn.close()
            
    else:
        print("Error! Cannot make a connection")

    #Getting the post id
    conn = create_connection('R_NYU.db')
    posts = pd.read_sql("SELECT * FROM post", conn)
    id_list = posts['id'].tolist()

    #Inserting comment data into the database
    if conn is not None:
        for curr_id in id_list:
            sub = r_api.submission(id = curr_id)
            sub.comments.replace_more(limit = None)
            comments = sub.comments.list()
            #Inserting comments into the comment table
            for comment in comments:
                curr_com = (str(comment.id), str(comment.author), str(comment.body), comment.score, comment.parent_id, comment.link_id, comment.created_utc)
                com_sql = """INSERT OR IGNORE INTO comment (id, name, content, score, comment_id, link_id, created_utc) VALUES
                        (?,?,?,?,?,?,?)
                    """
                cur = conn.cursor()
                #We would also like to add users/authors of the comments to the database
                if comment.author is not None:
                    try: 
                        user = (str(comment.author), comment.author.created_utc)
                    except Exception as e:
                        print(e)
                    user_sql = """ INSERT OR IGNORE INTO user (name, created_utc) VALUES (?,?)"""
            
                    flair = (str(comment.author_flair_text), str(comment.author))
                    flair_sql = """UPDATE user SET flair = (?) WHERE name = (?)"""
                    
                    try:
                        cur.execute(user_sql, user)
                        cur.execute(flair_sql, flair)
                    except Error as e:
                        print(e)
                
                print('users comment is:', curr_com, 'user is', user, 'flair is', flair)
                try:
                    cur.execute(com_sql, curr_com)
                except Error as e:
                    print(e)
                
                conn.commit()
        conn.close()
    else:
        print("Error! Cannot connect to database!")
        
    #Getting users' subreddits 
    conn = create_connection('R_NYU.db')
    users = pd.read_sql("SELECT * FROM user", conn)
    users_name = users['name'].tolist()
    outputs = list()
    if conn is not None:
        for user in users_name:
            username = r_api.redditor(user)
            try:
                subreds = username.comments.new(limit=None)
                for subreddit in subreds:
                        subred = (user, str(subreddit.subreddit))
                        if subred not in outputs:
                            outputs.append(subred)
            except Exception as e:
                pass
    else:
        print("Error! Cannot connect to database!")


def convert_to_csv():
    #Create the connection
    conn = create_connection('R_NYU.db')

    #Getting the data into pandas dataframe
    posts = pd.read_sql("SELECT * FROM post", conn)
    users = pd.read_sql("SELECT * FROM user", conn)
    comments = pd.read_sql("SELECT * FROM comment", conn)

    posts.to_csv('data/reddit-posts.csv', encoding= 'utf-8', index = False)
    users.to_csv('data/reddit-users.csv', encoding= 'utf-8', index = False)
    comments.to_csv('data/reddit-comments.csv', encoding= 'utf-8', index = False)
    conn.close()

convert_to_csv()