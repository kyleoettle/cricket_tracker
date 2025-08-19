# Cricket Tracker Implementation Plan

This plan breaks down the build into small, trackable steps. Use the color-coded icons to track progress:
- ⬜ Not started
- 🟨 In progress
- 🟩 Done

---

## 1. Repo & Project Setup


⬜ 1.1 Initialize Git repo and directory structure
	- Create `src` directory
	- Move `api`, `ml`, and `ui` into `src/`
⬜ 1.2 Add `.gitignore`, `README.md`, and `requirements.txt` to root
⬜ 1.3 Set up Python environment (venv/conda)
⬜ 1.4 Add pre-commit hooks (black, ruff, mypy)

## 2. Infrastructure & Deployment

⬜ 2.1 Install Azure Developer CLI (AZD)
⬜ 2.2 Run `azd init` and create `azure.yaml`
⬜ 2.3 Scaffold Bicep templates for Container Apps, Cosmos DB, Blob Storage
⬜ 2.4 Add Dockerfile for FastAPI + Streamlit container
⬜ 2.5 Test local Docker build and run
⬜ 2.6 Deploy initial app to Azure using `azd up`


## 3. API (FastAPI)

⬜ 3.1 Scaffold `src/api` folder and FastAPI app (`main.py`)
⬜ 3.2 Add JWT Auth0 middleware and RBAC decorators
⬜ 3.3 Create Pydantic models for all entities
⬜ 3.4 Implement Cosmos DB client and dependency injection
⬜ 3.5 Add routes for sessions, cycle logs, metrics, model registry
⬜ 3.6 Add endpoints for model inference and retraining
⬜ 3.7 Write unit tests for API endpoints


## 4. ML Module

⬜ 4.1 Scaffold `src/ml` folder
⬜ 4.2 Implement feature engineering (ACWR, aggregations)
⬜ 4.3 Build starter TensorFlow model (MLP)
⬜ 4.4 Add trainer for batch retrain from Cosmos DB
⬜ 4.5 Implement inference service (load/serve model, hot-reload)
⬜ 4.6 Integrate model registry logic
⬜ 4.7 Write minimal ML tests (synthetic data)


## 5. UI (Streamlit)

⬜ 5.1 Scaffold `src/ui` folder and `dashboard.py`
⬜ 5.2 Implement login screen (Auth0)
⬜ 5.3 Build player workload input form
⬜ 5.4 Build menstrual cycle tracking form
⬜ 5.5 Create player dashboard (charts, metrics, AI insights)
⬜ 5.6 Build coach dashboard (team table, filters, risk badges)
⬜ 5.7 Add player profile view (trends, cycle overlay, recommendations)
⬜ 5.8 Add model retraining tab (button, status)
⬜ 5.9 Add export, notifications, and settings screens

## 6. Data Model & Cosmos DB

⬜ 6.1 Define containers: players, teams, sessions, cycleLogs, metrics, injuries, modelRegistry
⬜ 6.2 Implement partition keys and indexing
⬜ 6.3 Add data validation and privacy logic
⬜ 6.4 Test CRUD operations for all entities

## 7. Security & Privacy

⬜ 7.1 Integrate Auth0 JWT validation in API and UI
⬜ 7.2 Enforce RBAC on endpoints and UI screens
⬜ 7.3 Restrict cycle data access (player + assigned coach/medical)
⬜ 7.4 Add audit logging for sensitive endpoints

## 8. CI/CD & Testing

⬜ 8.1 Set up GitHub Actions for build, test, and deploy
⬜ 8.2 Add test coverage for API, ML, and UI
⬜ 8.3 Validate deployment to Azure (Container Apps)
⬜ 8.4 Monitor logs and metrics (Log Analytics)

## 9. Rollout & Validation

⬜ 9.1 Pilot with one team (collect feedback)
⬜ 9.2 Refine forms, labels, and dashboards
⬜ 9.3 Expand to more teams
⬜ 9.4 Define data retention and privacy policies

---

Update this file as you progress. Each step is designed to be small and actionable for rapid iteration and tracking.
