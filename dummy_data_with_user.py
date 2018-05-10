from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_with_user import Category, Base, Items, User

engine = create_engine('sqlite:///itemcatalogwithUser.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create User
user1 = User(name="ayush dids", email="ayush97didwaniya@gmail.com")
session.add(user1)
session.commit()

user2 = User(name="Ayush Didwaniya", email="didwaniya.ayush@gmail.com")
session.add(user2)
session.commit()

# items for Soccer
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

Item1 = Items(name="soccer shin Gaurd", description="xzcvxzv", price="$2.99",
              category=category1, user=user1)
session.add(Item1)
session.commit()

Item2 = Items(name="soccer ball", description="fsgsd", price="$5.50",
              category=category1, user=user1)
session.add(Item2)
session.commit()

Item3 = Items(name="soccer shoes", description="scvxc", price="$3.99",
              category=category1, user=user2)
session.add(Item3)
session.commit()

# Items for basketball
category2 = Category(name="Basketball")
session.add(category2)
session.commit()

Item1 = Items(name="Basketball ball", description="asddas", price="$2.99",
              category=category2, user=user1)
session.add(Item1)
session.commit()

Item2 = Items(name="Basketball Shoes", description="sadfs", price="$5.50",
              category=category2, user=user2)
session.add(Item2)
session.commit()

# Items for Baseball
category3 = Category(name="Baseball")
session.add(category1)
session.commit()

Item1 = Items(name="baseball shoes", description="asdfadf", price="$2.99",
              category=category3, user=user2)
session.add(Item1)
session.commit()

Item2 = Items(name="baseball ball", description="savxzv", price="$5.50",
              category=category3, user=user1)
session.add(Item2)
session.commit()


# Items for Frisball
Category4 = Category(name="Frisbee")
session.add(Category4)
session.commit()

Item1 = Items(name="frisball ball", description="fasfasf", price="$2.99",
              category=Category4, user=user2)
session.add(Item1)
session.commit()

Item2 = Items(name="Frisball shoes", description="dsfaf",
              price="$5.50", category=Category4, user=user2)
session.add(Item2)
session.commit()

# Items for snowbording
Category5 = Category(name="Snowbording")
session.add(Category5)
session.commit()


Item1 = Items(name="Snowbording Snowbord", description="dfadfasf",
              price="$2.99", category=Category5, user=user1)
session.add(Item1)
session.commit()

Item2 = Items(name="Snowbording goggles", description="safasaf", price="$5.50",
              category=Category5, user=user1)
session.add(Item2)
session.commit()

# Items for rockclimbing
Category6 = Category(name="Rockclimbing")
session.add(Category6)
session.commit()


Item1 = Items(name="rope", description="safasg", price="$2.99",
              category=Category6, user=user2)
session.add(Item1)
session.commit()

Item2 = Items(name="shoes rockclimb", description="Juicy grilled"
              "chicken patty with tomato mayo and lettuce",
              price="$5.50", category=Category6, user=user2)
session.add(Item2)
session.commit()

# Items for Foosball
Category7 = Category(name="Foosball")
session.add(Category7)
session.commit()

Item1 = Items(name="Foosball ball", description="sdgsbxc", price="$2.99",
              category=Category7, user=user2)
session.add(Item1)
session.commit()

Item2 = Items(name="Foosball goggles", description="safafav", price="$5.50",
              category=Category7, user=user1)
session.add(Item2)
session.commit()


# Items for Skating
Category8 = Category(name="Skating ")
session.add(Category8)
session.commit()

Item1 = Items(name="skates", description="dafasf", price="$2.99",
              category=Category8, user=user1)
session.add(Item1)
session.commit()

Item2 = Items(name="skating helmet", description="safasf", price="$5.50",
              category=Category8, user=user2)
session.add(Item2)
session.commit()

print "added menu items!"
