import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import package_service, user_service

# Not sure what the names here mean
from viewmodels.home.index_viewmodel import IndexViewModel
from viewmodels.shared.viewmodelbase import ViewModelBase

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


@blueprint.route('/')
@response(template_file='home/index.html')
def index():
    vm = IndexViewModel()

    # If you don't use the @response, we'd return like this:
    #     return flask.render_template('home/index.html', packages=test_packages)
    return vm.to_dict()


@blueprint.route('/about')
@response(template_file='home/about.html')
def about():
    vm = ViewModelBase()

    # If you don't use the @response, we'd return like this:
    #     return flask.render_template('home/about.html')
    return vm.to_dict()
