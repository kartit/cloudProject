from google.appengine.ext import ndb
from hashlib import sha256
from base64 import b64encode
from os import urandom
import uuid


class Users( ndb.Model ):
    name = ndb.StringProperty( required=True )
    email = ndb.StringProperty( required=True )
    password = ndb.StringProperty( required=True )
    confirmation_code = ndb.StringProperty( required=True )
    confirmation_email = ndb.BooleanProperty( default=False )

    @classmethod
    def if_user_exists(cls, email):
        return cls.query( cls.email == email ).get( )

    @classmethod
    def add_new_user(cls, name, email, password):
        user = cls.if_user_exists( email )

        if not user:
            random_bytes = urandom( 64 )
            salt = b64encode( random_bytes ).decode( 'utf-8' )
            hashed_pass = salt + sha256( salt + password ).hexdigest( )
            confirmation_code = str( uuid.uuid4( ).get_hex )

            new_user_key = cls(
                name=name,
                email=email,
                password=hashed_pass,
                confirmation_code=confirmation_code
            ).put( )
            print "************entering users.py****"
            print new_user_key
            return {
                'created': True,
                'user_id': (new_user_key.id( )),
                'confirmation_code': confirmation_code
            }
        else:
            return {
                'created': False,
                'title': "Email is already taken",
                'message': 'Please choose a different email'
            }

    @classmethod
    def check_password(cls, email, password):
        user = cls.if_user_exists( email )

        if user:
            hashed_password = user.password
            salt = hashed_password[0:88]
            check_password = salt + sha256( salt + password ).hexdigest( )
            if check_password == hashed_password:
                print user.key.id()
                return user.key.id( )
            else:
                return None
        else:
            return None
