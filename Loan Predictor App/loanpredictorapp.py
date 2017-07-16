"""App that lets you input loan information and get a response about whether you should invest in the loan or not.
App uses logistic regression and is set to return a result based on the probability that it shoots out. The logistic regression model is a
simpler version of the app I used in my presentation and uses only the 7 best features.
App is set to say to invest only if probability passes 70%...this setting gives roughly 95% precision """


from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, DecimalField
app = Flask(__name__)
from sklearn.linear_model import LogisticRegression
import numpy as np
import pickle

from wtforms import validators, ValidationError
app.secret_key = "dogs"
LR = pickle.load( open( "alg.pkl", "rb" ) )

#this creates the form to fill loan information in
class ContactForm(Form):
	LoanAmount = IntegerField("Loan Amount",[validators.InputRequired("Please enter.")])
	Term = IntegerField("Loan Length (in payments)", [validators.InputRequired("Please enter.")])
	InterestRate = DecimalField("Interest Rate", [validators.InputRequired("Please enter.")])

	AnnualIncome = IntegerField("Annual Income", [validators.InputRequired("Please enter.")])
	inquiries = DecimalField("Inquiries in the Last 6 Months", [validators.InputRequired("Please enter.")])
	dti = DecimalField("Debt to Income Ratio", [validators.InputRequired("Please enter.")])
	revol_util = DecimalField("Revolving Line Utilization", [validators.InputRequired("Please enter.")])
	submit = SubmitField("$$$$$$")


@app.route('/', methods = ['GET', 'POST'])
def index():
	form = ContactForm()

	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('index.html', form = form, answer="")
		else:
		
			response = [int(request.form["LoanAmount"]), int(request.form["Term"]),float(request.form["InterestRate"]), int(request.form["AnnualIncome"]), float(request.form["inquiries"]), float(request.form["dti"]), float(request.form["revol_util"])]
			if LR.predict_proba(response)[:, 1] > .7:
				answer = "Go For It!!!"
				return render_template('index.html', form = form, answer=answer)
			elif LR.predict_proba(response)[:,1] <= .7:
				answer = "Stay Way!!!!"
				return render_template('index.html', form = form, answer=answer)
			# else:
			# 	answer = "other"
			# 	return render_template('index.html', form = form, answer=answer)


	elif request.method == 'GET':
		return render_template('index.html', form = form, answer="")

if __name__ == '__main__':
	app.run(debug = True)