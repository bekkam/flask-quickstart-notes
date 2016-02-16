
# Import the Flask class.  An instance of this class will be our WSGI application
from flask import Flask
# import the request object
from flask import request

from flask import render_template, redirect, make_response

# Create an instance of the Flask class.  The first argument is the name of the
# application's module package.  If using a single module (like here),
# use __name__ bc depending on if its started as an application or module,
# the name will be different ('__main__' versus the actual import name).
# This is needed so Flask knows where to look for templates, static files, etc.

# Instantiate a Flask object called "app", passing it the name of the application's module package.
app = Flask(__name__)

# Use the route() decorator to tell Flask what URL should trigger our function
@app.route('/')
# The function is given a name which is also used to generate URLs for that particular function,
# and returns the message we want to display in the user's browser.
def hello_world():
    # return "Hello World!!!"
        return """
    <!DOCTYPE hmtl>
    <html>
        <body>
            <h1>Hi there!</h1>
        </body>
    </html>"""

# ********Routing ************
# The route() decorator binds a URL to a function. You can make certain parts of the
# URL dynamic
# 1. Variable rules:
#   A. To add variable parts to a URL, mark these special sections as <variable_name>.
#       Such a part is then passed as a keyword arg to your function.  You can also
#       convert such a variable from string to int, float, or path by spcifying
#       <converter:variable_name>

# Python arguments: a value passed to a function (or method) when calling the function.
#   2 types of arguments:
#   1. keyword arg: an argument preceded by an identifier (eg name=) in a fxn call or
#       passed as a value in a dict preceded by **. Both 3 and 5 are keyword args:
#       complex(real=3, imag=5)
#   2. Positional arg: arg that's not a keyword arg:
#       complex(3,5)
#   Args are assigned to named local variables in a function body.

# Trailing Slashes
# @app.route('/projects/')        accessible if user types '/projects' or '/projects/'  --> use this one
# @app.route('/projects')         accessible only if user types '/projects'

# Example:
# Bind the URL '/user/<username>' to the function show_user_profile
# Pass <username> to the function as a keyword argument.
# Keyword 'username' is assigned to local variable username.
# Route answers browser's Get request
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # sent the return statement to the browser
    return 'User %s' % username

# Float converter 404s if user enters int, eg '/post/6/'
@app.route('/post/<float:post_id>/')
def show_post_(post_id):
    # show the post with the given id, the id is an float
    print "hello"
    # return "post_id is %d" % post_id
    return """
    <!DOCTYPE hmtl>
    <html>
        <body>
            <h1>Hi there %f!</h1>
        </body>
    </html>""" % (post_id)

# ******The methods argument******
# By default, a route only answers to GET requests.
# Change this behavior w/ the methods arg to route() decorator

# Request - Response:  Client/browser sends requests to a server; server responds w/ html
# Client Requests:
# The http method tells the server what the client want to do with the requested page

# GET request method - Browser sends get request to server; request contains the exact URL
# the user wants. Designed to retrieve information from the server. As part of a GET request,
# some data can be passed within the URL's query string, specifying, for example, search terms,
# date ranges, or other information that defines the query.

# POST request method - Browser tells server that it wants to post some new info to that URL,
# and that the server must ensure the data is stored and only stored once. This is how
# html forms usually transmit data to a server, assuming the form info should alter the db.
# Search forms are usu only for retrieval, so often will be get requests,
# unless such search data is sensitive.
#   Previously, the only methods a form could submit to the server were Get and Post.
#   With JS and html5, forms can submit other methods to a server

# Server Response: server sends response to browser; response contains the
# exact html for that page

@app.route('/login/', methods=['GET', 'POST'])
def login():
    pass
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

# ************* Rendering Templates ******************

# Jinja is a template engine for the Python programming language. jinja provides Python-like expressions
#  while ensuring that the templates are evaluated in a sandbox. It is a text-based template language
#  and thus can be used to generate any markup as well as sourcecode.

# Flask configures the Jinja2 template engine automatically.

# To use, import render_template from flask. In the view function's return statement
# call the render_template() method, passing in the variables you want to pass
# to the template engine as keyword arguments

# Example:  both URLs route to the same view function.  The view function renders
# the template hello.html, passing in the keyword arg name=name.
# hello.html is formatted based on name's value.  Server sends resulting
# html to browser.
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    # (flask will look for the hello.html template in the templates folder)
    return render_template('hello.html', name=name)


# ************** Redirects *************
# To redirect a user to another endoint, use the redirect() function.
@app.route('/something/')
def index():
    return redirect('/hello')


# ************** Errors ********************

# @errorhandler() decorator lets you customize the error page
# 404 after the render_template call tells flask the page was not found; by default, 200 is
# assumed which translates to all went well.
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404

# ************** Responses ********************
# In Flask, the return value from a view fxn is automatically converted into a response object for you.

# Flask's logic in converting return values into response objects is:
# 1. if response object of correct type is returned, its directly returned from the view
# 2. if its a string, a response object is created - the string is the response body, a 200 OK
# error code and a test/html mimetype.
# 3. If a tuple is returned, the tuple can fprovide extra info.  Such tuples must take the form
# (response, status, headers).  Headers can be a list, or dict of additional header values.
# If 1-3 don't work, Flask assumes the return value is a valid WSGI application & converts
# it to a response object.

# To get ahold of the resulting response object inside the view, you can use the make_response()
# function,  For example, to get the response object of the not_found fxn, wrap the return expression
# with make_response() and get the response object to modify it, then return it:
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['Date'] = 'Beginning of time'               #Changes header Date to "Beginning of time"
    return resp
     # return render_template('error.html'), 404

# ************* Running the Application **************************
# Use the run() function to run the local server with our application.
# Only run the server if the script is executed directly from the python interpreter,
# and not used as an imported module
if __name__ == '__main__':
    app.debug = True
    app.run()


# By enabling debugging, the server will reload itself on code changes,
# and provide a debugger if things go wrong.  There are 2 ways to enable
# debugging: set the flag on the application object (app.debug=True),
# or pass it as a parameter to run (app.run(debug=True))
