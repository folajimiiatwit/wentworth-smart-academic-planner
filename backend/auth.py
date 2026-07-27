"""
Purpose:
Handles username-based account creation and login.

Main responsibilities:
- Validate usernames
- Create a new user if the username does not already exist
- Return saved user information for returning users
"""
import pandas as pd
from backend.data_manager import create_user, get_user
def login_user(username):
  """
  Authenticate a user by username and create a new user record when needed.

  The username is normalized by trimming whitespace and converting it to lowercase.
  If the username does not already exist in the users CSV file, this function creates
  an empty user profile with no completed courses and zero elective credits.

  Args:
      username (str): Username entered by the student.

  Returns:
      dict: A success message and normalized username, or an error message for an
      invalid blank username.
  """
  normalized_username = username.strip().lower()

  if not normalized_username:
    return {"error": "Invalid username"}

  user = get_user(normalized_username)

  if user is None:
    user = create_user(normalized_username)

  if user is None:
    return {"error": "Could not create user"}

  return {
    "message": "Login Successful",
    "username": user.username,
  }    
