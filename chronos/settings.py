
from chronos.metadata import Setting, Session


def get_setting(key):
    """Get setting value from database. Return None or value."""
    session = Session()
    value = session.query(Setting).get(key)
    session.close()

    return value


def set_setting(key, value):
    """Update setting or create new."""
    session = Session()
    if get_setting(key) is None:
        session.add(
            Setting(
                key=key,
                value=value
            )
        )
    else:
        session.query(Setting).get(key).value = value

    session.commit()
    session.close()
