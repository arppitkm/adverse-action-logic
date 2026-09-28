"""
AWS Lambda handler using Mangum.

Mangum wraps the FastAPI ASGI application so it can run behind
API Gateway (REST or HTTP) and ALB Lambda integrations.
"""

from mangum import Mangum

from app.main import app

handler = Mangum(app, lifespan="off")
