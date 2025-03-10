from sqlite3 import connect, Connection
from sys import argv


def stripArcade(db: Connection):
    cleaned = []

    for arcade_id, name in db.execute(
        """
        SELECT 
        arcade_id, 
        name
        FROM `arcades`
        """
    ).fetchall():
        cleaned.append((name.strip(), int(arcade_id)))

    db.executemany(
        """
        UPDATE `arcades`
        SET name = ?
        WHERE arcade_id = ?;
        """,
        cleaned,
    )


def stripCabinets(db: Connection):
    cleaned = []

    for cabinet_id, name in db.execute(
        """
        SELECT 
        cabinet_id, 
        cabinet_name
        FROM `cabinets`;
        """
    ).fetchall():
        cleaned.append((name.strip(), int(cabinet_id)))

    db.executemany(
        """
        UPDATE `cabinets`
        SET cabinet_name = ?
        WHERE cabinet_id = ?;
        """,
        cleaned,
    )


def stripCountries(db: Connection):
    cleaned = []

    for id, name in db.execute(
        """
        SELECT
        id, 
        name
        FROM `countries`;
        """
    ).fetchall():
        cleaned.append((name.strip(), int(id)))

    db.executemany(
        """
        UPDATE `countries`
        SET name = ?
        WHERE id = ?
        """,
        cleaned,
    )


if __name__ == "__main__":
    database = argv[1]
    db = connect(database)

    stripArcade(db)
    stripCabinets(db)
    stripCountries(db)

    db.commit()
