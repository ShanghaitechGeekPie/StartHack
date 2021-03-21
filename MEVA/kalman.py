from pykalman import KalmanFilter
import joblib
import numpy as np


def Kalman(observations,damping=1):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
            initial_state_mean=initial_value_guess,
            initial_state_covariance=observation_covariance,
            observation_covariance=observation_covariance,
            transition_covariance=transition_covariance,
            transition_matrices=transition_matrix
        )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state


res = joblib.load("meva_output_dammit.pkl")

verts = []

for item in res:
    verts.append(item['verts'])
verts = np.array(verts)
verts = np.transpose(verts, [1, 2, 0])
for i in range(6890):
    for j in range(3):
        verts[i][j] = np.squeeze(Kalman(verts[i][j], 0.1), axis=1)