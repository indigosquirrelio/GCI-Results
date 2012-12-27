# coding=utf-8
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Main(BaseHandler):
    def get(self):
        self.render("front.html")
    def post(self):
        text = self.request.get("text")
        text = text.split("\n")
        user = []
        parent = []
        first = text[0]
        if 'Student' in first:
            for i in range(len(text)-1):
                child = text[i+1].split(",")
                user.append(child[2])
                child = [child[0], child[1], child[2]]
                parent.append(child)
            for i in range(len(user)):
                parent[i].append(user.count(user[i]))
            sorted_parent = sorted(parent, key=lambda tup: tup[-1], reverse=True)
            keys = []
            users = []
            for i in range(len(sorted_parent)):
                if parent[i][2] not in users:
                    keys.append([parent[i][2], parent[i][3]])
                    users.append(parent[i][2])
            text = self.request.get("text")
            sorted_keys = sorted(keys, key=lambda tup: tup[-1], reverse=True)
            for i in range(len(sorted_keys)):
                sorted_keys[i].append((i+1))
            error = "none"
            self.render('front.html', keys = sorted_keys, text = text, values = sorted_parent, error = error)
        else:
            text = self.request.get("text")
            error = "error"
            self.render('front.html', text = text, error = error)




app = webapp2.WSGIApplication([('/', Main)],
                              debug=True)
