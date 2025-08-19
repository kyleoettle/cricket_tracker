Awesome — here’s a concise, end-to-end implementation plan based on the stack and choices we aligned on:

Auth: Auth0 (JWT, RBAC)

App: Single Python repo with FastAPI (API + ML) and Streamlit (UI) running in one container

Data: Azure Cosmos DB (Core/SQL API) for operational data + model registry (metadata)

Models: TensorFlow for training/inference

Artifacts: Azure Blob Storage for model binaries (SavedModel/.h5)

Deploy: Docker → Azure Container Registry → Azure Container Apps (or App Service for Containers)

Deployment: Azure Developer CLI (AZD)
Use AZD for streamlined provisioning and deployment to Azure. AZD manages infrastructure-as-code (Bicep), resource creation, and CI/CD integration.

Key AZD steps:
- Install AZD: https://aka.ms/azure-dev/install
- Run `azd init` to set up the project for Azure deployment (creates `azure.yaml` and scaffolds infra).
- Use Bicep templates (e.g., `azure-aca.bicep`) for resource provisioning (Container Apps, Cosmos DB, Blob Storage, etc.).
- Deploy with `azd up` (provisions resources, builds, and deploys the app).
- Integrate with GitHub Actions for CI/CD using AZD workflows.

Infra files:
- `azure.yaml`: AZD project configuration.
- `azure-aca.bicep`: Infrastructure-as-code for Azure resources.

Reference: https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/

Retraining: Coach-triggered button and/or scheduled batch from Cosmos DB → save to Blob → update model registry in Cosmos

1) Architecture & patterns
1.1 High-level flow

Player/coach logs in (Auth0) → Streamlit UI.

Streamlit calls FastAPI endpoints with Bearer JWT.

FastAPI enforces RBAC (player/coach/admin) and reads/writes Cosmos DB.

Coach presses “Retrain” → FastAPI batch loads from Cosmos, trains TensorFlow, saves model to Blob, writes new model version doc to Cosmos, marks it active.

Inference API loads active model at startup (or hot-reloads on version change) and serves predictions to UI.

1.2 Key patterns

Model registry pattern: Cosmos stores versioned metadata; Blob stores binaries.

Config by environment: env vars for secrets/URIs; .env for local, Azure App Settings for prod.

Security: Auth0 JWT validation middleware in FastAPI; scopes + roles claims for authorization.

Data privacy: Separate container for menstrual data; access limited to player + designated medical/coach roles.

2) Repository & processes

/src
  /api              # FastAPI
    main.py
    deps.py         # auth/jwt, db clients
    models.py       # pydantic schemas
    routes/
      players.py
      sessions.py
      cycle.py
      metrics.py
      predict.py
      retrain.py
  /ml               # TensorFlow code
    features.py     # ACWR, aggregations, encoders
    trainer.py      # batch train from Cosmos
    inference.py    # load/serve active model, hot-reload
  /ui               # Streamlit
    dashboard.py
/infra
  azure-aca.bicep (optional IaC)


Process

Format/typecheck: black, ruff, mypy.

Tests: pytest (unit for features, API, minimal model test).

CI/CD: GitHub Actions → build, push image to ACR, deploy to ACA.

3) Data model (Cosmos DB – SQL API)

Create database: cricket_ai
Recommended consistency: Session (default)
Autoscale RU/s on each container (start 1k–3k RU/s and tune).

Partition key (pk) is critical for cost/perf. Use playerId where items are player-centric; use teamId for team views; for registry use /type.

3.1 players (container)

id: string (auth0 user id or internal uuid) (pk)

type: "player" (for cross-container queries)

fullName, role (player|coach|admin), teamId, dob, otherSports (array)

Indexing: default; add composite on (teamId,id) for team queries.

3.2 teams

id (pk), type: "team", name, coachIds (array)

3.3 sessions (training/match/other sport)

id (uuid)

playerId (pk)

type: "session"

teamId, date (ISO), sessionType (practice|match|gym|other)

sport (cricket|netball|...)

durationMin, rpe (0–10), sessionLoad (= rpe × duration)

Cricket detail: bowlingOvers, battingBalls, fieldingLoad (1–5)

TTL: e.g., none (keep) or archive older raw sessions later.

3.4 cycleLogs (menstrual & wellness)

id (uuid)

playerId (pk)

type: "cycle"

date, cyclePhase (menstrual|follicular|ovulatory|luteal)

symptoms (array), wellness (1–5), sleep (1–5), mood (1–5), soreness (1–5)

Access: strict (see RBAC). Consider client-side encryption for sensitive fields (optional phase 2).

3.5 metrics (weekly derived)

id: ${playerId}_${weekStart}

playerId (pk)

type: "metrics"

weekStart (ISO Monday), acuteLoad7, chronicLoad28, acwr

battingLoad, bowlingLoad, fieldingLoad, externalSportLoad

Compute via batch job on retrain or nightly.

3.6 injuries (optional, valuable for labels)

id, playerId (pk), type:"injury"

date, injuryType, severity, daysOut, notes

3.7 modelRegistry (model metadata)

id: model_<timestamp> (pk)

type: "model"

status: active|candidate|archived

createdAt, createdBy (coach id or system)

dataRange: {from, to}

algo: "tf_mlp_v1" (or "tf_lstm_v1")

metrics: {auc, pr_auc, loss, val_loss, ...}

storage: {container, blobName, url}

notes

Unique constraint (logical): Only one status=active.

4) Storage (Blob)

Container: ml-models

Naming: injury_risk/<algo>/<YYYY>/<MM>/model_<timestamp>.h5

Access: Private; app uses managed identity or SAS (short-lived) to download/upload.

Versioning: enable blob versioning (optional) + keep metadata in Cosmos.

5) Core calculations & features
5.1 Derived metrics

SessionLoad = rpe * durationMin

Acute (7d) = sum(SessionLoad last 7 days)

Chronic (28d) = rolling mean of Acute over 28 days (or EWMA α≈0.07)

ACWR = Acute / Chronic (clip Chronic floor: e.g., 50 to avoid div by small number)

Role splits:

bowlingLoad: sum(overs × rpe)

battingLoad: sum(balls × rpe)

externalSportLoad: sum SessionLoad where sport != cricket

5.2 ML features (examples)

Numeric: acuteLoad7, chronicLoad28, acwr, battingLoad7, bowlingLoad7, externalSportLoad7

Categorical: cyclePhase (one-hot)

Interactions: acwr*luteal, bowlingLoad7*menstrual

Temporal: last 4 weeks loads (for LSTM)

Labels:

InjuryNext14Days (requires injury logs)

ReadinessNextMatch (if you collect readiness ratings)

6) API (FastAPI)
6.1 Security

Validate Auth0 JWT (RS256), audience, issuer.

Extract sub (user id), roles and/or permissions from claims.

Decorators:

@requires_role("coach"), @requires_role("player")

Or @requires_scope("retrain:models")

6.2 Example endpoints

POST /api/sessions (player) – create session

GET /api/sessions?playerId=me&from=&to=

POST /api/cycle (player) – log cycle

GET /api/metrics/weekly?playerId=...

GET /api/predict/{playerId} – current risk/readiness

POST /api/retrain (coach/admin) – batch retrain

Body: {from, to, algo} (optional)

Response: model id, metrics

GET /api/models/active – active model metadata

POST /api/models/{id}/activate (coach/admin) – rollback/activate

7) Streamlit UI (coach & player)

Player tab: quick entry forms for session & cycle; see personal trends (ACWR line + threshold bands).

Coach tab: team selector → table of players with risk badge, ACWR, bowling load; drill-down player view.

Retrain tab (coach only): date range picker → “Retrain” button → show metrics; “Activate model” button if multiple candidates.

What-if: sliders for midweek overs → recompute predicted readiness for match day.

8) TensorFlow integration
8.1 Training (batch)

Pull sessions + cycle + injuries (if available) per player/date range.

Build features (Pandas) → X, y

Split train/val by time (avoid leakage).

Model (starter MLP for tabular):

import tensorflow as tf
def make_model(n_in):
    m = tf.keras.Sequential([
      tf.keras.layers.Input((n_in,)),
      tf.keras.layers.Dense(64, activation="relu"),
      tf.keras.layers.Dropout(0.2),
      tf.keras.layers.Dense(32, activation="relu"),
      tf.keras.layers.Dense(1, activation="sigmoid")  # risk prob
    ])
    m.compile(optimizer="adam", loss="binary_crossentropy",
              metrics=[tf.keras.metrics.AUC(name="auc")])
    return m


Save: model.save(local_path) → upload to Blob → write registry doc in Cosmos (status="candidate").

Optionally auto-activate best by val_auc.

8.2 Inference service

On startup: fetch active model metadata from Cosmos → download Blob → tf.keras.models.load_model()

Hot reload: poll registry every N minutes or provide POST /api/models/reload to switch immediately after activation.

Cache model in memory; thread-safe lock around swap.

9) Deployment on Azure

Provision: ACR, Container Apps env, Cosmos DB account (SQL API), Blob Storage (private, with managed identity), optional Log Analytics.

Secrets: store Auth0 domain/audience, Cosmos URI/key, Storage conn string (or assign managed identity + role Storage Blob Data Contributor).

Build & push: GitHub Actions → docker build → push to ACR.

Deploy: Container App with CPU 1–2 vCPU / 2–4 GB RAM; scale min=1, max=3.

Ingress: enable external for Streamlit; secure /api/* with JWT (document audience/issuer).

Observability: send logs to Log Analytics; add basic metrics (requests, latency, retrain duration).

Dockerfile (single container, both servers):

FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["sh","-c","uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run ui/dashboard.py --server.port=8501 --server.address=0.0.0.0"]

10) RBAC & privacy

Auth0 roles: player, coach, admin.

Scopes: read:own, read:team, write:own, write:team, retrain:models.

Cycle data: restrict to player + assigned coach/medical; hide by default from other staff.

Audit: log access to cycle endpoints.

Data retention: define policy (e.g., delete cycle logs after N years on request).

11) Scheduling retrains

Coach button → POST /api/retrain (async task)

Automated: Azure Container Apps Jobs or Azure Functions Timer → call /api/retrain nightly/weekly with preset range.

Track job runs in a jobs container in Cosmos (status, duration, metrics).

12) Validation, testing, rollout

Validation: Pydantic models on all API inputs; server-side recomputation of sessionLoad.

Testing: unit tests for features, model training on synthetic set, API contract tests.

Rollout: pilot with one team → refine forms/labels → expand.

Safeguards: ACWR & wellness rule-based guardrails even when model confidence is low.