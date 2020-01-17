import os
import pypi_org.data.db_session as db_session
from pypi_org.data.package import Package
from pypi_org.data.releases import Release
from pypi_org.services.user_service import create_user


def main():
    init_db()
    # while True:
    #     insert_a_package()
    insert_a_user()

def init_db():
    # init db session to talk with db.  Similar to how in our app we open up a single session
    # This really just inits the db_session.__factory connected to this path, that way we can use it to create sessions
    # later
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join("..", "db", "pypi.sqlite")
    db_file = os.path.join(top_folder, rel_file)
    db_session.global_init(db_file)


def insert_a_user():
    success = create_user(name="Andrew",
                          email="a@b.com",
                          password="supersecret",
                          profile_image_url=None,
                          )
    if success:
        print("User added successfully")
    else:
        print("User not added")


def insert_a_package():
    p = Package()
    p.id = input("Package id / name: ").strip().lower()

    p.summary = input("Package summary: ").strip()
    p.author_name = input("Author: ").strip()
    p.license = input("License: ").strip()

    print("Release 1:")
    r = Release()
    r.major_ver = int(input("Major version: "))
    r.minor_ver = int(input("Minor version: "))
    r.build_ver = int(input("Build version: "))
    # this attaches the relationship with r to the Package p.  sa will traverse this object and see this relationship
    # and know it must add r even if we don't explicitly do a session.add(r) here.  Adding r here might be awkward since
    # we might have an auto generated p.primary_key, etc...
    p.releases.append(r)

    # if we want a second release object, we can do the same thing and again append to p.releases
    print("Release 2:")
    r = Release()
    r.major_ver = int(input("Major version: "))
    r.minor_ver = int(input("Minor version: "))
    r.build_ver = int(input("Build version: "))
    p.releases.append(r)

    session = db_session.create_session()

    # # Old way (before we had a db_session.create_session()).  Old way also had no type hinting
    # # If you want to see what the session object can do, you can use type casting
    # import sqlalchemy.orm as orm
    # session: orm.Session = db_session.__factory()
    # # Now type session <dot> <tab> and everything is available!

    # Add the changes we want to commit to the db (don't need to add r's because of the relations we already appended)
    session.add(p)

    # Once we have changes to commit (all at once), do a commit
    session.commit()


if __name__ == "__main__":
    main()
