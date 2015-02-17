# -*- coding: UTF-8 -*-

# THIRD-PARTY MODULES
from bottle import request, response
import time

#LOCAL MODULES
import database
#Here you can import your database module, this is a demo import

class User(object):

    def __init__( self ):
        self.db = database.DatabaseUsers() #database connection
        self.COOKIE_SECRET_KEY = 'yet_another_very_secret_key' #change this key to yours
        self.loggedin = False
        self.credentials = None
        self.validate() #validating user to see if he is logged in

    def authenticate( self , email , password ):
        '''
        @type email str
        @type password dict

        Checks user credentials and authenticates him in system.
        '''
        if email and password:
            user = self.db.find_user( email, password ) #if user exitsts

            if user:
                last_login = {
                    'last_login': time.strftime( 
                                        '%Y.%m.%d %H:%M:%S GMT',
                                        time.gmtime( time.time() )
                                    )
                }
                self.db.update_user( uemail= email , ulastlogintime = last_login,ulastauth ='webapp' ) #updating last_login
                self.set_cookie( str(user['_id']) )
                self.loggedin = True
                self.credentials = user
                return True

        return False

    def loginusinggoogle(self, google_json):
        '''
        @type email str
        @type password dict

        Checks user credentials and authenticates him in system.
        '''
        {u'family_name': 'Marr\\xc3\\xa3o Rodrigues', u'name': 'Hugo Marr\\xc3\\xa3o Rodrigues', u'picture': 'https://lh3.googleusercontent.com/-5C4DJsnFrQY/AAAAAAAAAAI/AAAAAAAAAhc/syjLemW4kaM/photo.jpg', u'locale': 'en', u'gender': 'male', u'id': '117948364019653655693', u'link': 'https://plus.google.com/117948364019653655693', u'given_name': 'Hugo', u'email': 'marrao@gmail.com', u'verified_email': 'True'}
        email = google_json['email']
        if email:
            user = self.db.find_user( email, None ) #if user exitsts

            if user:
                last_login = {
                    'last_login': time.strftime( 
                                        '%Y.%m.%d %H:%M:%S GMT',
                                        time.gmtime( time.time() )
                                    )
                }
                self.db.update_user( email , last_login ) #updating last_login
                self.set_cookie( str(user['_id']) )
                self.loggedin = True
                self.credentials = user
                return True

        return False

    def loginusingfacebook(self, facebook_json):
        '''
        '''
        print facebook_json
        pass

    def loginusingtwitter(self, twitter_json):
        '''
        '''
        print twitter_json
        pass

    def logout( self ):
        '''
        Initiates user logout by destoying cookie.
        '''

        self.remove_cookie()
        self.loggedin = False
        self.credentials = None

        return True

    def register( self , **kwargs ):
        '''
        @type email str
        @type password str
        @type accepted str

        Get email, password and age acceptance from register page, 
        checks if email is already registered, hashes password with 
        md5 and store user data.
        '''
        register_options = {'ufname':None, 'ulname':None, 'uname':None, 'uemail': None, 'upassword':None,
        'ulastauth':None,'ulastlogindatetime':None,'ufirstauth':None,'ufirstlogindatetime':None}
        register_options.update(kwargs)

        if register_options['uemail'] and register_options['upassword']:

            if not self.db.find_user( register_options['uemail'] ): #no user exists
                uinfo = self.db.add_user( **register_options )
                uid = uinfo['_id']

                if uid: #if user added successful
                    self.set_cookie( str(uid) )
                    self.loggedin = True
                    self.credentials = self.db.return_user_by_objectid( uid )
                    return True

        return False

    def validate( self ):
        '''
        Validates user email credential by decrypting encrypted cookie.
        Indicates that user is logged in and verified. If verification
        fails - destroys cookie by calling logout method ( because of
        possible cookie fraud ). Stores user info in credentials
        attribute in case of successful decryption.
        '''

        #uid = request.get_cookie( 'teste' , secret = self.COOKIE_SECRET_KEY )
        uid = request.get_cookie( 'teste' ,)
        user = self.db.return_user_by_objectid( uid )

        if user:
            self.loggedin = True
            self.credentials = user
            return True

        self.logout()
        return None

    #COOKIES
    def set_cookie( self, uid ):
        '''
        Sets user cookie based on his uid.
        '''
        response.set_cookie( 
                'teste',
                str(uid),
#                secret = self.COOKIE_SECRET_KEY,
                expires = time.time() + ( 3600*24*365 ),
                #domain = 'smehogar-ekergy.rhcloud.com',
                path = '/'
        )

        #print request.get_cookie( 'teste' , secret = self.COOKIE_SECRET_KEY )

    def remove_cookie( self ):
        '''
        Destroys user cookie.
        '''
        response.set_cookie(
                'teste',
                '',
                #secret = self.COOKIE_SECRET_KEY,
                expires = time.time() - ( 3600*24*365 ),
                #domain = 'smehogar-ekergy.rhcloud.com',
                path = '/'
        )
