import flask

from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import package_service

blueprint = flask.Blueprint('packages', __name__, template_folder='templates')


@blueprint.route('/project/<package_name>')
@response(template_file='packages/details.html')
def package_details(package_name: str):
    # vm = PackageViewModel()
    #
    # print(f'package_name = {package_name}')
    # print(f'vm.package_name = {vm.package_name}')

    if not package_name:
        return flask.abort(404)

    package = package_service.get_package_by_id(package_name.strip().lower())
    if not package:
        return flask.abort(404)

    latest_version = "0.0.0"
    latest_release = None
    is_latest = True


    if package.releases:
        latest_release = package.releases[0]
        latest_version = latest_release.version_text

    return {
        'package': package_service.get_package_by_id(package_name),
        'latest_version': latest_version,
        'latest_release': latest_release,
        'release_version': latest_release,
        'is_latest': is_latest,
    }


@blueprint.route('/<int:rank>')
def popular(rank: int):
    # rank is passed here, already converted to an integer and everything!
    return f"The details for the {rank}th most popular package"
