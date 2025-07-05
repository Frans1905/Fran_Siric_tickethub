
def test_list_tickets(client, auth_headers):
    """GET /tickets should return a list and respect limit param."""
    response = client.get("/tickets?limit=2", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_list_tickets_status(client, auth_headers):
    """GET /tickets should return a list and return tickets with correct status."""
    response = client.get("/tickets?limit=2&status=open", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(ticket["status"] == "open" for ticket in data)

def test_list_tickets_prio(client, auth_headers):
    """GET /tickets should return a list and return tickets with correct priority."""
    response = client.get("/tickets?limit=2&priority=high", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert all(ticket["priority"] == "high" for ticket in data)

def test_search_tickets(client, auth_headers):
    """GET /tickets/search should filter titles by substring."""
    response = client.get("/tickets/search?q=Clean", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("Clean".lower() in ticket["title"].lower() for ticket in data)


def test_get_ticket_details_success(client, auth_headers):
    """GET /tickets/{id} for existing ticket returns details and source."""
    response = client.get("/tickets/1", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "source" in data
    source = data["source"]
    assert all(k in source for k in ("id", "todo", "completed", "userId"))
    assert data["assignee"] == "Paisley Bell"


def test_get_ticket_details_not_found(client, auth_headers):
    """GET /tickets/{id} for non-existent ticket returns 404."""
    response = client.get("/tickets/999999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_stats_endpoint(client, auth_headers):
    response = client.get("/tickets/stats", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "total" in data
    assert "open" in data
    assert "closed" in data
    assert "priority" in data
    assert all(p in data["priority"] for p in ["low", "medium", "high"])
