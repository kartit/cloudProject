from framework.request_handler import FoodSearchRequestHandler
from lib.cloudstorage import cloudstorage_api
from google.appengine.api import blobstore
from google.appengine.api import images
from modals.donation import Donations


class UserAccount(FoodSearchRequestHandler):
    @FoodSearchRequestHandler.login_required
    def get(self):
        user_id = self.check_user_logged_in.key.id()
        print user_id
        donations = Donations.get_all_donations_user(user_id)
        tpl_values = {'donation': donations}
        self.render('/account/account_home.html', **tpl_values)


class ShareNew(FoodSearchRequestHandler):
    @FoodSearchRequestHandler.login_required
    def get(self):
        self.render('account/post_new_share.html')

    @FoodSearchRequestHandler.login_required
    def post(self):
        user_key = self.check_user_logged_in.key
        title = self.request.get('title').encode("utf-8")
        quantity = int(self.request.get('quantity').encode("utf-8"))
        city = self.request.get('city').encode("utf-8")
        country = self.request.get('country').encode()
        state=self.request.get('state').encode()
        comments = self.request.get('comments').encode()
        photo = self.request.POST['image']
        saved_photo = self.save_image(photo, user_key)
        print (user_key, title, quantity, city, country);
        Donations.add_new_donation(title=title, quantity=quantity, city=city, country=country,state=state, comments=comments,
            photo_key=saved_photo['blobstore_key'], photo_url=saved_photo['serving_url'], user_key=user_key,

        )
        self.redirect('/account')

    @classmethod
    def save_image(cls, photo, user_key=None):
        img_title = photo.filename
        img_content = photo.file.read()
        img_type = photo.type

        cloud_storage_path = '/gs/fooddonation/%s/%s' % (user_key.id(), img_title)
        blobstore_key = blobstore.create_gs_key(cloud_storage_path)
        print blobstore_key
        cloud_storage_file = cloudstorage_api.open(filename=cloud_storage_path[3:], mode='w', content_type=img_type)
        cloud_storage_file.write(img_content)
        cloud_storage_file.close()

        blobstore_key = blobstore.BlobKey(blobstore_key)
        serving_url = images.get_serving_url(blobstore_key)
        print serving_url
        return {'serving_url': serving_url, 'blobstore_key': blobstore_key}
