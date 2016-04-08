from framework.request_handler import FoodSearchRequestHandler
from google.appengine.api import search


class SearchDonations(FoodSearchRequestHandler):
    def get(self):
        query = self.request.get('q')
        if not query:
            self.redirect('/')
        else:
            index = search.Index('donation')
            snippet = 'snippet("%s",comments,100)' % query
            options=search.QueryOptions(
                returned_expressions=[
                    search.FieldExpression(name='snippet',expression=snippet)
                ]
            )
            results=index.search(
               query=search.Query(
                   query_string=query,
                   options=options
               )
           )
            docs=[]
            if results:
                docs=results.results
            tpl_values={
                'donation':docs,
                'query':query
            }
            self.render('serp/serp.html',**tpl_values)