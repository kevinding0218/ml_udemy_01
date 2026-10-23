# KNN Classification Pipeline — Notes

---

# Part 1: Concepts

Key terms used in this example and throughout ML classification.

---

## Features and Label

| Term | Also called | Your example |
|---|---|---|
| **Feature** | Input, predictor, independent variable | Age, salary |
| **Label** | Target, output, dependent variable | Bought (1) or not (0) |

Features are the input columns you feed into the model. The label is what you're asking the model to predict.

```python
X = training_data.iloc[:, :-1].values  # all columns except last → features
y = training_data.iloc[:, -1].values   # last column → label
```

When predicting a new person: you supply the features, the model returns the label.

```python
classifier.predict(sc.transform(np.array([[40, 20000]])))
#                                          ^^   ^^^^^
#                                         age  salary  ← features you know
#                                                         label = model's guess
```

---

## Train/Test Split (X_train, X_test, y_train, y_test)

When you split your data, both X and y get split — because you need the correct answers for the test portion too, so you can measure how well the model did.

Think of it like a practice exam vs a final exam:

| Variable | What it is | Used for |
|---|---|---|
| `X_train` | Input features, training portion | Fed to the model so it can learn |
| `y_train` | Correct answers, training portion | The model studies these during training |
| `X_test` | Input features, test portion | Given to the trained model to predict |
| `y_test` | Correct answers, test portion | Compared against the model's predictions to measure accuracy |

`y_test` is hidden from the model during training. After training, you ask the model to predict on `X_test`, then compare `y_pred` (what it guessed) against `y_test` (the real answers):

```
Training phase:   model sees X_train + y_train → learns patterns
Testing phase:    model sees X_test only        → makes predictions (y_pred)
Evaluation:       compare y_pred vs y_test      → accuracy score
```

If you tested on the same data you trained on, you'd get artificially high accuracy — the model already memorized those answers. A separate test set tells you how it performs on data it has never seen, which is what matters in real life.

---

## When to use classification — and when not to

Classification assumes two things that aren't always true:

1. **The output is one of a fixed, known set of values** (e.g., card_id is always one of 500 known IDs)
2. **The input vocabulary is known ahead of time** (e.g., card names are always from a list you've seen before)

When either assumption breaks down, a classifier is the wrong tool.

### Decision guide

| Your situation | Right tool |
|---|---|
| Output is one of a known set of labels | **Classification** (KNN, Random Forest, etc.) |
| Output is a number on a continuous scale (price, temperature) | **Regression** |
| Input text varies slightly — typos, abbreviations | **Fuzzy matching** to normalize → then classify |
| Input text is open-ended, no known vocabulary | **Text embeddings + semantic search** |
| No labels at all — just find groups in data | **Clustering** (unsupervised learning) |

### The open vocabulary problem

Label encoding and one-hot encoding both require knowing all possible values upfront — a **closed vocabulary**. If a client can send any string and you have no predefined list to map it to, encoding breaks.

The solution is **text embeddings**: instead of assigning an arbitrary number from a fixed list, embeddings convert any text into a numeric vector based on *meaning*. They're pre-trained on large text datasets, so they understand similarity without needing a lookup table.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

model.encode("Charizard")  # → [0.12, -0.34, 0.87, ...]
model.encode("Chariz")     # → [0.11, -0.33, 0.85, ...]  ← very similar
model.encode("Blastoise")  # → [0.45,  0.21, -0.12, ...] ← very different
```

With embeddings, "Chariz" and "Charizard" are close in vector space even if "Chariz" was never in training data — because the model understands their textual similarity.

### Classification vs semantic search

If the input is truly unconstrained and you have no fixed output list, you're not doing classification — you're doing **retrieval**:

- **Classification** answers: *"which known bucket does this belong to?"*
- **Semantic search** answers: *"what does this most resemble in my database?"*

Semantic search uses embeddings + vector similarity (cosine distance) to find the closest match in a database — no fixed label list required. This is a different architecture (vector databases, similarity search) and a different ML domain.

Knowing which problem you actually have is more important than knowing which algorithm to use.

---

## KNN (K-Nearest Neighbors)

KNN is a classification algorithm that makes predictions by finding the K most similar training examples and taking a majority vote.

**How it works:**
1. You have training data — rows of (features, label) pairs the model has already seen
2. A new person comes in with their feature values
3. KNN computes the distance between that person and every training row
4. It picks the K closest rows (the "neighbors")
5. It counts which label appears most among those K neighbors — that's the prediction

**In your code:** `n_neighbors=5` means it looks at the 5 closest people and takes a majority vote.

**Distance formula (Euclidean, p=2):**
```
distance = sqrt((a1-b1)² + (a2-b2)² + ... + (aN-bN)²)
```

This is why feature scaling matters — see Part 2.

---

## Confusion Matrix

Accuracy alone tells you "how often was the model right?" but not *where* it went wrong. The confusion matrix breaks predictions into four buckets.

```
                  Predicted: 0        Predicted: 1
Actual: 0      True Negative (TN)   False Positive (FP)
Actual: 1      False Negative (FN)  True Positive (TP)
```

| Term | What happened | Store example |
|---|---|---|
| **True Positive (TP)** | Predicted bought, actually bought | Correctly identified a buyer |
| **True Negative (TN)** | Predicted didn't buy, actually didn't | Correctly ignored a non-buyer |
| **False Positive (FP)** | Predicted bought, actually didn't | Wasted a marketing offer |
| **False Negative (FN)** | Predicted didn't buy, actually did | Missed a real buyer |

### Metrics from the confusion matrix

| Metric | Formula | What it answers |
|---|---|---|
| **Accuracy** | (TP + TN) / total | What % of all predictions were correct? |
| **Precision** | TP / (TP + FP) | Of all flagged buyers, how many really were? |
| **Recall** | TP / (TP + FN) | Of all real buyers, how many did we catch? |
| **F1 Score** | 2 × (Precision × Recall) / (Precision + Recall) | Balance between precision and recall |

### Which metric matters?

It depends on which mistake is more costly:

- **Missing a real buyer (FN) is costly** → prioritize **Recall** (e.g., medical diagnosis — better to over-flag than miss a disease)
- **Flagging a non-buyer (FP) is costly** → prioritize **Precision** (e.g., fraud — don't block innocent users)
- **Both matter equally** → use **F1 Score**

Your code computes all of these:
```python
confusion_matrix(y_test, y_pred)       # raw matrix
accuracy_score(y_test, y_pred)         # accuracy
classification_report(y_test, y_pred)  # precision, recall, F1 per class
```

---

## Confidence Score (predict_proba)

The model's label output is binary (0 or 1). But `predict_proba` also exposes how confident the model is.

### What the output looks like

`predict_proba` returns a 2D array — one row per person, one column per class:

```python
classifier.predict_proba(X_test)
# → [[0.20, 0.80],   ← person 1: 20% chance didn't buy, 80% chance bought
#    [0.60, 0.40],   ← person 2: 60% didn't buy, 40% bought
#    [0.00, 1.00],   ← person 3: 0% didn't buy, 100% bought
#    [0.80, 0.20]]   ← person 4: 80% didn't buy, 20% bought

classifier.predict_proba(X_test)[:,1]
# → [0.80, 0.40, 1.00, 0.20]  ← class-1 probability only, one number per person
```

`[:,1]` means: all rows, column index 1 (the "bought" probability). The two columns always sum to 1.0.

### How KNN calculates it

With `n_neighbors=5`, probability = fraction of the 5 neighbors that voted for each class. With k=5, the only possible values are:

| Neighbors voting "bought" | Probability | Prediction |
|---|---|---|
| 5 out of 5 | 1.00 | Bought |
| 4 out of 5 | 0.80 | Bought |
| 3 out of 5 | 0.60 | Bought |
| 2 out of 5 | 0.40 | Didn't buy |
| 1 out of 5 | 0.20 | Didn't buy |
| 0 out of 5 | 0.00 | Didn't buy |

There are no in-between values — with k=5 you only ever see these six numbers.

### Should you trust the prediction?

There are **no universal thresholds** — 0.8 doesn't automatically mean "trustworthy" in every situation. What matters is your use case:

- If acting on a wrong prediction is cheap (e.g., sending a discount email), even 0.6 might be good enough
- If acting on a wrong prediction is expensive (e.g., approving a loan), you might only act at 0.8+

In practice you can raise the decision threshold above 0.5:
```python
# Instead of defaulting to: predict label 1 whenever prob > 0.5
# You can require higher confidence:
threshold = 0.8
y_pred_strict = (y_prob >= threshold).astype(int)
```

This lowers recall (you'll miss more buyers) but raises precision (the buyers you do flag are more reliable).

---

## Saving and reusing a trained model (pickle)

Training is slow. You don't want to retrain every time you need a prediction. Pickle saves your trained Python objects to disk so you can load and reuse them later — in a different script, on a different machine, or by a teammate.

Your pipeline saves two files because prediction needs both:

```python
pickle.dump(classifier, open("classifier.pickle", "wb"))  # trained KNN model
pickle.dump(sc,         open("sc.pickle",         "wb"))  # fitted scaler
```

`"wb"` = write binary. Pickle files are binary, not plain text.

### Loading and predicting (predict_new.py)

```python
import pickle
import numpy as np

classifier = pickle.load(open("classifier.pickle", "rb"))
sc         = pickle.load(open("sc.pickle", "rb"))

new_input  = np.array([[40, 20000]])  # [age, salary] — same column order as training

prediction  = classifier.predict(sc.transform(new_input))
probability = classifier.predict_proba(sc.transform(new_input))[:, 1]

print(f"Prediction : {prediction[0]}  (1 = bought, 0 = didn't buy)")
print(f"Confidence : {probability[0]:.0%}")
```

`"rb"` = read binary.

**Why you must load both files:** the scaler memorized the averages and ranges from training data. If you scale the new input differently — or skip scaling — the numbers fed into the model won't match what it was trained on, and predictions will be wrong.

### Alternative: combine both into one file using Pipeline

Instead of two separate files, you can wrap the scaler and classifier into a single `Pipeline` object and save that as one file. Scaling is baked in — it can't be accidentally skipped.

In `ml_pipeline.py` (commented-out option at the bottom):
```python
from sklearn.pipeline import Pipeline

pipe = Pipeline([
    ('scaler',     StandardScaler()),
    ('classifier', KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2))
])
pipe.fit(X_train, y_train)
pickle.dump(pipe, open("model.pickle", "wb"))
```

In `predict_new.py` (switch to Approach B):
```python
pipe = pickle.load(open("model.pickle", "rb"))
prediction  = pipe.predict(np.array([[40, 20000]]))   # no sc.transform() needed
probability = pipe.predict_proba(np.array([[40, 20000]]))[:, 1]
```

Two files is how tutorials teach it (each piece is visible). One pipeline file is how you'd do it in production.

### Sharing pickle files with your team — version requirements

Pickle files are **not guaranteed to work across different Python or library versions**. When you hand the files to a teammate, they need to match:

| Requirement | Why it matters |
|---|---|
| **Same Python version** (e.g., 3.11.x) | Pickle protocol can differ across versions |
| **Same scikit-learn version** | The model object structure may change between releases |
| **Same numpy version** | Arrays serialized by one version may differ in another |

The safest way to share: include a `requirements.txt` with exact versions.

```bash
# Generate from your environment
pip freeze > requirements.txt
```

```bash
# Teammate installs the exact same versions
pip install -r requirements.txt
```

Then they run `predict_new.py` directly — no retraining needed.

---

# Part 2: Pipeline Deep Dives

How and why specific steps in `ml_pipeline.py` work the way they do.

---

## Why do we need feature scaling?

KNN computes distance between people using all feature columns at once. A column with large raw numbers will dominate the distance calculation and make other columns invisible — not because it's more important, but because its unit is bigger.

### Example: age vs salary

| | Age | Salary |
|---|---|---|
| Person A | 30 | $50,000 |
| Person B | 32 | $90,000 |

**Raw distance (before scaling):**
```
sqrt( (32-30)²  +  (90000-50000)² )
= sqrt(    4    +  1,600,000,000  )
≈ 40,000
```

- Age's share: 4 / 1,600,000,004 ≈ **0.000%** — completely invisible
- Salary's share: 1,600,000,000 / 1,600,000,004 ≈ **100%** — salary is everything

**After scaling** — each column is converted to the same unit (roughly -3 to +3):
- 2-year age gap → ~0.2 scaled units
- $40k salary gap → ~1.1 scaled units

Both live on the same ruler now. Salary still contributes more (it really is a bigger real-world gap), but age is no longer invisible.

### Is there a target split (50/50)?

No. The goal isn't equal shares — it's that each column's share reflects **genuine differences in the data**, not fake distortion from unit sizes.

### What does the distance number mean?

The absolute value (40,000 or 1.4) means nothing on its own. KNN never asks "is this too far?" — it just **ranks** all training points by distance and picks the closest K. It's always relative, never a threshold.

---

## When to use feature scaling (and when not to)

Scaling is not always needed — it depends on the algorithm, not on whether you're doing classification.

**The rule:** does the algorithm measure distance or use gradient descent? → Scale. Does it split data by threshold values? → Skip it.

| Algorithm | Needs scaling? | Why |
|---|---|---|
| KNN | Yes | Compares distances — bigger units dominate |
| SVM | Yes | Finds a margin based on distances |
| Logistic Regression | Yes | Gradient descent converges faster with similar-sized features |
| Neural Networks | Yes | Same reason as logistic regression |
| Decision Tree | No | Splits on thresholds ("salary > 50000") — the unit doesn't matter |
| Random Forest | No | Just a collection of decision trees |
| XGBoost / Gradient Boosting | No | Tree-based — invariant to scale |
| Naive Bayes | No | Works with probabilities, not distances |

Quick mental check before training: *"Does this algorithm compute distances or use gradient descent?"* → Scale. Tree-based? → Skip.

For example, if you swapped KNN for Random Forest in your pipeline, you could remove `StandardScaler` entirely and nothing would break.

---

## Why fit_transform on train but only transform on test?

```python
X_train = sc.fit_transform(X_train)  # learn scale from training, then apply
X_test  = sc.transform(X_test)       # apply the same scale, don't re-learn
```

Re-fitting on test data would leak future information into your scaling step. In real life you don't know the "average salary of all future customers" — you only know what you saw during training. The scaler must stay frozen after training.

---

## What to do when accuracy is low

### 1. Tune the number of neighbors (k)

`n_neighbors` is the most direct knob for KNN:

```python
for k in [1, 3, 5, 7, 9, 11]:
    clf = KNeighborsClassifier(n_neighbors=k, metric='minkowski', p=2)
    clf.fit(X_train, y_train)
    print(f"k={k}: {accuracy_score(y_test, clf.predict(X_test)):.3f}")
```

- Too small (k=1) → overfitting: model memorizes noise, fails on new data
- Too large → underfitting: model is too broad, misses real patterns
- Use odd numbers to avoid tie votes in binary classification

### 2. Check if the data is the problem

- **Too little data** — not enough examples to learn real patterns
- **Missing important features** — age and salary may not be enough; adding more columns can help
- **Class imbalance** — if 95% of rows are "didn't buy", a model that always says "didn't buy" gets 95% accuracy but is useless; check F1 score instead

### 3. Try a different algorithm

| Algorithm | Good when |
|---|---|
| Logistic Regression | Simple, interpretable, linear patterns |
| Random Forest | Works well out of the box, handles many features |
| SVM | Good with smaller datasets and clear margins |
| Gradient Boosting (XGBoost) | Often best accuracy on tabular data |

### 4. Use cross-validation for a fairer estimate

A single 80/20 split can get lucky depending on which rows land in the test set. Cross-validation repeats the split multiple times and averages the result:

```python
from sklearn.model_selection import cross_val_score
scores = cross_val_score(classifier, X_train, y_train, cv=5)
print(f"CV accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

If cross-validation accuracy is much lower than your single test accuracy, the model got a favorable split by chance.

---

# Part 3: Real-World Example — Trading Card Lookup

## The problem

You have a dataset of trading cards. Each row describes a card and ends with a `card_id` — a unique identifier for that specific printing. You want to train a model so that when a new record comes in with the card's attributes but no `card_id`, the model can predict which card it is.

```
| year | card_number | card_name  | game    | variety      | card_id |
|------|-------------|------------|---------|--------------|---------|
| 1999 | 4           | Charizard  | Pokemon | Holo         | 101     |
| 1999 | 4           | Charizard  | Pokemon | Normal       | 102     |
| 2000 | 4           | Charizard  | Pokemon | Holo         | 103     |
| 2001 | 4           | Charizard  | Pokemon | Reverse Holo | 104     |
| 1999 | 6           | Blastoise  | Pokemon | Holo         | 201     |
| 2000 | 6           | Blastoise  | Pokemon | Normal       | 202     |
```

Features (X): year, card_number, card_name, game, variety
Label (y): card_id

---

## The challenge: mixed column types

`year` and `card_number` are already numbers — fine as-is. But `card_name`, `game`, and `variety` are text. Models only understand numbers, so you need to encode them first.

### Deciding how to encode each text column

The right encoding depends on how many distinct values a column has:

| Column | Example values | Distinct count | Strategy | Why |
|---|---|---|---|---|
| `game` | Pokemon, Magic, Yu-Gi-Oh | Small (< 20) | **One-hot encoding** | Few categories, no natural order |
| `variety` | Holo, Normal, Reverse Holo | Small (< 20) | **One-hot encoding** | Few categories, no natural order |
| `card_name` | Charizard, Blastoise, … | Large (hundreds+) | **Label encoding** | One-hot would create hundreds of columns |

**One-hot encoding** creates a new 0/1 column for each category — safe when there are few categories:
```
variety = "Holo"         → [1, 0, 0]
variety = "Normal"       → [0, 1, 0]
variety = "Reverse Holo" → [0, 0, 1]
```

**Label encoding** replaces each category with an arbitrary number — used when one-hot would explode the column count:
```
"Blastoise" → 0
"Charizard" → 1
"Pikachu"   → 2
```
The numbers have no real meaning (Charizard is not "greater than" Blastoise), but the model can still use them to find similar rows.

---

## Step-by-step code

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# --- 1. Load your data ---
df = pd.read_csv('trading_cards.csv')

# --- 2. Separate features and label ---
X = df[['year', 'card_number', 'card_name', 'game', 'variety']].values
y = df['card_id'].values

# --- 3. Encode text columns ---

# Label-encode card_name (high cardinality — too many for one-hot)
le_name = LabelEncoder()
X[:, 2] = le_name.fit_transform(X[:, 2])  # column index 2 = card_name

# One-hot encode game (column 3) and variety (column 4)
# remainder='passthrough' means all other columns stay untouched
ct = ColumnTransformer(
    transformers=[('ohe', OneHotEncoder(), [3, 4])],
    remainder='passthrough'
)
X = ct.fit_transform(X)

# --- 4. Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# --- 5. Scale (important — year and card_number are on very different scales) ---
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test  = sc.transform(X_test)

# --- 6. Train ---
classifier = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
classifier.fit(X_train, y_train)

# --- 7. Predict card_id for a new record ---
new_card = {
    'year': 1999,
    'card_number': 4,
    'card_name': 'Charizard',
    'game': 'Pokemon',
    'variety': 'Holo'
}

# Encode card_name the same way training data was encoded
name_encoded = le_name.transform([new_card['card_name']])  # → [1]

# Build the raw input row in the same column order as X
new_row = np.array([[
    new_card['year'],
    new_card['card_number'],
    name_encoded[0],
    new_card['game'],
    new_card['variety']
]], dtype=object)

# Apply the same one-hot encoding and scaling
new_row_encoded = ct.transform(new_row)
new_row_scaled  = sc.transform(new_row_encoded)

predicted_id   = classifier.predict(new_row_scaled)
predicted_proba = classifier.predict_proba(new_row_scaled)

print(f"Predicted card_id: {predicted_id[0]}")
print(f"Confidence: {predicted_proba.max():.0%}")
```

---

## Important caveats

**card_id is the label, not a feature.** Don't include it in X — only in y. If you accidentally include it, the model cheats.

**If every card_id is unique**, this becomes a lookup problem with hundreds of classes. KNN can still do it, but accuracy will be lower because with k=5 neighbors, the model needs at least 3 training rows with the *same* card_id to be confident. More training data per card = more reliable predictions.

**Unseen values at prediction time.** If a new record contains a `card_name` that was never in training data, `le_name.transform()` will throw an error — the encoder has never seen that name before. You'd need to handle that explicitly (drop the row, or use a fallback encoding).

**Columns that don't help.** If a column like a database-internal ID or a free-text note has no predictive value, drop it before training — it adds noise without signal.
