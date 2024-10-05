from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd
import MySQLdb
import datetime
import weathertest as wt


app = Flask(__name__)
model = pickle.load(open("c1_flight_rf.pkl", "rb"))
mydb = MySQLdb.connect(host='localhost',user='root',passwd='root',db='airline')
conn = mydb.cursor()
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
@cross_origin()
def index():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return render_template('home.html')
@app.route('/notebook',methods=['GET','POST'])
def notebook():
    return render_template("notebook.html")
@app.route('/register',methods=['POST'])
def reg():
    name=request.form['name']
    cid=request.form['cid']
    pin=request.form['pin']
    email=request.form['emailid']
    mobile=request.form['mobile']
    cmd="SELECT * FROM login WHERE cid='"+cid+"'"
    print(cmd)
    conn.execute(cmd)
    cursor=conn.fetchall()
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        print("name Already Exists")
        return render_template("login.html",message="User name id Already Exists")
    else:
        print("insert")
        cmd="INSERT INTO login Values('"+str(cid)+"','"+str(name)+"','"+str(pin)+"','"+str(email)+"','"+str(mobile)+"')"
        print(cmd)
        print("Inserted Successfully")
        conn.execute(cmd)
        mydb.commit()
        return render_template("login.html",message="Inserted SuccesFully")
@app.route('/login',methods=['POST'])
def log_in():
    if request.form['cid'] != None and request.form['cid'] != "" and request.form['pin'] != None and request.form['pin'] != "":
        cid=request.form['cid']
        pin=request.form['pin']
        cmd="SELECT cid,pin,email FROM login WHERE cid='"+cid+"' and pin='"+pin+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
            if(isRecordExist==1):
                session['logged_in'] = True
                session['cid'] = request.form['cid']
                return redirect(url_for('index'))
            else:
                return render_template("login.html",message="Check user name id and password")

    return redirect(url_for('index'))

@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        dep_hour = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        arrival_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Duration_hour = abs(arrival_hour - dep_hour)
        Duration_mins = abs(arrival_min - dep_min)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_Stops = int(request.form["stops"])
        # print(Total_stops)



        airline=request.form['airline']
        if(airline=='Jet Airways'):
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif (airline=='IndiGo'):
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 1
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif (airline=='Air India'):
            Airline_AirIndia = 1
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
            
        elif (airline=='Multiple carriers'):
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0
            
        elif (airline=='SpiceJet'):
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_Vistara = 0
            Airline_Other = 0
            
        elif (airline=='Vistara'):
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 1
            Airline_Other = 0

        elif (airline=='GoAir'):
            Airline_AirIndia = 0
            Airline_GoAir = 1
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        else:
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 1


        Source = request.form["Source"]
        if (Source == 'Delhi'):
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0

        elif (Source == 'Kolkata'):
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0

        elif (Source == 'Mumbai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0

        elif (Source == 'Chennai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1

        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0



        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            Destination_Cochin = 1
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
        
        elif (Source == 'Delhi'):
            Destination_Cochin = 0
            Destination_Delhi = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        elif (Source == 'Hyderabad'):
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0

        elif (Source == 'Kolkata'):
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1

        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0


        prediction=model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            Duration_hour,
            Duration_mins,
            Airline_AirIndia,
            Airline_GoAir,
            Airline_IndiGo,
            Airline_JetAirways,
            Airline_MultipleCarriers,
            Airline_Other,
            Airline_SpiceJet,
            Airline_Vistara,
            Source_Chennai,
            Source_Kolkata,
            Source_Mumbai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata,
        ]])

        output=round(prediction[0],2)
        format_str = '%Y-%m-%dT%H:%M'
        print("date_dep==",date_dep)
        print("date_arr==",date_arr)

        #datetime_obj1 = datetime.datetime.strptime(date_dep, format_str)
        #datetime_obj2=datetime.datetime.strptime(date_arr,format_str)

        condition=wt.process(Source,date_dep,date_arr)
        output1=0
        if "snow" in condition or "Snow" in condition:
            output1=output-100
        elif "rain" in condition or "Rain" in condition:
            output1=output-200
        elif "strom" in condition or "Strom" in condition:
            output1=output-300
        elif "cloud" in condition or "Cloud" in condition:
            output1=output-50
        else:
            output1=output
        
        
        

        

        return render_template('home.html',prediction_text="Your Flight actual price is Rs. {}".format(output),output1="Your Flight Price based on Weather is Rs."+str(output1)+" due to "+str(condition))


    return render_template("home.html")

@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for('index'))
    


if __name__ == '__main__':
    socketio.run(app,debug=True,host='127.0.0.1', port=5000)
