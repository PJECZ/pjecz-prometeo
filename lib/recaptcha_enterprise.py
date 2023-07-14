"""
Validate reCAPTCHA Enterprise token

Usage:

    @app.get("/your-route")
    async def your_route(token: str):
        await validate_recaptcha(token)
        # Your code here

"""
from typing import Annotated

from fastapi import Depends, HTTPException
from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

from config.settings import PROJECT_ID, Settings, get_settings


async def create_assessment(
    settings: Annotated[Settings, Depends(get_settings)],
    token: str,
) -> Assessment:
    """Create an assessment to analyze the risk of a request."""

    # Create client
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Create event
    event = recaptchaenterprise_v1.Event()
    event.token = token
    event.site_key = settings.recaptcha_site_key

    # Create assessment
    assessment = Assessment()
    assessment.event = event

    # Set project
    if PROJECT_ID != "":
        project_name = f"projects/{PROJECT_ID}"
    else:
        project_name = "projects/justicia-digital-gob-mx"

    # Build the assessment request
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    # Call API
    response = client.create_assessment(request=request)

    # Check if the token is valid and the risk score
    if response.token_properties.valid and response.risk_analysis.score >= 0.5:
        return response

    # Else, raise an exception
    raise HTTPException(status_code=400, detail="Invalid reCAPTCHA token")
