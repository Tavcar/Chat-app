#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
from models import Sporocilo
from operator import attrgetter
from datetime import datetime


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()
        urejen = sorted(seznam, key=attrgetter("nastanek"), reverse=True)
        params = {"seznam": urejen}
        return self.render_template("base.html", params=params)

    def post(self):
        ime = self.request.get("ime") or "Anonimnež"
        vnos = self.request.get("vnos")
        nastanek = datetime.now().strftime("%d-%m-%Y ob %H.%M.%S")
        sporocilo = Sporocilo(ime=ime, vnos=vnos, nastanek=nastanek)
        sporocilo.put()
        return self.redirect_to("prva")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/', MainHandler, name="prva"),
], debug=True)
