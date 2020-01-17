# This file makes a factory that is shared across the app and will only be created the first time we init something(?).
# If we already have a factory, then this function has no action regardless of input.
# I guess the global factory here is shared across anything in the app that imports this?  <--Yes, tried it myself.

import sqlalchemy as sa
import sqlalchemy.orm as orm

from pypi_org.data.modelbase import SqlAlchemyBase

# Hide the factory as private.
__factory = None


def global_init(db_file: str, echo: bool = True):
    """
    Initializes a single shared factory for all db access in this app
    """
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    conn_str = "sqlite:///" + db_file.strip()
    print(f"Connecting to DB with {conn_str}")

    # Set echo=False if you don't want to see what SQL calls are being fired
    engine = sa.create_engine(conn_str, echo=echo)

    # orm.sessionmaker() returns a callable that can create sessions (eg: units of work - the things that package our
    # calls to the db together instead of firing off atomic calls separately)
    __factory = orm.sessionmaker(bind=engine)

    # Tell SqlAlchemy about our ORM/Package.  Only needed this one time, so import in here.  pycharm thinks this is
    # a useless command, but it actually isn't
    # ...we could have the imports here directly, but Michael prefers to have them grouped together somewhere
    # noinspection PyUnresolvedReferences
    import pypi_org.data.__all_models

    SqlAlchemyBase.metadata.create_all(engine)
    print("global_init complete")


def create_session() -> sa.orm.Session:
    """
    Create and return a session through this factory
    """

    global __factory
    return __factory()
