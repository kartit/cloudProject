from hashlib import sha256

SECRET = "in559GvextmUceX5Ewc8I91KSzF1LFdKER+0PfqrPOdoMyWddKme9LfRoPFT2gdddj5sALWYWPiz14L02/xo6Q=="


def sign_cookie(value):
    string_value = str( value )
    signature = sha256( SECRET + string_value ).hexdigest( )
    return signature + "|" + string_value


def check_cookie(value):
    signature = value[:value.find( '|' )]
    declared_value = value[value.find( '|' ) + 1:]

    if sha256( SECRET + declared_value ).hexdigest( ) == signature:
        return declared_value
    else:
        return None
