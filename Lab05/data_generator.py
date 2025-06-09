
import json

def generate_data(num_users=1000):
    users = []
    for i in range(1, num_users + 1):
        user = {
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "city": f"City {(i % 10) + 1}"
        }
        users.append(user)
    with open('data.json', 'w') as f:
        json.dump(users, f, indent=4)

if __name__ == '__main__':
    generate_data()


