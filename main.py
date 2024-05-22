import requests
import pyuseragents

follow_url = 'https://client.warpcast.com/v2/follows'

user_info_url = 'https://client.warpcast.com/v2/user-by-username'

auth_token = '' #INPUT YOUR AUTHORIZATION TOKEN IN BETWEEN THESE COMMAS

def get_usernames_from_file(file_path):
    usernames = []
    with open(file_path, 'r') as file:
        for line in file:
            username = line.strip().split('/')[-1]
            usernames.append(username)
    return usernames

def get_user_id(username):
    headers = {
        'Authorization': auth_token
    }
    params = {
        'username': username
    }
    response = requests.get(user_info_url, headers=headers, params=params)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data.get('result', {}).get('user', {}).get('fid') 
        if user_id:
            return user_id
        else:
            print(f"User ID not found for {username}. Response: {user_data}")
            return None
    else:
        print(f"Failed to get ID for {username}. Status code: {response.status_code}, Response: {response.text}")
        return None

def follow_user(fid, username):
    headers = {
        "Authorization": auth_token,
        "Content-Type": "application/json; charset=utf-8",
        "Origin": "https://warpcast.com",
        "Referer": "https://warpcast.com/",
        'user-agent': pyuseragents.random(),
    }
    data = {
        "targetFid": fid
    }
    response = requests.put(follow_url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Successfully followed {username} ✅")
    else:
        print(f"Failed to follow {username} ❌")

def main():
    file_path = 'username.txt'
    
    usernames = get_usernames_from_file(file_path)
    
    for username in usernames:
        user_id = get_user_id(username)
        if user_id:
            follow_user(user_id, username)

if __name__ == "__main__":
    main()