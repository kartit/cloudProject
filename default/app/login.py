from framework.request_handler import FoodSearchRequestHandler
from modals.users import Users


class LoginUser( FoodSearchRequestHandler ):
    def get(self):
        self.render( 'login/login.html' )

    def post(self):
        email = self.request.get( 'email' )
        password = self.request.get( 'password' )
        user_id = Users.check_password( email, password )
        print email
        if user_id:
            print user_id
            self.send_cookie( name='User', value=user_id )
            self.redirect( '/account' )

        else:
            self.redirect( '/login' )
