from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Party

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQL_ALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User({'username':'jawnboy', 'email':'jawnboy@yahoo.com','password':'iamjawnboy'})
        #u.set_password('iamjawnboy')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('iamjawnboy'))

    def test_avatar(self):
        u=User({'username':'john', 'email':'john@example.com','password':'iamjohn'})
        #print(u.avatar(128))
        #print('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

    def test_follow(self):
        u1 = User({'username':'jawnboy', 'email':'jawnboy@yahoo.com','password':'iamjawnboy'})
        u2 = User({'username':'nicky6', 'email':'nicky6@yahoo.com','password':'iamnicky6'})
        db.session.add(u1)
        db.session.add(u2)
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(),1)
        self.assertEqual(u1.followed.first().username, 'nicky6')
        self.assertEqual(u2.followers.count(),1)
        self.assertEqual(u2.followers.first().username, 'jawnboy')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User({'username':'jawnboy', 'email':'jawnboy@yahoo.com','password':'iamjawnboy'})
        u2 = User({'username':'nicky6', 'email':'nicky6@yahoo.com','password':'iamnicky6'})
        u3 = User({'username':'john', 'email':'john@yahoo.com','password':'iamjohn'})
        u4 = User({'username':'susan', 'email':'susan@yahoo.com','password':'iamsusan'})
        db.session.add_all([u1, u2, u3, u4])

        #create four parties
        p1 = Party({'title':'jawnboy with it','owner_id':1})
        p2 = Party({'title':'nicky6 with it','owner_id':2})
        p3 = Party({'title':'john with it','owner_id':3})
        p4 = Party({'title':'susan with it', 'owner_id':4})
        db.session.add_all([p1,p2,p3,p4])
        db.session.commit()

        #setup the followers
        u1.follow(u2) #jawnboy follows nicky6
        u1.follow(u4) #jawnboy follows susan
        u2.follow(u3) #nicky6 follows john
        u3.follow(u4) #mary follows david
        db.session.commit()

        #check the followed parties of each user
        f1 = u1.followed_parties().all()
        f2 = u2.followed_parties().all()
        f3 = u3.followed_parties().all()
        f4 = u4.followed_parties().all()

        #make sure they follow the write parties
        self.assertEqual(f1, [p4,p2,p1])
        self.assertEqual(f2, [p3,p2])
        self.assertEqual(f3, [p4,p3])
        self.assertEqual(f4, [p4])



if __name__ == '__main__':
    unittest.main(verbosity=2)
