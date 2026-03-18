"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_success(client, reset_activities):
    """
    Test successful signup for an activity.
    Should return HTTP 200 and add the participant to the activity.
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate_email_fails(client, reset_activities):
    """
    Test that signing up with an email that already exists fails.
    Should return HTTP 400 with an error message.
    """
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}  # Already registered
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_nonexistent_activity_fails(client, reset_activities):
    """
    Test that signing up for a non-existent activity fails.
    Should return HTTP 404 with an error message.
    """
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_signup_multiple_different_students(client, reset_activities):
    """
    Test that multiple different students can sign up for the same activity.
    """
    # First signup
    response1 = client.post(
        "/activities/Programming Class/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second signup
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": "bob@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Verify both are registered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    programmign_participants = activities["Programming Class"]["participants"]
    assert "alice@mergington.edu" in programmign_participants
    assert "bob@mergington.edu" in programmign_participants


def test_signup_increases_participant_count(client, reset_activities):
    """
    Test that signing up increases the participant count for an activity.
    """
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data["Chess Club"]["participants"])
    
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "newperson@mergington.edu"}
    )
    
    # Get new state
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data["Chess Club"]["participants"])
    
    assert final_count == initial_count + 1
