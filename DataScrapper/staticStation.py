import json
import sqlalchemy as sqla
from createdbtable import conn


def staticStation():
    # STATIC DATA
    # Read dublin.json and get data store in dub
    f = open('dublin.json', 'r')
    content = f.read()
    dub = json.loads(content)

    # Populate static data into database
    # First get each station's information in tuple form
    for dbstation in dub:
        dbvals = (int(dbstation.get('number')),
                  dbstation.get('name'),
                  dbstation.get('address'),
                  float(dbstation.get('latitude')),
                  float(dbstation.get('longitude')))
        # Then populate static data into table dublin
        conn.execute(sqla.text("""INSERT INTO dbbikes.dublin VALUES(%i,"%s","%s",%f,%f);""" % dbvals))
        conn.commit()
