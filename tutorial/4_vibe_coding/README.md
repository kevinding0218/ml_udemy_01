# Customer purchase prediction

Train a binary classifier using the dataset's `Age` and `Salary` columns to
predict `Purchased` (0 = no, 1 = yes). The model is a logistic regression
pipeline with standardized inputs.

## Setup and run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python train_model.py
python predict.py 35 50000
python app.py
```

Training reports holdout metrics, then fits on the full dataset and saves
`model/purchase_model.joblib`. Pass age and salary as positional inputs to
`predict.py`; it prints the predicted outcome and estimated purchase
probability. Re-run training if you change the CSV.

## Local REST API

Start the Flask API after training:

```bash
python app.py
```

The server listens at `http://127.0.0.1:5000`. Check `GET /health`, or send
age and salary as JSON to `POST /predict`:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "salary": 50000}'
```

The response includes the predicted class (`1` = purchase, `0` = no purchase),
a boolean outcome, and the estimated purchase probability. Invalid or missing
inputs return HTTP 400 with an error message.

Open `http://127.0.0.1:5000` in your browser to use the web form. It submits
the entered age and salary to the local prediction API and displays the result.

## GitHub Pages (organization-only)

The static Pages version runs prediction in the browser, so it does not need a
hosted Flask API and does not send entered ages or salaries to a server. It
needs a small JSON export of the trained model:

```bash
python export_web_model.py
```

For organization-only access, the repository must be owned by your organization
and your GitHub plan must support private Pages access. In the organization
repository, first set **Settings → Pages → Build and deployment → Source** to
**GitHub Actions**, and restrict site visibility to organization members in
**Settings → Pages → Visibility**. Then run the
**Publish customer predictor Pages site** workflow from the Actions tab. The
workflow is manual to avoid publishing the page before its access restriction
has been configured.

The current repository is under the personal account `kevinding0218`, so it
must be moved or copied to the organization repository before organization-only
Pages access can be configured.
