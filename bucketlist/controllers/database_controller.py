"""
File      : database_controller.py
Date      : April, 2017
Author    : eugene liyai
Desc      : Acts as a service file for database population and db engine to be used
"""

# ============================================================================
# necessary imports
# ============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bucketlist.models.bucketlist import Bucketlist
from bucketlist.models.users import Users
from bucketlist.models.bucketlist_items import BucketlistItems
from bucketlist.models.initialize_db import init_bucketlist_database


class DatabaseController:

    def __init__(self, engine):
        """
        :param engine: The engine route and login details
        :return: a new instance of Database Controller class
        :type engine: string
        """
        if not engine:
            raise ValueError('The parameters specified in engine string are not supported by SQLAlchemy')
        self.engine = engine
        db_engine = create_engine(engine)
        db_session = sessionmaker(bind=db_engine)
        self.session = db_session()

    def initialize_database(self):
        """
        Initializes the database tables and relationships
        :return: None
        """
        init_bucketlist_database(self.engine)

    def drop_tables(self):
        """
        drops the database tables and relationships
        :return: None
        """
        BucketlistItems.__table__.drop(self.engine)
        Bucketlist.__table__.drop(self.engine)
        Users.__table__.drop(self.engine)

    def create_user(self, first_name, last_name, username, email, password):
        """

        The method creates and saves a new user to the database.

        :param first_name: First Name of the new user
        :param last_name: Last Name of the new user
        :param email: Email address of the new user
        :param username: User name selected by the new user
        :param password: Password for the new user
        :return: The id of the new user
        """

        new_user = Users(first_name=first_name, last_name=last_name, username=username,
                         email=email, password=password)
        self.session.add(new_user)
        self.session.commit()

        return {"user_id": new_user.user_id, "username": new_user.username}

    def get_user_by_email_or_username(self, username=None, email=None, serialize=False):
        """
        If the username parameter is  provided, the application looks up the user with the provided username,
        else it returns None

        :param username: The username of the user intended to be searched
        :param email: The email of user intended to be searched
        :return: The user with the matching username or email.
        """

        if isinstance(username, int) or isinstance(email, int):
            raise ValueError('Error in values passed to server!')

        single_user = None
        if username:
            single_user = self.get_by_username(username)
        elif email:
            single_user = self.get_by_email(email)

        if serialize and single_user:
            return [user.serialize() for user in single_user]
        else:
            return single_user

    def get_user_by_id(self, user_id=None, serialize=False):
        """
        If the user_id parameter is  provided, the application looks up the user with the provided id,
        else it returns all the users

        :param user_id: The id of the user intended to be searched(default value is None)
        :return: The user with the matching id or all users.
        """

        all_users = []

        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        if user_id is None:
            all_users = self.session.query(Users).order_by(Users.last_name).all()
        else:
            all_users = self.session.query(Users).filter(Users.user_id == user_id).all()

        if serialize:
            return [user.serialize() for user in all_users]
        else:
            return all_users

    def update_user(self, user_id, new_user):
        """
        The application looks up the user with the provided user_id
        in order to update the user's details

        :param user_id: The id of the user intended to be updated
        :param new_user: user object that holds updated details
        :return: The user with the matching id.
        """

        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        updated_user = None
        users = self.get_user_by_id(user_id)
        user = None
        if len(users) is not 1:
            return updated_user
        else:
            user = users[0]

        if user:
            user.email = new_user["email"]
            user.phone = new_user["username"]
            user.first_name = new_user["first_name"]
            user.last_name = new_user["last_name"]
            self.session.add(user)
            self.session.commit()
            updated_user = self.get_user_by_id(user_id)[0]

        return updated_user.serialize()

    def delete_user(self, user_id):
        """
        The application looks up the user with the provided user_id
        in order to delete the user object from the database

        :param user_id: The id of the user intended to be deleted
        :return: True if user object was deleted, else False.
        """
        if int(user_id) < 0:
            raise ValueError('Parameter [user_id] should be positive!')

        if user_id:
            user_deleted = self.session.query(Users).filter(Users.user_id == user_id).delete()
            return user_deleted > 0
        return False

    def create_bucketlist(self, bucketlist_name, user):
        """

        The method creates and saves a new bucketlist to the database.

        :param bucketlist_name: the bucketlist's name
        :param user: user that creates the bucketlist
        :return: The id of the new bucketlist
        """

        created_bucketlist = Bucketlist(bucketlist_name=bucketlist_name, user=user)
        self.session.add(created_bucketlist)
        self.session.commit()

        return created_bucketlist.bucketlist_name

    def get_bucketlist_by_id(self, bucket_id=None, serialize=False):
        """
        If the bucket_id parameter is  provided, the application looks up the buketlist with the provided id,
        else it returns all the bucketlists in the database

        :param bucket_id: The id of the bucketlist intended to be searched(default value is None)
        :return: The bucketlist with the matching id or all bucketlists.
        """

        all_bucketlists = []

        if int(bucket_id) < 0:
            raise ValueError('Parameter [bucket_id] should be positive!')

        if bucket_id is None:
            all_bucketlists = self.session.query(Bucketlist).order_by(Bucketlist.bucketlist_id).all()
        else:
            all_bucketlists = self.session.query(Bucketlist).filter(Bucketlist.bucketlist_id == bucket_id).all()

        if serialize:
            return [bucketlist.serialize() for bucketlist in all_bucketlists]
        else:
            return all_bucketlists

    def update_bucketlist(self, bucket_id, new_bucketlist):
        """
        The application looks up the bucketlist with the provided bucket_id
        in order to update the bucketlist's details

        :param bucket_id: The id of the bucketlist intended to be updated
        :param new_bucketlist: bucketlist object that holds updated details
        :return: The Bucketlist with the matching id.
        """

        if int(bucket_id) < 0:
            raise ValueError('Parameter [bucket_id] should be positive!')

        updated_bucketlist = None
        bucketlists = self.get_bucketlist_by_id(bucket_id)
        bucketlist = None
        if len(bucketlists) is not 1:
            return updated_bucketlist
        else:
            bucketlist = bucketlists[0]

        if bucketlist:
            bucketlist.bucketlist_name = new_bucketlist["bucketlist_name"]
            self.session.add(bucketlist)
            self.session.commit()
            updated_bucketlist = self.get_bucketlist_by_id(bucket_id)[0]

        return updated_bucketlist.serialize()

    def delete_bucketlist(self, bucket_id):
        """
        The application looks up the bucketlist with the provided bucket_id
        in order to delete the bucketlist object from the database

        :param bucket_id: The id of the bucketlist intended to be deleted
        :return: True if bucketlist object was deleted, else False.
        """

        if int(bucket_id) < 0:
            raise ValueError('Parameter [bucket_id] should be positive!')

        if bucket_id:
            bucketlist_deleted = self.session.query(Bucketlist).filter(Bucketlist.bucketlist_id == bucket_id).delete()
            return bucketlist_deleted > 0
        return False

    def create_bucketlist_item(self, bucketlist_item_name, description, bucketlist):
        """

        The method creates and saves a new bucket list item to the database.

        :param bucketlist_item_name: the item name
        :param description: detailed description of the item to be created
        :param bucketlist: bucketlist under which the item is created
        :return: The id of the new bucket list item id
        """

        new_bucketlist_item = BucketlistItems(item_name=bucketlist_item_name,
                                              description=description, bucketlist=bucketlist)
        self.session.add(new_bucketlist_item)
        self.session.commit()

        return new_bucketlist_item.item_name

    def get_item_by_id(self, item_id=None, serialize=False):
        """
        If the item_id parameter is  provided, the application looks up the item with the id, in the bucket lists
        available,
        else it returns all the items in the bucket list

        :param item_id: The id of the bucketlist intended to be searched(default value is None)
        :return: The bucketlist with the matching id or all bucketlists.
        """

        all_items = []

        if int(item_id) < 0:
            raise ValueError('Parameter [item_id] should be positive!')

        if item_id is None:
            all_items = self.session.query(BucketlistItems).order_by(BucketlistItems.item_id).all()
        else:
            all_items = self.session.query(BucketlistItems).filter(BucketlistItems.item_id == item_id).all()

        if serialize:
            return [item.serialize() for item in all_items]
        else:
            return all_items

    def get_by_username(self, username=None):
        """
        If the username parameter is  provided, the application looks up the user with the username provided.

        :param username: The username of the user intended to be searched(default value is None)
        :return: The user with the matching username.
        """
        searched_user = None

        if username:
            searched_user = self.session.query(Users).filter_by(username=username).first()

        return searched_user

    def get_by_email(self, email=None):
        """
        If the email parameter is  provided, the application looks up the user with the email provided.

        :param email: The email of the user intended to be searched(default value is None)
        :return: The user with the matching email.
        """

        searched_user = None

        if email:
            searched_user = self.session.query(Users).filter_by(email=email).first()

        return searched_user

    def update_bucketlist_item(self, item_id, new_item):
        """
        The application looks up the item with the provided item_id
        in order to update the items's details

        :param item_id: The id of the item intended to be updated
        :param new_item: item object that holds updated details
        :return: The item with the matching id.
        """

        updated_item = None
        items = self.get_item_by_id(item_id)
        item = None

        if int(item_id) < 0:
            raise ValueError('Parameter [item_id] should be positive!')

        if len(items) is not 1:
            return updated_item
        else:
            item = items[0]

        if item:
            item.item_name = new_item["item_name"]
            item.done = new_item["done"]
            item.description = new_item["description"]
            item.date_completed = new_item["date_completed"]
            self.session.add(item)
            self.session.commit()
            updated_item = self.get_item_by_id(item_id)[0]

        return updated_item.serialize()

    def user_login_authentication(self, username=None, email=None, password=None):
        """
        The method checks for username/email and password match in the database

        :param username: authentication username
        :param email: authentication email
        :param password: authentication password
        :return: dictionary of authentication status
        """
        if username and password:
            user = self.get_user_by_email_or_username(username=username)
            if user and user.check_user_password(password):
                return {'status': True, 'User': user}
            else:
                return {'status': False, 'User': None}
        elif email and password:
            user = self.get_user_by_email_or_username(email=email)
            if user and user.check_user_password(password):
                return {'status': True, 'User': user}
            else:
                return {'status': False, 'User': None}
        else:
            return {'status': False, 'User': None}

    def delete_bucketlist_item(self, item_id):
        """
        The application looks up the item with the provided item_id
        in order to delete the item object from the database

        :param item_id: The id of the item intended to be deleted
        :return: True if item object was deleted, else False.
        """

        if int(item_id) < 0:
            raise ValueError('Parameter [item_id] should be positive!')

        if item_id:
            item_deleted = self.session.query(BucketlistItems).filter(BucketlistItems.item_id == item_id).delete()
            return item_deleted > 0
        return False

    def populate_database(self):

        user1 = Users(first_name='eugene',
                      last_name='liyia',
                      username='liyai',
                      email='liyai@mail.com',
                      password='password')

        user2 = Users(first_name='mark',
                      last_name='maasai',
                      username='maasai',
                      email='maasai@mail.com',
                      password='password')

        self.session.add(user1)
        self.session.add(user2)
        self.session.commit()

        #
        # User's bucket lists
        #

        bucketlist1 = Bucketlist(bucketlist_name='Liyai_list',
                                 user=user1.user_id)

        bucketlist2 = Bucketlist(bucketlist_name='Maasai_list',
                                 user=user2.user_id)

        self.session.add(bucketlist1)
        self.session.add(bucketlist2)
        self.session.commit()
        #
        # Liyai's bucketlist items
        #

        bucketlist_item1 = BucketlistItems(item_name='Sky diving',
                                           description='Sign up for lake Naivasha sky diving on 23rd of may',
                                           bucketlist=bucketlist1.bucketlist_id)

        bucketlist_item2 = BucketlistItems(item_name='Water rafting',
                                           description='Sign up for white water rafting at Sagana lounge next week',
                                           bucketlist=bucketlist1.bucketlist_id)

        bucketlist_item3 = BucketlistItems(item_name='Give back to society',
                                           description="Visit Arch children's home and help out where possible",
                                           bucketlist=bucketlist1.bucketlist_id)

        #
        # Maasai's bucketlist items
        #

        bucketlist_item4 = BucketlistItems(item_name='Bungy jumping',
                                           description='Find a place that offers this service',
                                           bucketlist=bucketlist2.bucketlist_id)

        bucketlist_item5 = BucketlistItems(item_name='A kiss under the eiffel tower',
                                           description='Take Sandy to Paris on our anniversary',
                                           bucketlist=bucketlist2.bucketlist_id)

        bucketlist_item6 = BucketlistItems(item_name='Sing in a karaoke bar ',
                                           description="Sky lounge every wednesday, there's karaoke night",
                                           bucketlist=bucketlist2.bucketlist_id)

        self.session.add(bucketlist_item1)
        self.session.add(bucketlist_item2)
        self.session.add(bucketlist_item3)
        self.session.add(bucketlist_item4)
        self.session.add(bucketlist_item5)
        self.session.add(bucketlist_item6)
        self.session.commit()
