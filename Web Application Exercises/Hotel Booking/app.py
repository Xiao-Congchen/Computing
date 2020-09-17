from flask import Flask, url_for, render_template, request, redirect
import sqlite3
from werkzeug.utils import secure_filename
import os.path
import random

app = Flask(__name__)

# OS
ALLOWED_EXTENSIONS = set(['bmp', 'gif', 'jpg', 'jpeg', 'png'])
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)),'static\\images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# OS

@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        picture_or_room = request.form["picture or room"]
        # directs user to respective page
        return redirect(url_for(picture_or_room))
                           
@app.route("/upload/", methods = ["GET", "POST"])
def picture():
    if request.method == "GET":
        query = """SELECT RoomType FROM RoomType"""  # dynamically getting all room types
        db = sqlite3.connect("hotelbooking.db")
        cursor = db.execute(query)
        room_types = cursor.fetchall()
        db.close()
        return render_template("picture.html", room_types = room_types)
    else:
        room = request.form["room"]  # to get room type to insert picture into
        query = """SELECT RoomTypeID FROM RoomType
                WHERE RoomType = ?"""
        db = sqlite3.connect("hotelbooking.db")
        cursor = db.execute(query, (room,))
        room_id = cursor.fetchone()[0]
        room_type = "roomtype_0" + f"{room_id}"
        db.close()
        #print(room_type)
        pic = request.files["picture"]
        if pic.filename != '':
            #checks that the file extension is of defined type
            if pic.filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                file = secure_filename(pic.filename)
                file = room_type + file[-4:]
                #updating database
                pic.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
                query = """UPDATE RoomType
                        SET RoomImage = ?
                        WHERE RoomTypeID = ?"""
                db = sqlite3.connect("hotelbooking.db")
                db.execute(query, (f"/static/images/{file}",room_id))
                db.commit()
                db.close()
                
                query = """SELECT * FROM RoomType WHERE RoomTypeID = ?"""
                db = sqlite3.connect("hotelbooking.db")
                cursor = db.execute(query, (room_id,))
                data = cursor.fetchall()[0]
                print(data)
                return render_template("room_display.html", data = data)
            else:
                return "Upload failed because file is not an image. Please refresh and retry."
            


@app.route("/room_booking/", methods = ["GET", "POST"])
def room():
    if request.method == "GET":
        query = """SELECT * FROM RoomType"""  # dynamically getting all room types
        db = sqlite3.connect("hotelbooking.db")
        cursor = db.execute(query)
        room_info = cursor.fetchall()
        db.close()
        return render_template("booking.html", room_info = room_info)
    else:
        room_type_id = request.form['room']  # getting all data
        start_date = request.form['startdate']
        no_of_days = request.form['noofdays']
        customer_id = request.form['customerid']
        #print(room_id, start_date, no_of_days, customer_id)
        
        # picking a random room of the type specified to book
        query = """SELECT RoomID FROM Room WHERE RoomTypeID=?"""
        db = sqlite3.connect("hotelbooking.db")
        cursor = db.execute(query,(room_type_id,))
        data = cursor.fetchall()
        db.close()
        room_id = random.choice(data)[0]  
        #print(data,room_id)
        
        # update database on booking record
        query = """INSERT INTO BookingRecord(RoomID, CustomerID, StartDate, NoOfDays, PaymentStatus)
                VALUES(?,?,?,?,?)"""
        db = sqlite3.connect("hotelbooking.db")  
        db.execute(query,(room_id, customer_id, start_date, no_of_days, "Unpaid"))
        db.commit()
        db.close()

        # getting booking details
        query = """SELECT * FROM BookingRecord WHERE RoomID=?"""
        db = sqlite3.connect("hotelbooking.db")  
        cursor = db.execute(query,(room_id,))
        data = cursor.fetchall()[-1]
        db.close()
        return render_template("booking_confirmation.html", data=data)
        


if "__main__" == __name__:
    app.run(debug = False)
