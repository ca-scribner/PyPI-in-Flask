import sqlalchemy as sa
from pypi_org.data.modelbase import SqlAlchemyBase


class Maintainer(SqlAlchemyBase):
    __tablename__ = "maintainers"

    # Need to be set as foreign key relationships, which I think we will do in packages (but maybe could do here
    # instead?)
    user_id = sa.Column(sa.Integer, primary_key=True)
    package_id = sa.Column(sa.String, primary_key=True)
