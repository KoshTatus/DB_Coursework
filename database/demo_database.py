from sqlalchemy import text
from database import SessionLocal

countries_demo = [row.split(',') for row in open("countries_demo.txt")]

print(countries_demo)


#add_demo()
