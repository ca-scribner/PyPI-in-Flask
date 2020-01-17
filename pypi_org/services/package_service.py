from typing import List, Optional
import sqlalchemy.orm

from pypi_org.data.db_session import create_session
from pypi_org.data.package import Package
from pypi_org.data.releases import Release


def get_latest_releases(limit=10) -> List[Release]:
    session = create_session()

    # Without joinedload, a single query gets all releases we want, but then an additional limit queries get the
    # associated packages (one package per query) which is rough!  joinedload turns these into a single query
    releases = session.query(Release) \
        .options(sqlalchemy.orm.joinedload(Release.package)) \
        .order_by(Release.created_date.desc()) \
        .limit(limit) \
        .all()

    # Before doing the joinedload, this below code helped prevent lazy loading.  But with the joinedload it breaks.
    # Trying to expunge on each package and release it appears raises an exception?

    # (from before adding joined load): Close the session so it doesn't lazily load things later
    # if we don't do this, access to these releases could still be db calls, even when fired by the html page builds.
    # And, if we depend on that, the connection could be garbage collected (?) and not exist when we expect (I was
    # getting intermittent errors that seemed like that or something similar).
    # But, if we don't expunge first, we won't have a static view of that data
    # for r in releases:
    #     session.expunge(r.package)
    #     session.expunge(r)
    # session.close()

    # But, if we don't close the session at all, that also raises an exception.  Not sure if this expunge_all is needed?
    session.expunge_all()
    session.close()

    return releases


def get_package_count() -> int:
    session = create_session()
    return session.query(Package).count()


def get_release_count() -> int:
    session = create_session()
    return session.query(Release).count()


def get_package_by_id(package_id: str) -> Optional[Package]:
    if not package_id:
        return None

    session = create_session()
    # Like above, need to do a joinedload to eager load the things we will eventually use.  Otherwise, when the
    # html later tries to look at the releases, it will try to use this (now closed) session!
    package = session.query(Package)\
        .options(sqlalchemy.orm.joinedload(Package.releases))\
        .filter(Package.id == package_id.strip().lower())\
        .first()

    session.close()
    return package
