import pandas as pd
from backend.data_manager import load_users, save_users, ELECTIVE_COLUMNS
def login_user(username):
  username = username.strip().lower()
  if username=="":
    return {"error": "invalid username"}
  users=load_users()
  existing_usernames=users["username"].astype(str).str.lower().values

  if username not in existing_usernames:
    new_user_data = {
      "username":username, "completed_required_courses":"",
      "planned_courses": ""
    }

    for column in ELECTIVE_COLUMNS:
      new_user_data[column]=0

    new_user = pd.DataFrame([new_user_data])
    users=pd.concat([users, new_user], ignore_index=True)
    save_users(users)
    
  return{"message":"Login Successful", "username": username}
    
