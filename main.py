#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")


class SteviloHandler(BaseHandler):
    def post(self):
        stevilo = self.request.get("vnos1")
        if stevilo == str(43):
            odgovor = "Bravo uganil si skrito stevilo!"
        elif stevilo > str(43):
            odgovor = "Ni ti uspelo, tvoja cifra je previsoka"
        else:
            odgovor = "Ni ti uspelo, tvoja cifra je prenizka"
        params = {"stevilo": stevilo, "odgovor": odgovor}
        self.render_template("skritostevilo.html", params)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/skritostevilo', SteviloHandler)
], debug=True)
