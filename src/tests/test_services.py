class TestMetricsService:
    def test_metrics(self, client):
        response = client.get("/metrics")
        assert response.status_code == 200
