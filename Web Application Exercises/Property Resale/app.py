from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/buy/", methods=["GET", "POST"])
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        RecordID, BuyerID, SoldPrice, SoldDate = request.form["RecordID"], request.form[
            "BuyerID"], request.form["SoldPrice"], request.form["SoldDate"]

        # establishing connection with database
        db = sqlite3.connect("PropertyResale.db")

        # query to get property id
        propertyid_query = f"""
        SELECT PropertyID FROM Record WHERE Record.RecordID = "{RecordID}"
        """
        cursor = db.execute(propertyid_query)
        propertyID = cursor.fetchall()[0][0]

        # query to update Record
        update_query = f"""
        UPDATE Record SET
        BuyerID = "{BuyerID}",
        SoldPrice = "{SoldPrice}",
        SoldDate = "{SoldDate}"
        WHERE Record.RecordID = "{RecordID}"
        """
        update_query_2 = f"""
        UPDATE Property SET
        Status = "TRUE"
        WHERE PropertyID = "{propertyID}"
        """
        db.execute(update_query)
        db.execute(update_query_2)
        db.commit()

        # query to get user info
        user_query = f"""
        SELECT * FROM User WHERE UserID = "{BuyerID}"
        """
        cursor = db.execute(user_query)
        userinfo = cursor.fetchall()

        # query to get property info
        property_query = f"""
        SELECT * FROM Property WHERE PropertyID = "{propertyID}"
        """
        cursor = db.execute(property_query)
        propertyinfo = cursor.fetchall()

        db.close()
        print(userinfo[0])
        print(propertyinfo[0])
        return render_template("profile.html", userinfo=userinfo[0], propertyinfo=propertyinfo[0])


@app.route("/profile/")
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(debug=False)
