from starlette import status


class TestCreateGame:
    def test_create_game(self, client):
        response = client.post("/games")
        body = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in body
        assert "code" in body
        assert "status" in body
        assert "tries" in body
        assert "max_tries" in body
        assert "guesses" in body
        assert "created_at" in body
