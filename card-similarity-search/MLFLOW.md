# MLflow — Do You Need It for This Project?

## What MLflow is

MLflow is an open-source platform for managing the ML lifecycle. It has four main features:

| Feature | What it does |
|---------|--------------|
| **Experiment tracking** | Log metrics (loss, accuracy), parameters, and notes across training runs so you can compare them |
| **Model registry** | Version models, promote them through Staging → Production with an audit trail |
| **Artifacts** | Save and retrieve model weights, plots, and data files tied to a specific run |
| **Model serving** | Deploy a tracked model as a REST API |

MLflow's core value is answering: *"I ran 50 training experiments — which one performed best, and with what settings?"*

---

## Do you need it for this project right now?

**No.** Here is why:

This project has no training loop. CLIP is a pretrained model used as a fixed
feature extractor. You are not adjusting any model weights, there are no loss
curves, and there are no hyperparameters being searched. The only things you tune
are `threshold` and `top_k`, which are just numbers passed at query time — not
something that needs a tracking system.

| MLflow feature | Useful here? | Reason |
|----------------|-------------|--------|
| Experiment tracking | Not yet | No training runs to compare |
| Model registry | Not yet | CLIP checkpoint is fixed, not yours to version |
| Artifacts | Maybe | Could store `card_embeddings.npy` as a versioned artifact |
| Model serving | No | Already covered by the Flask API (`src/api.py`) |

---

## When it would become relevant

### Fine-tuning CLIP (Phase 5d in PLAN.md)

This is the clearest trigger. Once you start training, you will quickly end up with
questions like:

- *"Which learning rate worked best?"*
- *"Did run #3 or run #7 produce better Recall@3?"*
- *"What exact settings produced the model we deployed?"*

MLflow answers all of these. You would:

1. Start a run at the beginning of each fine-tuning session
2. Log parameters: learning rate, batch size, number of epochs, CLIP model variant
3. Log metrics each epoch: training loss, eval loss, Recall@3 on your test set
4. Save the fine-tuned model weights as an artifact
5. Compare runs in the MLflow UI to pick the best one
6. Register the winning model and promote it to Production

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 1e-5)
    mlflow.log_param("clip_model", "openai/clip-vit-base-patch32")
    mlflow.log_param("epochs", 10)

    for epoch in range(10):
        loss = train_one_epoch(...)
        recall = evaluate(...)
        mlflow.log_metric("train_loss", loss, step=epoch)
        mlflow.log_metric("recall_at_3", recall, step=epoch)

    mlflow.pytorch.log_model(model, "fine_tuned_clip")
```

### Comparing CLIP model sizes (Phase 5b in PLAN.md)

If you swap between `clip-vit-base-patch32` and `clip-vit-large-patch14` and want
to record which produced better Recall@3 on your card dataset, MLflow is a clean
way to track that comparison even without full fine-tuning.

---

## Summary

| Scenario | Use MLflow? |
|----------|-------------|
| POC with pretrained CLIP, no training | **No** |
| Adjusting `threshold` or `top_k` | **No** — just change the number |
| Comparing CLIP model variants by Recall@3 | **Maybe** — useful but not required |
| Fine-tuning CLIP on your card dataset | **Yes** — log params, metrics, save weights |
| Versioning your embeddings file | **Maybe** — MLflow artifacts can store `.npy` files, but a git tag is simpler for now |

**Rule of thumb:** introduce MLflow the moment you have more than one training run
to compare. Before that point it adds overhead without payoff.

---

## Resources

- MLflow docs: https://mlflow.org/docs/latest/index.html
- MLflow + HuggingFace integration: `mlflow.transformers.log_model()`
- Free hosted tracking server: Databricks Community Edition (or run locally with `mlflow ui`)
