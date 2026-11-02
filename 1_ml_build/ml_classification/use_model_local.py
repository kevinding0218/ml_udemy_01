import pickle
import numpy as np

# =============================================================================
# APPROACH A: two separate files (classifier.pickle + sc.pickle)
# Use this if ml_pipeline.py saved them separately (current default)
# =============================================================================

classifier = pickle.load(open("classifier.pickle", "rb"))
sc         = pickle.load(open("sc.pickle", "rb"))

new_input = np.array([[40, 20000]])  # [age, salary] — same column order as training

prediction  = classifier.predict(sc.transform(new_input))
probability = classifier.predict_proba(sc.transform(new_input))[:, 1]

print(f"Prediction : {prediction[0]}  (1 = bought, 0 = didn't buy)")
print(f"Confidence : {probability[0]:.0%}")


# =============================================================================
# APPROACH B: single combined pipeline file (model.pickle)
# Use this if ml_pipeline.py was run with the pipeline option enabled.
# Scaler is baked in — no manual sc.transform() needed.
# =============================================================================

# pipe = pickle.load(open("model.pickle", "rb"))
#
# new_input = np.array([[40, 20000]])  # [age, salary] — same column order as training
#
# prediction  = pipe.predict(new_input)
# probability = pipe.predict_proba(new_input)[:, 1]
#
# print(f"Prediction : {prediction[0]}  (1 = bought, 0 = didn't buy)")
# print(f"Confidence : {probability[0]:.0%}")
