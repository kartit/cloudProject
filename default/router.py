from webapp2 import WSGIApplication
from webapp2 import Route

app = WSGIApplication(
    routes=[
        Route( '/', handler='app.home.Home' ),
        Route( '/register', handler='app.register.RegisterUser' ),
        Route('/login',handler='app.login.LoginUser'),
        Route('/account',handler='app.account.UserAccount'),
        Route('/account/share-my-food',handler='app.account.ShareNew'),
        Route('/search',handler='app.serp.SearchDonations'),
        Route('/donation/<donation_id:[0-9]+>',handler='app.donationpage.DonationPage'),

    ]
)
