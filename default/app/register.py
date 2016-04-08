from framework.request_handler import FoodSearchRequestHandler
from modals.users import Users
from google.appengine.api import mail
from os import environ
import re


class RegisterUser( FoodSearchRequestHandler ):
   # @classmethod
    # def send_email(cls, to, user_id, confirmation_code):
    #     email_object=mail.EmailMessage(
    #     sender='noreply@coen691-1193.appspotmail.com',
    #     subject='Confirm Your Email mail',
    #     to=to
    #     )
    #     email_parameter={
    #         'domain':'http://localhost:8080' if environ['SERVER_SOFTWARE'].startswith('Development') else'http://coen691-1193.appspot.com',
    #         'user_id':user_id,
    #         'confirmation_code':confirmation_code
    #     }
    #     html_from_tem=cls.jinja_environment.get_template('email/confirmation_email.html').render(email_parameter)
    #     email_object.html=html_from_tem
    #     email_object.send()
    def post(self):
        email = self.request.get( 'email' )
        name = self.request.get( 'name' )
        password = self.request.get( 'password' )
        status = 200
        print name, email, password

        if name and email and password:

            email_validation_pattern = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if re.match( email_validation_pattern, email ):

                user = Users.add_new_user( name, email, password )
                if user['created']:
                    pass
                    html = self.jinja_environment.get_template( 'commons/register_modal_sucess.html').render()
                    json_response = {
                        'html': html
                    }
                    self.send_email( to=email, user_id=user['user_id'], confirmation_code=user['confirmation_code'] )
                else:
                    status = 400
                    json_response = user
            else:
                status = 400
                json_response = {
                    'created': False,
                    'title': "this email is not valid",
                    'message': "please enter a valid email"
                }

        else:
            status = 400
            json_response = {}

            if not email:
                json_response.update(
                    {
                        'title': 'you have not sent us an email',
                        'message': 'Please send us a valid email address,thanks!'
                    }
                )
            if not password:
                json_response.update(
                    {
                        'title': 'Please type in a password',
                        'message': 'Please a send us ur password'
                    }
                )
            if not name:
                json_response.update(
                    {
                        'title': 'The Name field is required',
                        'message': 'Please fill in your name in order to continue'
                    }
                )

        self.json_response( status_code=status, **json_response )
