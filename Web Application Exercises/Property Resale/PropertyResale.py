import sqlite3

connection = sqlite3.connect("PropertyResale.db")

user = """
CREATE TABLE User
(
UserID TEXT UNIQUE,
Name TEXT,
Contact INTEGER,
Email TEXT,
PRIMARY KEY("UserID")
)
"""
connection.execute(user)

Property = """
CREATE TABLE Property
(
PropertyID TEXT UNIQUE,
Address TEXT,
Postal INTEGER,
TotalArea INTEGER,
NoOfBedroom INTEGER,
NoOfToilet INTEGER,
AskingPrice REAL,
Status TEXT DEFAULT 'FALSE' CHECK(Status == "FALSE" or Status == "TRUE"),
PRIMARY KEY("PropertyID")
)
"""
connection.execute(Property)

record = """
CREATE TABLE Record
(
RecordID INTEGER,
SellerID TEXT,
PropertyID TEXT,
DateListed INTEGER,
BuyerID TEXT,
SoldPrice REAL,
SoldDate INTEGER,
FOREIGN KEY("SellerID") REFERENCES "User"("UserID"),
FOREIGN KEY("PropertyID") REFERENCES "Property"("PropertyID"),
FOREIGN KEY("BuyerID") REFERENCES "User"("UserID"),
PRIMARY KEY("RecordID" AUTOINCREMENT)
)
"""
connection.execute(record)

with open("users.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(";")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO User VALUES {lines}")
        connection.commit()
        lines = f.readline()

with open("properties.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(";")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO Property VALUES {lines}")
        connection.commit()
        lines = f.readline()

with open("records.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(";")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        print(lines)
        connection.execute(f"INSERT INTO Record VALUES {lines}")
        connection.commit()
        lines = f.readline()

query = """
SELECT RecordID, DateListed, SellerID, User.Name, Record.PropertyID FROM Record
INNER JOIN User
ON Record.SellerID = User.UserID
INNER JOIN Property
ON Property.PropertyID = Record.PropertyID
WHERE Property.Status = "FALSE" AND Property.NoOfBedroom = 3 AND Property.NoOfToilet = 3
ORDER BY Property.AskingPrice ASC
"""
cursor = connection.execute(query)
for row in cursor:
    print(row)
    
connection.close
