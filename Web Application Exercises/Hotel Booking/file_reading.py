##import sqlite3
##
##with open("bookingrecords.csv") as f:
##    line = f.readline()
##    line = f.readline()
##    data = ""
##    db = sqlite3.connect("hotelbooking.db")
##    while line:
##        data = line[:-1]
##        data = tuple(data.split(","))
##        query = """
##                INSERT INTO BookingRecord VALUES(?,?,?,?,?,?)
##                """
##        db.execute(query, data)
##        db.commit()
##        line = f.readline()
##    db.close()
##
##with open("roomtypes.csv") as f:
##    line = f.readline()
##    line = f.readline()
##    data = ""
##    db = sqlite3.connect("hotelbooking.db")
##    while line:
##        data = line[:-1]
##        data = tuple(data.split(","))
##        query = """
##                INSERT INTO RoomType VALUES(?,?,?,?,?)
##                """
##        db.execute(query, data)
##        db.commit()
##        line = f.readline()
##    db.close()
##
##with open("rooms.csv") as f:
##    line = f.readline()
##    line = f.readline()
##    data = ""
##    db = sqlite3.connect("hotelbooking.db")
##    while line:
##        data = line[:-1]
##        data = tuple(data.split(","))
##        query = """
##                INSERT INTO Room VALUES(?,?,?,?,?)
##                """
##        db.execute(query, data)
##        db.commit()
##        line = f.readline()
##    db.close()
##
##with open("customers.csv") as f:
##    line = f.readline()
##    line = f.readline()
##    data = ""
##    db = sqlite3.connect("hotelbooking.db")
##    while line:
##        data = line[:-1]
##        data = tuple(data.split(","))
##        query = """
##                INSERT INTO Customer VALUES(?,?,?,?,?,?)
##                """
##        db.execute(query, data)
##        db.commit()
##        line = f.readline()
##    db.close()
##
##
##db = sqlite3.connect("hotelbooking.db")
##query = """
##        SELECT Level, Unit, RoomType, Price, Promotion, StartDate, NoOfDays FROM Room, Roomtype, BookingRecord, Customer
##        ON Room.RoomTypeID = RoomType.RoomTypeID AND BookingRecord.RoomID = Room.RoomID
##        WHERE BookingRecord.CustomerID = Customer.CustomerID AND Customer.name = "Derren Brett" AND BookingRecord.PaymentStatus = "Unpaid"
##        """
##cursor = db.execute(query)
##data = cursor.fetchall()
##
##print (data)
