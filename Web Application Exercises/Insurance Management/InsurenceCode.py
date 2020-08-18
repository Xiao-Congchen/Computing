import sqlite3

connection = sqlite3.connect("Insurence.db")

agent = """
CREATE TABLE Agent
(
AgentID TEXT PRIMARY KEY UNIQUE,
Name TEXT NOT NULL,
Gender TEXT NOT NULL CHECK(Gender = "M" or Gender = "F"),
Appointment TEXT NOT NULL,
TeamNo INTEGER NOT NULL,
BaseSalary REAL NOT NULL
)
"""
connection.execute(agent)

customer = """
CREATE TABLE Customer
(
CustomerID TEXT PRIMARY KEY UNIQUE,
Name TEXT NOT NULL,
Gender TEXT NOT NULL CHECK(Gender = "M" or Gender = "F"),
DoB INTEGER NOT NULL,
Address TEXT NOT NULL,
HealthCondi TEXT
)
"""
connection.execute(customer)

policy = """
CREATE TABLE Policy
(
PolicyID TEXT PRIMARY KEY,
YearlyPremium REAL NOT NULL,
TotalYears INTEGER NOT NULL,
ProtectedSum REAL NOT NULL,
CommissionRate REAL NOT NULL
)
"""
connection.execute(policy)

policyrecord = """
CREATE TABLE PolicyRecord
(
PolicyRecordNo INTEGER,
AgentID TEXT NOT NULL,
CustomerID TEXT NOT NULL,
PolicyID TEXT NOT NULL,
StartDate TEXT NOT NULL,
FOREIGN KEY("PolicyID") REFERENCES "Policy"("PolicyID"),
FOREIGN KEY("AgentID") REFERENCES "Agent"("AgentID"),
FOREIGN KEY("CustomerID") REFERENCES "Customer"("CustomerID")
PRIMARY KEY("PolicyRecordNo" AUTOINCREMENT)
)
"""
connection.execute(policyrecord)

connection.commit()

with open("agents.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(",")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO Agent VALUES {lines}")
        connection.commit()
        lines = f.readline()
        
### OR ##########################################
'''
with open("agents.csv", "r") as f:
    lines = f.readline()  # ignoring header line
    lines = f.readline()[:-1]  # ignoring \n
    while lines:
        data = lines.split(",")
        connection.execute("INSERT INTO Agent VALUES(?,?,?,?,?,?)", tuple(data))
        connection.commit()
        lines = f.readline()[:-1]
'''
#################################################
        
with open("customers.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.replace('"', '')
        lines = lines.replace(", ", "!@")
        lines = lines.split(",")
        lines = str(lines)
        lines = lines.replace("!@", ", ")
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO Customer VALUES {lines}")
        connection.commit()
        lines = f.readline()

with open("policies.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(",")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO Policy VALUES {lines}")
        connection.commit()
        lines = f.readline()

with open("policyrecords.csv", "r") as f:
    lines = f.readline()
    lines = f.readline()
    while lines:
        lines = lines[:-1]
        lines = lines.split(",")
        lines = str(lines)
        lines = "(" + lines[1:-1] + ")"
        connection.execute(f"INSERT INTO PolicyRecord VALUES {lines}")
        connection.commit()
        lines = f.readline()

query = """
SELECT PolicyRecordNo, StartDate, PolicyRecord.AgentID, Agent.Name, PolicyID FROM PolicyRecord
INNER JOIN Agent
ON PolicyRecord.AgentID = Agent.AgentID
WHERE Agent.name = "Pippa Booth" AND PolicyRecord.StartDate >= "20200101" AND PolicyRecord.StartDate <= "20201231"
ORDER BY PolicyRecord.StartDate ASC
"""
cursor = connection.execute(query)
for row in cursor:
    print(row)

connection.close
