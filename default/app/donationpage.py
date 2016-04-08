from framework.request_handler import FoodSearchRequestHandler
from modals.donation import Donations


class DonationPage(FoodSearchRequestHandler):
    def get(self, donation_id):
        donation = Donations.get_by_id(int(donation_id))
        template_value = {'donation': donation}
        self.render('donation-page/donation-page.html', **template_value)
