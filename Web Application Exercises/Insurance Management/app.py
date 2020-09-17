from flask import Flask, url_for, render_template, request, redirect
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        user = request.form["user"]
        return redirect(url_for(user))


@app.route("/customer/", methods=["GET", "POST"])
def customer():
    if request.method == "GET": 
        return render_template("customer.html")
    else:
        customer_id = request.form["customer_id"]
        query = f"""
        SELECT PolicyID FROM PolicyRecord
        WHERE CustomerID = "{customer_id}" 
        """
        db = sqlite3.connect(
            "insurance.db")  # fetching data depending on CustomerID
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("userdisplay.html", data=data)


@app.route("/policydetails/", methods=["GET", "POST"])
def policydetails():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        policy_id = request.form["policyid"]
        query = f"""
        SELECT * FROM Policy
        WHERE PolicyID = "{policy_id}" 
        """
        db = sqlite3.connect(
            "insurance.db")  # fetching data depending on CustomerID
        cursor = db.execute(query)
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("policydetails.html", data=data[0])


@app.route("/agent/", methods=["GET", "POST"])
def agent():
    if request.method == "GET":
        return render_template("agent.html")
    else:
        team_no = request.form["team_no"]
        query = f"""
        SELECT name, BaseSalary from Agent
        WHERE TeamNo = {team_no}
        """
        db = sqlite3.connect("insurance.db")
        cursor = db.execute(query)
        team_member_info = cursor.fetchall()
        cursor.close()
        db.close()
        agent = []
        base_salary = []
        for member_info in team_member_info:
            if member_info[0] not in agent:  # name of the agent that sold the policy
                # initiating name list
                agent.append(member_info[0])
                # initiating salary list
                base_salary.append(member_info[1])
        # salary list for each month
        jan = agentsalaryhelper(team_no, 20200100, agent, base_salary.copy())
        feb = agentsalaryhelper(team_no, 20200200, agent, base_salary.copy())
        mar = agentsalaryhelper(team_no, 20200300, agent, base_salary.copy())

        formated_data = []
        # list of [name, jan salary, feb salary, mar salary]
        for i in range(len(agent)):
            formated_data.append([agent[i], jan[i], feb[i], mar[i]])
        return render_template("team.html", data=formated_data)


def agentsalaryhelper(team_no, monthstart, agent, salary):
    monthend = monthstart + 100
    query = f"""
        SELECT Agent.AgentID, Agent.name, BaseSalary, PolicyRecord.PolicyID, StartDate, Policy.ProtectedSum,Policy.CommissionRate FROM Agent
        INNER JOIN PolicyRecord, Policy
        ON Agent.AgentID = PolicyRecord.AgentID AND PolicyRecord.PolicyID = Policy.PolicyID
        WHERE TeamNo = {team_no} AND StartDate>"{monthstart}" AND StartDate<"{monthend}"
        """
    db = sqlite3.connect("insurance.db")
    cursor = db.execute(query)
    salary_data = cursor.fetchall()
    cursor.close()
    db.close()
    for entry in salary_data:
        # find index to update salary
        salaryindex = agent.index(entry[1])
        # update salary with new commission
        salary[salaryindex] += entry[5] * entry[6]
    return(salary)


if __name__ == "__main__":
    app.run(debug=False)
