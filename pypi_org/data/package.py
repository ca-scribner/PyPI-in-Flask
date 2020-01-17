import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from pypi_org.data.modelbase import SqlAlchemyBase
from pypi_org.data.releases import Release


class Package(SqlAlchemyBase):
    # Without __tablename__, sqlalchemy will name the underlying table the same as the data class.  But for us,
    # the data class is properly a single package, whereas the table is a holder of many packages.  This lets us keep
    # everything feelign consistent

    __tablename__ = "packages"

    id = sa.Column(sa.String, primary_key=True)
    # NOTE: we use the datetime.datetime.now FUNCTION, not the current time.  sa will call this for us
    # index=True makes this indexed to make sorting/searching better(?)
    # - yes, it maintains an ordered search table (or something like that) that gives O(logn) searching (binary search)
    #   instead of O(n) searching (assumably at the cost of storage space --> Yes, roughly doubling the data being
    #   indexed!)
    #   using "EXPLAIN QUERY PLAN SELECT author_email FROM packages WHERE author_email = 'xyz'" will return how it will
    #   be done (if indexed, it can search rather than scan)
    # - these can also get used by SQLite when we do something like order by.  It wont redo that work if we index
    # - remember that indexes will make add/update/drop slower.  If you do a lot of this, consider dropping the index
    #   before doing these then recreating after
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    last_updated = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    summary = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    home_page = sa.Column(sa.String)
    docs_url = sa.Column(sa.String)
    package_url = sa.Column(sa.String)

    author_name = sa.Column(sa.String)
    author_email = sa.Column(sa.String, index=True)

    license = sa.Column(sa.String, index=True)

    # maintainers

    # releases relationship
    # order_by can take a list to get multiple order columns!
    # This releases object acts like a list that we can append to to add relations.  Example shown in bin/basic_inserts.py
    releases = orm.relation("Release", order_by=[
        Release.major_ver.desc(),
        Release.minor_ver.desc(),
        Release.build_ver.desc(),
    ],
                            back_populates="package",  # Maintain i-directional link so if we change something
                                                       # after getting to it through release.package it comes here (?)
                            )

    def __repr__(self):
        return f"<Package {self.id}>"
