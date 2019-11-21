import psycopg2
import csv

#For connecting to the database
conn = psycopg2.connect("host=ec2-23-23-92-204.compute-1.amazonaws.com port=5432 dbname=d3osb2va95ounc user=lgblsznbvphfrp password=1421cd0e3f11a3d472a215008ae23f015cc7864ecbf615ab47c499c62ec102fe")
cur = conn.cursor()

#importing csv file
with open('books.csv', 'r') as f:
	reader = csv.reader(f)
	next(reader)

	for row in reader:
		cur.execute("INSERT INTO books VALUES (%s, %s, %s, %s)",
					row 
					)
		print("adding...please wait")
		conn.commit()
		





		iam a hacker but i forgot it and studying this fucking useless for days :(
		 but not so long sure i'll be back to you love you lots...and miss u 