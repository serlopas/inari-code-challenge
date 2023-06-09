class TestHealthCheck:
    def test_healthcheck(self, client):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"message": "pong"}
