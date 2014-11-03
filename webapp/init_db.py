from src import db
from src import models

db.drop_all()
db.create_all()
u = models.User('lee','123456')
a = '''
========================================
Every beauty start with ugly
========================================

Zero
----

Here, we start
'''
b = models.Article(a)
db.session.add(b)
db.session.add(u)
db.session.commit()
