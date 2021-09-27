"""
Main python file for Help4All Website.
This File should be run as it is the main server.
Running any file other than this will lead to not running the server.
"""

from flask import Flask, render_template, request, url_for, redirect  # Importing all flask dependencies

import myEmail, dbmanager  # Import custom tools

import random  # Import other library (ies)

app = Flask(
    __name__, static_folder="static",
    template_folder="pages")  # initialized a flask app



@app.route("/favicon.ico")  # Favicon
def favicon():
	return redirect(
	    url_for('static', filename="favicon.ico")
	)  # This favicon was generated using the online tool at favicon.io


@app.route("/")  # Home Page...
def home():
	return render_template("index.html")



@app.route("/contact", methods=["POST"])
def contact():
    name = request.form["name"]
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]

    myEmail.send("nalinangrish2005@gmail.com", subject=subject, text=message+f"\n\nFrom: {name}\n{email}")

    return render_template("contact.html", name=name)


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/donate")
def donate():
    return render_template('donate.htm')

@app.route("/signup")
def signup():
    return render_template('signup.htm')



@app.route(
    "/donate/process",
    methods=["POST", "GET"])  # Process data submitted through donate form
def donateprocessor():
    name = request.form['namefirst'] + " " + request.form['namelast']  # Get all data
    phone = request.form['areaCode'] + request.form['phone']
    address = request.form['address']
    item = request.form['typeOf']
    if(item=="Cash"):
        item = item + " : " + request.form['amount']
    notes = request.form['notes']

    index = str(dbmanager.addOrder(name, phone, address, item, notes))  # Use dbmanager to add a help request and get it's index number for further operations
    infoUrl = str(request.url_root)[:-1] + url_for('orders', num=index)  # Generate url for information about order (For NGOs)
    NGOList = dbmanager.getNGOs()

    for NGO in NGOList:  # Get list of NGOs and send each one of them an email to notify them about a new donor along with the information link
        NGOname, NGOemail = tuple(NGO)
        myEmail.send(
		    NGOemail,
		    subject=f"Help4All - {name} wants to help you",
		    text=
		    "We have recieved an order from {}. As we knew that your organisation {} operates here, we thought to inform you about it. You can visit the details about this order from {}"
		    .format(name, NGOname, infoUrl))

    return render_template("donatesuccess.htm", number=index)


@app.route("/orders/<num>")  # Order Information page
def orders(num):
	myOrder = dbmanager.getOrder(num)

	name = myOrder.getName()
	phone = myOrder.getPhone()
	address = myOrder.getAddress()
	item = myOrder.getItem()
	notes = myOrder.getNotes()

	status = myOrder.isApproved()
	if (status == True):  # Generate a simple string value based on approval
		status = "Approved"
	else:
		status = "Approval Pending"

	if (" " in phone):
		phone = phone.replace(" ", "")


	return render_template(
		'orders.htm',
		num=num,
		name=name,
		phone=phone,
		address=address,
		item=item,
        notes=notes,
		status=status)


@app.route("/donate/approve/<number>")  # Page after order is approved
def approveDonation(number):
	dbmanager.approveOrder(number)
	return redirect(url_for('success'))


@app.route(
    '/signup/process',
    methods=["POST", "GET"])  # Process data submitted through sign-up form
def signupprocessor():
	if request.method == "POST":  # Get all the data
		name = request.form['name']
		email = request.form['email']
		phone = request.form['areaCode']+request.form['phone']
		
		dbmanager.addNGO(name, email, phone)

	return redirect(url_for('success'))


@app.route('/success')  # This will display the success message and redirect to the home page
def success():
	return render_template('success.htm')



if __name__ == "__main__":  # Start the web server...
	app.run(
	    host="0.0.0.0", port=5000
	)  # Flask only supports 1 request at a time but this can be increased
	# by integrating it with a production deployment web server like apache or nginx
