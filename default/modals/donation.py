from google.appengine.ext import ndb
from google.appengine.api import search


class Donations(ndb.Model):
    user = ndb.KeyProperty(kind='Users')
    title = ndb.StringProperty(required=True)
    city = ndb.StringProperty(required=True)
    country = ndb.StringProperty(required=True)
    state=ndb.StringProperty(required=True)
    quantity = ndb.IntegerProperty(required=True)
    comments = ndb.TextProperty()
    photo_key = ndb.BlobKeyProperty()
    photo_url = ndb.StringProperty()


    @classmethod
    def add_new_donation(cls, title, quantity, city, country, state,comments, photo_key, photo_url, user_key=None):
        user_id = str(user_key.id())
        donation_key = cls(title=title, quantity=quantity, city=city, country=country,state=state, comments=comments,
                           photo_key=photo_key, photo_url=photo_url, user=user_key).put()
        index = search.Index('donation')
        doc = search.Document(doc_id=str(donation_key.id()), fields=[search.TextField(name='title', value=title),
                                                                     search.TextField(name='city', value=city),
                                                                     search.TextField(name='country', value=country),
                                                                     search.TextField(name='state', value=state),
                                                                     search.TextField(name='comments', value=comments),
                                                                     search.NumberField(name='quantity',
                                                                                        value=quantity),
                                                                     search.TextField(name='photo_url',
                                                                                      value=photo_url),
                                                                     search.TextField(name='user_id', value=user_id)], )
        index.put(doc)

    @classmethod
    def get_all_donations_user(cls, user_id):
        index = search.Index('donation')
        query = 'user_id:(%s)' % user_id
        results = index.search(query)
        return results.results