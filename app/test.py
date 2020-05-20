from model import model


ml_model = model(20, 12)
ml_model.restore_model("models/model_10_weights")

input_window = [1.0	,0.62,	0.81,	0.43,	0.82,	0.53,	0.92,	0.25,	0.66,	0.0]

input_window = ml_model.prepare_prediction_data(input_window)
pattern = ml_model.predict_pattern(input_window)

print(pattern[0].tolist())
