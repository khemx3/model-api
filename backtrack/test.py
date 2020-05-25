from modelapi.model import model


ml_model = model(20, 12)
ml_model.restore_model("models/model_1_weights")

input_window = [34.54,	36.2,	37.57,	36.81,	37.16,	36.73,	36.27,	36.2,	36.84,	38.495]

input_window = ml_model.prepare_prediction_data(input_window)
pattern = ml_model.predict_pattern(input_window)

print(pattern[0].tolist())
