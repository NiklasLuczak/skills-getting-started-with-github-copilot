"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


def test_remove_participant_success(client, reset_activities):
    """
    Test successful removal of a participant from an activity.
    Should return HTTP 200 and remove the participant.
    """
    response = client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Removed" in data["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_nonexistent_participant_fails(client, reset_activities):
    """
    Test that removing a participant who isn't registered fails.
    Should return HTTP 404 with an error message.
    """
    response = client.delete(
        "/activities/Chess Club/participants/notregistered@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_from_nonexistent_activity_fails(client, reset_activities):
    """
    Test that removing from a non-existent activity fails.
    Should return HTTP 404 with an error message.
    """
    response = client.delete(
        "/activities/Nonexistent Activity/participants/student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_remove_decreases_participant_count(client, reset_activities):
    """
    Test that removing a participant decreases the participant count.
    """
    # Get initial state
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    initial_count = len(initial_data["Chess Club"]["participants"])
    
    # Remove participant
    client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    
    # Get new state
    final_response = client.get("/activities")
    final_data = final_response.json()
    final_count = len(final_data["Chess Club"]["participants"])
    
    assert final_count == initial_count - 1


def test_remove_all_participants(client, reset_activities):
    """
    Test that all participants can be removed from an activity.
    """
    # Remove all participants from Programming Class (which has 2)
    client.delete(
        "/activities/Programming Class/participants/emma@mergington.edu"
    )
    client.delete(
        "/activities/Programming Class/participants/sophia@mergington.edu"
    )
    
    # Verify empty
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert len(activities["Programming Class"]["participants"]) == 0


def test_remove_then_signup_again(client, reset_activities):
    """
    Test that a student can sign up after being removed.
    """
    # Remove
    client.delete(
        "/activities/Chess Club/participants/michael@mergington.edu"
    )
    
    # Sign up again
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"}
    )
    
    assert response.status_code == 200
    
    # Verify re-registered
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
