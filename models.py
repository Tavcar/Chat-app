from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    ime = ndb.StringProperty()
    vnos = ndb.StringProperty()
    nastanek = ndb.StringProperty()
