import json
import os
from flask import Flask ,render_template,request
import pickle
import numpy
import pandas as pd
import csv

import csv

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])


def home():
	if request.method=="POST":
		f=None
		model=None
		try:
			f=open("Creditcard.model","rb")
			model=pickle.load(f)
		except Exception as e:
			print("Issue",e)
		finally:
			if f is not None:
				f.close()

		if model is not None:
			up_data = request.files.get('file')
			data = []
			messages = []
			i=0
			if up_data:
				for row in up_data:
					values = row.decode().strip().split(",")
					row_data = [float(val) for val in values]
					i=i+1
					data.append(row_data)
					pred = model.predict([row_data])
					print(pred)
					if pred == 0:
						msg = "Legititimate Transaction"
					else:
						msg = "Fraudulent Transaction"
					#msg = " Legitimate Transaction " if pred == '0' else  "  Fraudulent Transaction"
					messages.append(str(i)+ "]   Transaction is: " + msg + "<br>")
			return render_template("index.html", msg='\n'.join(messages))
		else:
			print("Model issue")
			return render_template("index.html", msg="Model issue")
	else:
		return render_template("index.html")
			

if __name__ == "__main__" :
	app.run(debug=True,use_reloader=True)

