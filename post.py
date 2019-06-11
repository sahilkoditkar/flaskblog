
from database import Database
import datetime

class Post(object):

    def __init__(self, author, title, content, date = datetime.datetime.utcnow()):
        self.author = author
        self.title = title
        self.content = content
        self.created_date = date

    def json(self):
        return {
            'author':self.author,
            'title':self.title,
            'content':self.content,
            'created_date':self.created_date
        }
    
    def add_post(self):
        Database.insert(collection='posts', data=self.json())

    @staticmethod
    def get_posts(query={}):
        return [post for post in Database.find(collection='posts', query=query)]