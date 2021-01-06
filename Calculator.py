import math, csv, json
from flask import Flask, redirect, url_for, render_template,request

'''
Cummings and Finn - 1RM (kg) = 1.175 RepWt + 0.839 Reps –4.29787
rep_intensity = {'1':100,'2':95,'3':93,'4':90,'5':87,'6':85,'7':83,'8':80,'9':77,'10':75,'11':73,'12':70}
'''

def one_rep_max(reps, weight):
	rm = weight / ( 1.0278 - 0.0278 * reps )
	return rm

'''
realtive intensity - takes the weight you did for a number of reps dividedby the highest weight you could do at that rep range
'''

def relative_intensity(reps,weight,one_rm):
	max_weight = one_rm * (1.0278 - 0.0278 * reps)
	ai = (weight) / one_rm
	ri = ai / (max_weight / one_rm)
	return (ai,ri)

'''
it is recomended to increase intensity roughly 5% every week. This means that the sets and reps can change but the intensity
should fit a steady progress of 5%. We want to be able to plan this out.
'''

def increased_ai(reps, desired_ri):
	mi =  (1.0278 - 0.0278 * reps)
	new_ai = math.floor(mi * (desired_ri))/100
	return new_ai

def addMax(exercise, weight, file):
    with open(file, "r") as read_file:
        saved = json.load(read_file)
        
    new = {exercise : weight}
    saved.update(new)
    
    with open(file, "w") as write_file:
        json.dump(saved, write_file, indent = 4, sort_keys = True, separators = (",",":"))

'''
getting the web page up and running. Allows for a one_rep max to be determined, relative intensity, and what
actual intensity should be used. Will have fields that need to be filled and spaces for data to be returned.
'''

app = Flask(__name__)

@app.route('/', methods = ["POST","GET"])
def max():
	if request.method == "POST":
		try:
			weight = int (request.form['weight'])
			reps = int (request.form['reps'])
			rm = one_rep_max(reps,weight)
			rm = int (rm)
		except:
			rm = 'numbers please'
	else:
		rm = ""
	return render_template("max.html", rm = rm)

@app.route('/plan/', methods = ['POST', 'GET'])
def plan():
	if request.method == "POST":
		try:
			weight = int (request.form['weight'])
			reps = int (request.form['reps'])
			rm = int (request.form['1RM'])
			i = relative_intensity(reps,weight,rm)
			ri = str (int (i[1] * 100)) + "%"
			ai = str (int (i[0] * 100)) + "%"
		except:
			ri = ""
			ai = ""
		
		try:
			repsI = int (request.form['repsI'])
			relI = int (request.form['relI'])
			new_ai = (100 * increased_ai(repsI, relI))
			new_ai = str(new_ai) + "%"
		except:
			new_ai = ""
	else:
		ri = ""
		ai = ""
		new_ai = ""
	return render_template("plan.html", ri = ri, ai = ai, new_ai = new_ai)



@app.route('/tracker/', methods = ["POST","GET"])
def tracker():
	if request.method == "POST":
		try:
			weight = int (request.form['weight'])
			exercise = request.form['exercise']
			addMax(exercise,weight, "tracker.json")
		except:
			print ("error")
	else:
		rm = ""

	with open("tracker.json", "r") as read_file:
		workouts = json.load(read_file)
	return render_template("tracker.html", workouts = workouts)



# def add_user(csv_file,name,pswrd):
# 	accounts = open(csv_file,'a', newline='\n')
# 	obj = csv.writer(accounts)
# 	obj.writerow([name,pswrd])
# 	accounts.close()

# def exists(csv_file,name):
# 	with open(csv_file,'rt') as f:
# 		users = csv.reader(f)
# 		for user in users:
# 			if user[0] == name:
# 				return user
# 		return False


# def verify(csv_file, name, pswrd):
# 	profile = users.exists(csv_file,name)
# 	if len(profile) > 0:
# 		if profile[1] == pswrd:
# 			return True
# 	return False

# @app.route('/login/', methods=['POST','Get'])
# def login():
# 	if request.method=="POST":
# 		name = request.form['new_name']
# 		pswrd = request.form['new_pswrd']
# 		if exists('csv_tests/users.csv',name) == False:
# 			add_user('csv_tests/users.csv',name,pswrd)
# 	return render_template("login.html")

if __name__ == "__main__":
	app.run(debug = True)

