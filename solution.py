import requests

USERS_API = "https://jsonplaceholder.typicode.com/users"
TODOS_API = "https://jsonplaceholder.typicode.com/todos"

def get_users():
    response = requests.get(USERS_API)
    response.raise_for_status()
    return response.json()

def get_todos(user_id):
    response = requests.get(f"{TODOS_API}?userId={user_id}")
    response.raise_for_status()
    return response.json()

def is_user_in_fancode_city(user):
    lat = float(user['address']['geo']['lat'])  # Convert to float because int and string comparision is not supported with Python
    lng = float(user['address']['geo']['lng'])
    # Check if lat is between -40 and 5, and lng is between 5 and 100
    return -40 <= lat <= 5 and 5 <= lng <= 100

def calculate_completed_percentage(todos):
    total_tasks = len(todos)
    completed_tasks = sum(1 for todo in todos if todo['completed'])
    return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

def validate_fancode_users():
    users = get_users()
    for user in users:
        if is_user_in_fancode_city(user):
            todos = get_todos(user['id'])
            completed_percentage = calculate_completed_percentage(todos)
            print(f"User: {user['name']}, Completed Percentage: {completed_percentage}%")
            if completed_percentage <= 50:
                print(f"Validation Failed: {user['name']} does not have more than 50% tasks completed.")
                return False
    return True

if __name__ == "__main__":
    if validate_fancode_users():
        print("All users from FanCode city have more than 50% tasks completed.")
    else:
        print("Some users from FanCode city have less than 50% tasks completed.")
