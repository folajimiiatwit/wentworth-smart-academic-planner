"""
Purpose:
Handles username-based account creation and login.

Main responsibilities:
- Validate usernames
- Create a new user if the username does not already exist
- Return saved user information for returning users
"""
import pandas as pd
from backend.data_manager import load_users, save_users, ELECTIVE_COLUMNS
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
  username = username.strip().lower()
  if username=="":
    return {"error": "invalid username"}
  users=load_users()
  existing_usernames=users["username"].astype(str).str.lower().values

  if username not in existing_usernames:
    new_user_data = {
      "username":username, "completed_required_courses":"","custom_completed_courses": "",
      "planned_courses": ""
    }

    for column in ELECTIVE_COLUMNS:
      new_user_data[column]=0

    new_user = pd.DataFrame([new_user_data])
    users=pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    
  return{"message":"Login Successful", "username": username}
    
