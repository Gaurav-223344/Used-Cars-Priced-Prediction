from flask import Flask, render_template, request
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('xgboost_model.pkl', 'rb'))

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Location = str(request.form['location'])
        Kilometers_Driven = int(request.form['kilometers'])
        Fuel_Type = str(request.form['fuel'])
        Owner_Type = str(request.form['ownership'])
        Seats = int(request.form['seats'])
        Mileage_mean = float(request.form['mileage'])
        Engine_mean = int(request.form['engine'])
        Power_mean = float(request.form['power'])
        Purchase_Price = request.form['purchase']
        Car_Name = str(request.form['car_name'])
        if (Purchase_Price == 'yes'):
            Purchase_Price_ide = 1
        else:
            Purchase_Price_ide = 0
            
        Year = int(request.form['year'])
        Old = 2021 - Year
        
        Transmission = request.form['transmission']
        
        if (Transmission == 'Manual'):
            Manual = 1
        else:
            Manual = 0
        
        data = pd.DataFrame([[Location, Kilometers_Driven, Fuel_Type, Owner_Type, Seats, Car_Name, Mileage_mean, Engine_mean, Power_mean, Purchase_Price_ide, Old, Manual ]],
                            columns=['Location', 'Kilometers_Driven', 'Fuel_Type', 'Owner_Type', 'Seats', 'Car_Name', 'Mileage_mean', 'Engine_mean', 'Power_mean', 'Purchase_Price_ide', 'Old', 'Manual' ])
        
        dict_loc = {'Ahmedabad': 7.949576719576723,
                    'Bangalore': 13.895409252669035,
                    'Chennai': 7.827617866004969,
                    'Coimbatore': 14.971643835616439,
                    'Delhi': 9.664243792325049,
                    'Hyderabad': 9.955796610169477,
                    'Jaipur': 5.763577981651374,
                    'Kochi': 11.513287401574804,
                    'Kolkata': 5.432844036697246,
                    'Mumbai': 8.97049128367669,
                    'Pune': 6.5998790322580625}
        
        data['Location'] = data['Location'].map(dict_loc)
        
        dict_fuel = {'CNG': 3.4895652173913048,
                     'Diesel': 12.797961658841997,
                     'Electric': 12.75,
                     'LPG': 2.492857142857143,
                     'Petrol': 5.669419501133777}
        
        data['Fuel_Type'] = data['Fuel_Type'].map(dict_fuel)
        
        dict_of_OwnerType = {'Fourth & Above' : 0, 'Third' : 1, 'Second' : 2, 'First' : 3}

        data['Owner_Type'] = data['Owner_Type'].map(dict_of_OwnerType)
        
        dict_name = {'Ambassador': 1.35,
                     'Audi': 25.687647058823522,
                     'BMW': 24.76417040358744,
                     'Bentley': 59.0,
                     'Chevrolet': 3.109807692307693,
                     'Datsun': 2.9436363636363634,
                     'Fiat': 3.4745454545454537,
                     'Force': 9.333333333333334,
                     'Ford': 6.801526104417671,
                     'Honda': 5.353683168316831,
                     'Hyundai': 5.350570776255696,
                     'Isuzu': 14.0,
                     'Jaguar': 38.480588235294114,
                     'Jeep': 18.320833333333336,
                     'Lamborghini': 120.0,
                     'Land': 37.474199999999996,
                     'Mahindra': 8.055000000000001,
                     'Maruti': 4.484635897435896,
                     'Mercedes': 26.49607999999999,
                     'Mini': 28.215238095238096,
                     'Mitsubishi': 9.568499999999998,
                     'Nissan': 4.806266666666667,
                     'Porsche': 44.31545454545455,
                     'Renault': 5.762000000000002,
                     'Skoda': 7.601164383561648,
                     'Smart': 3.0,
                     'Tata': 3.434,
                     'Toyota': 11.475490797546001,
                     'Volkswagen': 5.412796934865907,
                     'Volvo': 18.652142857142856}
        
        data['Car_Name'] = data['Car_Name'].map(dict_name)
        
        scaler = StandardScaler()
        
        df = pd.read_csv('X_new.csv',usecols = ['Location', 'Kilometers_Driven', 'Fuel_Type', 'Owner_Type', 'Seats', 'Car_Name', 'Mileage_mean', 'Engine_mean', 'Power_mean', 'Purchase_Price_ide', 'Old', 'Manual' ])

        scaler.fit(df)
        data_new = scaler.transform(data)
        data_new = pd.DataFrame(data_new,columns=data.columns)
        
        prediction = model.predict(data_new)
        output=prediction[0]
        if output<=0:
            return render_template('index.html',prediction_texts="Please enter correct information")
        else:
            return render_template('index.html',prediction_texts=f"Price = {output}")
    
        
        
    else:
        return render_template('index.html')

    
    
if __name__=="__main__":
    app.run(debug=True)  
#if __name__=="__main__":
#    app.run(host='0.0.0.0',port=8080)
        