# Adverse Action Logic — MRS_30 Microservice

A standalone FastAPI microservice that performs adverse action calculations for the Lend API system. Rebuilt from LendAPI's MRS_30 (Model Runtime Studio 30) as an independent, deployable Lambda function.

## Architecture

```
app/
├── core/           # Pure business logic (no HTTP dependencies)
│   ├── cra_source.py          # CRA source population
│   ├── cra_calculations.py    # App score fail reasons
│   └── vantage_reasons.py     # Vantage reason code lookup
├── models/         # Pydantic request/response schemas
├── api/v1/         # FastAPI route handlers
├── main.py         # App factory
└── config.py       # Environment-based settings
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/v1/cra-sources` | Populate prioritized CRA sources |
| `POST` | `/v1/app-score-fail-reasons` | Compute top 4 risk model fail reasons |
| `POST` | `/v1/vantage-reasons` | Resolve Vantage score reason codes |
| `POST` | `/v1/adverse-action` | Unified endpoint (all three calculations) |

## Local Development

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run the server
uvicorn app.main:app --reload --port 8000

# Open API docs
open http://localhost:8000/docs
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=term-missing
```

## Deployment (AWS Lambda)

### Using SAM CLI

```bash
# Build
sam build

# Local testing
sam local start-api

# Deploy
sam deploy --guided
```

### Using Docker

```bash
# Build image
docker build -t mrs30-adverse-action .

# Run locally
docker run -p 9000:8080 mrs30-adverse-action

# Test
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" \
  -d '{"httpMethod": "GET", "path": "/health"}'
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MRS30_APP_NAME` | Adverse Action Logic (MRS_30) | Application name |
| `MRS30_APP_VERSION` | 1.0.0 | Application version |
| `MRS30_DEBUG` | false | Enable debug mode |
| `MRS30_ALLOWED_ORIGINS` | ["*"] | CORS allowed origins |
