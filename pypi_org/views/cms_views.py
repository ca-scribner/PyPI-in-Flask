import flask

import pypi_org.services.cms_service as cms_service

blueprint = flask.Blueprint('cms', __name__, template_folder='templates')


# Can use path type which will capture the actual path, not just a single /part/
@blueprint.route("/<path:full_url>")
def cms_page(full_url: str):
    print(f"Getting CMS page for {full_url}")

    page = cms_service.get_page(full_url)
    if not page:
        # If page does not exist, tell the user by returning a abort 404
        return flask.abort(404)

    return flask.render_template("cms/page.html", **page)
