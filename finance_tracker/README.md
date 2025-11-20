# AI Finance Tracker

AI-powered personal finance tracker built with Python and Streamlit. This repository contains a scaffolded, production-oriented architecture including:

- Domain models in `models/` demonstrating OOP (encapsulation, inheritance, polymorphism, abstraction).
- Database repositories in `database/repositories/` (Supabase Postgres).
- Business services in `services/`.
- AI/ML modules in `ai_modules/` (transaction classifier, spending predictor, recommender).
- Streamlit UI under `ui/`.
- Unit tests under `tests/`.

This README covers quick setup, Supabase initialization, training the sample ML model, running locally, and testing.

## Quick start (development)

1. Create and activate a Python 3.10+ virtual environment.

	PowerShell example:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and fill in your Supabase credentials and optional SMTP/Twilio keys.

3. (Optional) Initialize Supabase tables by applying `database/schema.sql` in your Supabase SQL editor.

4. Train the sample classifier (creates files in `ai_modules/models/`):
```powershell
python -m ai_modules.train_classifier
```

5. Run the Streamlit app:
```powershell
streamlit run main.py
```

## Supabase setup

1. Create a Supabase project at https://app.supabase.com and retrieve `SUPABASE_URL` and `SUPABASE_KEY` (use anon or service role as appropriate).
2. Create the `auth` users table by enabling Supabase Auth (default in Supabase projects).
3. Open SQL Editor in Supabase and run the contents of `database/schema.sql` to create the required tables and indexes.
4. Set Row-Level Security (RLS) and policies as needed for your deployment. The schema file includes example policies for `transactions`.

## Notes on AI modules

- `ai_modules/transaction_classifier.py` implements a RandomForestClassifier over TF-IDF features. A small training script is provided at `ai_modules/train_classifier.py` that writes model artifacts into `ai_modules/models/`.
- `ai_modules/spending_predictor.py` uses Prophet for forecasting; Prophet is optional and will be imported lazily at runtime. Install Prophet only if you plan to use forecasting.

## Running tests

Run pytest from the project root:
```powershell
pytest -q
```

## Development notes

- The app uses `config/supabase_config.py` to instantiate a Supabase client. If `SUPABASE_URL`/`SUPABASE_KEY` are not set, the client will be `None` and repository operations will return safe defaults.
- The `TransactionService` integrates the classifier: leaving the `Category` field empty in the add-transaction form will attempt automatic categorization using the trained model.

## Docs and UML

The `docs/` directory contains architecture notes and placeholder UML diagrams; replace these placeholders with generated diagrams exported from your UML tool.

## License

See `LICENSE` in repository root.
