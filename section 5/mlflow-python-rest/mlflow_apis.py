

import mlflow

mlflow.tracking.set_tracking_uri("http://127.0.0.1:5000/")

print(mlflow.tracking.get_tracking_uri())

experiment = mlflow.get_experiment("633010643391764265")
print("Name: {}".format(experiment.name))

experiment_id = mlflow.get_experiment_by_name("futurexskill mlflow demo 4")
print("ID: {}".format(experiment_id))

with mlflow.start_run(run_name = "new-run1-10") as run5:
    last_run = mlflow.last_active_run().info.run_id
    print("last_run "+ last_run)