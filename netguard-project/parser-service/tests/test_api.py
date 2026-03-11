from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_parse_endpoint():

    file_content = """
    resource "aws_s3_bucket" "test" {
      bucket = "demo-bucket"
    }
    """

    response = client.post(
        "/parse",
        files={"file": ("test.tf", file_content)}
    )

    assert response.status_code == 200