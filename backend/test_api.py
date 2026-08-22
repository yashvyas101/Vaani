import io
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def run_tests():
    print("1. Testing GET /health")
    response = client.get("/health")
    print(f"Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == 200

    print("\n2. Testing POST /api/demo/text with known question")
    response = client.post("/api/demo/text", json={"text": "tell me about beaches in goa"})
    print(f"Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == 200
    assert "Morjim for quiet sunsets" in response.json()["answer"]

    print("\n3. Testing POST /api/demo/text with unknown question")
    response = client.post("/api/demo/text", json={"text": "what is the capital of france?"})
    print(f"Status: {response.status_code}, Response: {response.json()}")
    assert response.status_code == 200
    assert "didn't quite catch that" in response.json()["answer"]

    print("\n4. Testing POST /api/demo/voice with mock audio")
    # create dummy audio file
    dummy_audio = io.BytesIO(b"fake_audio_bytes")
    dummy_audio.name = "test.wav"
    
    response = client.post(
        "/api/demo/voice",
        files={"audio": ("test.wav", dummy_audio, "audio/wav")}
    )
    print(f"Status: {response.status_code}, Content-Type: {response.headers.get('content-type')}")
    print(f"Response Bytes (first 30): {response.content[:30]}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"
    
    print("\nAll tests passed successfully!")

if __name__ == "__main__":
    run_tests()
