from app import app


def test_index_returns_200():
    client = app.test_client() #salje zahteve aplikaciji bez pravljenja servera
    response = client.get("/")
    assert response.status_code == 200 #assert znaci ovomora biti tacno inace test pada
    assert response.get_json()["message"] == "Hello"
    #Test ne  dira redis