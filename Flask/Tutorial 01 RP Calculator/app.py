from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/rp_calc/", methods=["GET", "POST"])
def rp_calc():
    if request.method == "GET":  # If typed in/directed over
        return render_template("rp_calc.html")
    else:  # Extract data
        PW, MT = request.form["PW"], request.form["MT"]

        subjects = ["H2 Subject 1", "H2 Subject 2",  # Base subjects
                    "H2 Subject 3", "H1 Subject", "General Paper"]
        if PW == "Yes":
            subjects.append("Project Work")
        if MT == "Yes":
            subjects.append("Mother Tongue")
        # Provides rp_calc_marks with subject list
        return render_template("rp_calc_marks.html", subjects=subjects)


rp = {  # Dictionary of rank points
    "A": 20.00,
    "B": 17.50,
    "C": 15.00,
    "D": 12.50,
    "E": 10.00,
    "S": 5.00,
    "U": 0.00
}


@app.route("/rp_display/", methods=["GET", "POST"])
def rp_display():
    if request.method == "GET":  # If user tries to access display page before providing details
        return render_template("rp_calc.html")
    else:  # If it is from rp_calc_marks, start calculation
        results = request.form  # obtains all data
        result_list = []
        max_pt = 0
        total_pt = 0
        for info in results:
            if info[0:2] == "H2":  # Check if subject is H2
                result_list.append(  # Subject Name, Grade, RP style
                    (info, results[info][0], '%.2f' % rp[results[info][0]]))
                max_pt += rp["A"]
                total_pt += rp[results[info][0]]
            else:  # H1 Subjects get half points
                result_list.append(
                    (info, results[info][0], '%.2f' % (rp[results[info][0]] / 2)))
                max_pt += rp["A"]/2
                total_pt += rp[results[info][0]] / 2
        if max_pt != 90.0:  # To calculate rank points upon 90 if MT is included
            total_pt = (total_pt / max_pt) * 90.0
        return render_template("rp_display.html", result=result_list, total=total_pt)


if __name__ == "__main__":
    app.run(debug=True)
