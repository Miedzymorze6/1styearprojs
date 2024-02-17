import tensorflow as tf
from tensorflow import keras
import numpy as np
import math
import random

def create_model(input_shape):
    model = keras.Sequential([
        keras.layers.Dense(8, activation='relu', input_shape=(input_shape,), name='input_layer'),
        keras.layers.Dense(4, activation='relu', name='hidden_layer'),                                        #neural network 8x4x1 :/
        keras.layers.Dense(1, activation='sigmoid', name='output_layer')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def should_colonize_neural_network(total_risk, sephi_value, trained_model):
    input_data = np.array([[total_risk, sephi_value]])
    prediction = trained_model.predict(input_data)                      #descision making part for should colonize or not
    return prediction[0, 0] >= 0.5

def generate_colonization_dataset(num_samples):
    np.random.seed(random.randint(1, 1000))
    features = np.random.rand(num_samples, 3)                          #random data for training

    for i in range(num_samples):
        total_risk = np.random.uniform(0, 1)
        sephi_value = np.random.choice([0.3, 0.45, 0.6, 0.75, 1.0])  # Random SEPHI levels
        features[i, 2] = 1 if total_risk <= 0.45 and sephi_value >= 0.8 else 0

    return features

def train_and_save_model(features, model_filename):
    input_shape = features.shape[1] - 1
    model = create_model(input_shape)                                     #train and save
    model.fit(features[:, :-1], features[:, -1], epochs=1000, batch_size=32, validation_split=0.2) #set epochs to 0 if you want to stop training.
    model.save(model_filename)
    print(f"Model saved to {model_filename}")

def likelihood_telluric(rp):    #L1
    rp_100 = rp * 0.97
    rp_50 = rp * 1.2
    sigma_telluric = (rp_50 - rp_100) / 3.0
    if rp <= rp_100:
        return 1.0
    elif rp_100 < rp < rp_50:
        return math.exp(-0.5 * ((rp - rp_100) / sigma_telluric) ** 2)
    else:
        return 0.0

def likelihood_atmosphere_gravity(ve):   #L2
    sigma_1 = 1.0 / 3.0
    sigma_2 = (8.66 - 1) / 3.0
    if ve < 1:
        return math.exp(-0.5 * ((ve - 1) / sigma_1) ** 2)
    elif ve >= 1:
        return math.exp(-0.5 * ((ve - 1) / sigma_2) ** 2)

def likelihood_surface_water(a, D1, D2, D3, D4):       #L3
    sigma_inner = (D2 - D1) / 3.0
    sigma_outer = (D4 - D3) / 3.0
    if a < D1:
        return 0.0
    elif D1 <= a < D2:
        return math.exp(-0.5 * ((a - D2) / sigma_inner) ** 2)
    elif D2 <= a <= D3:
        return 1.0
    elif D3 < a <= D4:
        return math.exp(-0.5 * ((a - D3) / sigma_outer) ** 2)
    else:
        return 0.0

def likelihood_magnetic(moment):            #L4
    sigma_magnetic = 0.333
    if moment < 1:
        return math.exp(-0.5 * ((moment - 1) / sigma_magnetic) ** 2)
    elif moment >= 1:
        return 1.0


def calculate_sephi(rp, ve, a, moment):         #final calculation for sephi
    likelihood_telluric_value = likelihood_telluric(rp)
    likelihood_atmosphere_gravity_value = likelihood_atmosphere_gravity(ve)
    likelihood_surface_water_value = likelihood_surface_water(a, D1_obj, D2_obj, D3_obj, D4_obj)
    likelihood_magnetic_value = likelihood_magnetic(moment)
    sephi_value = (likelihood_telluric_value * likelihood_atmosphere_gravity_value *
                   likelihood_surface_water_value * likelihood_magnetic_value) ** (1 / 4)
    global backup
    backup = sephi_value
    return sephi_value


def calculate_anomaly_score(weight_anomaly):              #anomaly calculator
    print("Set of anomalies that could be included in calculation - Unstable Geology, Unstable orbit, Unstable Host star, Toxic, Moon-moon ")
    l = int(input("Please enter the number of anomalies: "))
    anomalies = [input("Please list down anomalies and their severity from scale 1-3 (1 being low while 3 is high severity) (input format -> Toxic-1): ").split('-') for _ in range(l)]
    total_risk = sum(weight_anomaly.get(anomaly, 0) * int(severity) for anomaly, severity in anomalies)
    return total_risk

def get_input(prompt, default=None):
    value = input(prompt)
    return float(value) if value else default

num_samples = 1000
colonization_dataset = generate_colonization_dataset(num_samples)                       #model sample for colonization
np.savetxt("colonization_datasetAAAA.csv", colonization_dataset, delimiter=",")
train_and_save_model(colonization_dataset, "colonization_trainedAAAA_model.h5")
loaded_model = keras.models.load_model("colonization_trainedAAAA_model.h5")

weight_anomaly = {'Unstable Geology': 0.39, 'Unstable orbit': 0.39, 'Unstable Host Star': 0.52, 'Toxic': 0.09,
                  'Moon-Moon': 0.5}
total_risk = calculate_anomaly_score(weight_anomaly)
objekt = input("Enter the name of the object - ")
D1_obj = get_input(f"Enter the inner boundary for surface water for Host star of {objekt}: (0.75 for Sun)")
D2_obj = get_input(f"Enter the inner transition boundary for surface water for Host star of {objekt}: (0.95 for Sun)")
D3_obj = get_input(f"Enter the outer transition boundary for surface water for Host star of {objekt}: (1.68 for Sun)")
D4_obj = get_input(f"Enter the outer boundary for surface water for Host star of {objekt}: 1.77 for Sun)")
v_e = get_input(f"Enter escape velocity (in km/s) for {objekt}: ")
v_e /= 11.19
a = get_input(f"Enter Orbital Semi-Major axis for {objekt} (Relative to Earth): ")                          #inputs
moment = get_input(f"Enter Magnetic moment for {objekt} (Relative to Earth: ")
r = get_input('Please enter mean radius of body below (in Kilometers): ')
r /= 6371
sephi_value = calculate_sephi(r, v_e, a, moment)
colonize_neural_network = should_colonize_neural_network(total_risk, sephi_value, loaded_model)
sephi_value = backup

def classify_colonization_neural_network(total_risk, sephi_value):
    sephi_vals = {0: 'Too Low', 0.3: 'Low', 0.45: 'Average', 0.6: 'Above Average', 0.75: 'High', 1: 'Outstanding'}
    risk_vals = {0: 'None', 0.25: 'Low', 0.5: 'Average', 0.75: 'High'}
    final0 = 'Unknown'
    for i, label in sephi_vals.items():
        if sephi_value < i:
            final0 = label
            break

    final1 = 'Unknown'
    for i, label in risk_vals.items():
        if total_risk < i:
            final1 = label
            break

    return final0, final1

result_sephi, result_risk = classify_colonization_neural_network(total_risk, sephi_value)
sephi_value = backup
print("SEPHI Score: {}({}) Risk Level: {} for planet {} for colonization".format(sephi_value, result_sephi, result_risk, objekt))
def classify_suitability(sephi_value, risk_level):
    suitability_scale = {
        ('Too Low', 'High'): 'Unsuitable',
        ('Too Low', 'Average'): 'Unsuitable',
        ('Too Low', 'Low'): 'Unsuitable',
        ('Too Low', 'None'): 'Unsuitable',                 #manual classifiers for results
        ('Low', 'None'): 'Less Unsuitable',
        ('Low', 'Low'): 'Unsuitable',
        ('Low', 'Average'): 'Unsuitable',
        ('Low', 'High'): 'Unsuitable',
        ('Average', 'None'): 'Suitable',
        ('Average', 'Low'): 'Less Suitable',
        ('Average', 'Average'): 'UnSuitable',
        ('Average', 'High'): ' Unsuitable',
        ('Above Average', 'None'): 'Suitable',
        ('Above Average', 'Low'): 'Suitable',
        ('Above Average', 'Average'): 'Less Suitable',
        ('Above Average', 'High'): 'Unsuitable',
        ('High', 'None'): 'Suitable',
        ('High', 'Low'): 'Suitable',
        ('High', 'Average'): 'Less Suitable',
        ('High', 'High'): 'Unsuitable',
        ('Outstanding', 'None'): 'Totally Suitable',
        ('Outstanding', 'Low'): 'Totally Suitable',
        ('Outstanding', 'Average'):  'Suitable',
        ('Outstanding', 'High'): 'Less Suitable'
    }
    chkr = suitability_scale[(sephi_value, result_risk)]
    return chkr

result_sephi, result_risk = classify_colonization_neural_network(total_risk, sephi_value)
suitability = classify_suitability(result_sephi, result_risk)

print("SEPHI Score: {}, Risk Level: {} for planet {} for colonization".format(result_sephi, result_risk, objekt))
print("Suitability: {}".format(suitability))                                                                        #output
print('{} might be {} for colonization.'.format(objekt, suitability))
