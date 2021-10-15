from models import db, users, Post
from app import app

db.drop_all()
db.create_all()

default = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'

Larry = users(first_name='Larry', last_name='Rockland', image_url=default)
Joel = users(first_name='Joel', last_name='Burton',
             image_url='https://pbs.twimg.com/profile_images/1217917608/IMG_3419_400x400.jpg')
Alda = users(first_name='Alda', last_name='Alva', image_url=default)

post1 = Post(title='First Post', content='Hello World', user_id='1')

db.session.add(Larry)
db.session.add(Joel)
db.session.add(Alda)

db.session.add(post1)

db.session.commit()
