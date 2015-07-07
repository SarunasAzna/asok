import sqlite3
conn = sqlite3.connect('locations.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE locations
             (title text, description text,  lat real, lng real)''')




# Larger example that inserts many records at a time
locations = [('Vilnius', 'Capital of Lithuania', 54.6833, 25.2833),
             ('Aarhus', 'Second largest city in Denmark', 56.1572, 10.2107),
             ('Hell', 'Norwegian hell', 63.4444, 10.9225),
             ('Fucking', 'Fucking, Austria', 48.0672, 12.8636)
            ]
c.executemany('INSERT INTO locations VALUES (?,?,?,?)', locations)

for row in c.execute('SELECT * FROM locations ORDER BY lat'):
        print(row)



# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()








