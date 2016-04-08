from framework.request_handler import FoodSearchRequestHandler

class Home( FoodSearchRequestHandler ):
    def get(self):
        self.render('home/home.html')
