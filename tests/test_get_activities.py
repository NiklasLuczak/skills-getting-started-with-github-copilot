"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_success(client, reset_activities):
    """
    Test successful retrieval of all activities.
    Should return HTTP 200 with all activities in the response.
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Verify activity structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_returns_participants(client, reset_activities):
    """
    Test that the GET /activities endpoint returns participant data.
    """
    response = client.get("/activities")
    data = response.json()
    
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) == 2
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]


def test_get_activities_returns_activity_details(client, reset_activities):
    """
    Test that activity details are returned correctly.
    """
    response = client.get("/activities")
    data = response.json()
    
    programming = data["Programming Class"]
    assert programming["description"] == "Learn programming fundamentals and build software projects"
    assert programming["schedule"] == "Tuesdays and Thursdays, 3:30 PM - 4:30 PM"
    assert programming["max_participants"] == 20
