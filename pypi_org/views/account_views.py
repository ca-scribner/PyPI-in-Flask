import flask

from pypi_org.infrastructure.view_modifiers import response

import pypi_org.infrastructure.cookie_auth as cookie_auth
from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel
from pypi_org.viewmodels.account.login_viewmodel import LoginViewModel
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = flask.Blueprint("account", __name__, template_folder='templates')


# ##################### INDEX ##########################################

@blueprint.route("/account")
@response(template_file="account/index.html")
def index():
    # Using this IndexViewModel means we don't have to keep track of all the extra data we're exchanging below
    vm = IndexViewModel()
    # user_id = cookie_auth.get_user_id_via_auth_cookie(flask.request)
    # user = find_user_by_id(user_id)
    if not vm.user:
        return flask.redirect('/account/login')
    return vm.to_dict()


# ##################### REGISTER #######################################

# This pattern lets us write two separate functions for the account/register endpoint.  The first handles serving up
# an empty registration page. The second handles processing information the user posts to the page.  These could be
# in the same method and accept ["GET", "POST"] and then direct, but they're very different actions and flask lets us
# handle that up front without our own logic.
@blueprint.route("/account/register", methods=['GET'])
# @response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    if vm.user_id_logged_in:
        return flask.redirect('/account')
    else:
        return flask.render_template('/account/register.html')


@blueprint.route("/account/register", methods=["POST"])
def register_post():
    # ViewModel gets name/email/password from flask.request, checks whether they're filled out, and if so tries to
    # register a user.  We just interpret the results here.
    # These are broken into a few calls here, although originally I had it as all in __init__.  This is more clear about
    # what is happening though

    vm = RegisterViewModel()

    vm.validate()
    if vm.error:
        return flask.render_template("/account/register.html", **vm.to_dict())

    vm.create_user()
    if vm.error:
        return flask.render_template("/account/register.html", **vm.to_dict())

    resp = flask.redirect("/account")
    cookie_auth.set_auth(resp, vm.user.id)
    return resp


# ##################### LOGIN ##########################################

@blueprint.route("/account/login", methods=["GET"])
def login_get():
    vm = LoginViewModel()
    if vm.user_id_logged_in:
        return flask.redirect('/account')

    return flask.render_template("/account/login.html")


@blueprint.route("/account/login", methods=["POST"])
def login_post():
    vm = LoginViewModel()

    if vm.user_id_logged_in:
        return flask.redirect('/account')

    resp = vm.login_user()
    return resp


# ##################### LOGOUT #########################################

@blueprint.route("/account/logout", methods=["GET"])
def logout():
    resp = flask.redirect("/")
    cookie_auth.logout(resp)
    return resp
