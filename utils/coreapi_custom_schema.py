import coreapi
from rest_framework.schemas import AutoSchema


input_request_schema = AutoSchema(
    manual_fields=[
        coreapi.Field("request_id", required=True, type="int", description="Enter Request ID")
    ]
)
