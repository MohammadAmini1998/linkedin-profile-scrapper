import sqlite3
import csv
con = sqlite3.connect('Dataa.db')
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS records 
               (name text, location text, degree_level text,connections text, job text,link text)''')
con.commit()

def addRecord(name,location,degree,connections,job,link):
    cur.execute("INSERT INTO records VALUES(?,?,?,?,?,?)",(name,location,degree,connections,job,link))
    con.commit()


def showRecords():
    for row in cur.execute('SELECT * FROM records'):
        print(row)

def csv_convertor():
    cur.execute("select * from records;")
    with open("Dataa.csv", 'w',newline='') as csv_file: 
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cur.description]) 
        csv_writer.writerows(cur)