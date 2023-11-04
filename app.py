import sys
sys.path.append("database")
import sanic
from sanic import Sanic,response,json
from sanic_cors import CORS, cross_origin
from sanic.response import text,html
from sanic_ext import render
from sanic_jinja2 import SanicJinja2
from script import Model

app = Sanic(__name__)
CORS(app)
jinja = SanicJinja2(app, enable_async=True)
app.static('/img/logo.png', './templates/img/logo.png')


MODEL = Model()

@app.route("/")
async def home(req):
    template = await jinja.render_async("home.html",req)
    return response.html(template.body)

@app.route("/templates/video/<file>")
async def video(req, file):
    return await response.file("./templates/video/" + file)

@app.route("/index.js")
async def index_js(req):
    return await response.file("templates/index.js")


@app.route("/",methods=["GET"],version=2)
async def logo(req):
    return await response.file("logo.png")

@app.route("/signin",methods=["POST","GET"])
async def signin(req):
    template = await jinja.render_async("signin.html",req)
    return response.html(template.body)

@app.route("/style.css",methods=["GET","POST"])
async def style(req):
    return await response.file("templates/style.css")

@app.route("/base.css",methods=["POST","GET"])
async def base_css(req):
    return await response.file("templates/base.css")

@app.route("/style_signin.css",methods=["GET","POST"])
async def style_base(req):
    return await response.file("templates/style_signin.css")


@app.route("/register",methods=["POST"])
async def register(req: sanic.Request):
    global data1
    data1 = req.json
    
    if not MODEL.verification(data1):
        return response.json({'error': 'among us exists'})
    
    MODEL.user_data(data1)
    template =  await jinja.render_async("home.html",req)
    return response.html(template.body)
@app.route("/login.js")
async def login_js(req):
    return await response.file("templates/login.js")

@app.route("/login",methods=["POST","GET"])
async def login(req: sanic.Request):
    template =  await jinja.render_async("login.html",req)
    return response.html(template.body)

@app.route("/success", methods=["POST"])
async def login_success(req: sanic.Request):
    data = req.json
    if MODEL.confirmation_login(data.get('mail'),data.get('user')):
        return response.json({"error":"among us not exist"})
    return response.json({"success": "is success"})

@app.route("/search.js")
async def search(req):
    return await response.file("templates/search.js")

@app.route("/base",methods=["POST","GET"])
async def base(req):
    template = await jinja.render_async("base.html",req)
    return response.html(template.body)

@app.route("/product")
async def product(req):
    template = await jinja.render_async("product.html",req)
    return response.html(template.body)

@app.route("/Orders",methods=["POST"])
async def Orders(req:sanic.Request):
    data = req.json
    MODEL.Order_data(data.get("name"),data.get("quantity"),data.get("os"),data.get("price"))
    return response.json({"success":"is successe"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002,debug=True)  # Lancer Sanic sur le port 8001
