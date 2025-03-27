
import requests
import json

def main(params):

    HOST = ''
    PORT = ''

    USER_URL = f"https://{HOST}:{PORT}/SKLM/rest/v1/ckms/usermanagement/users/"
    GROUP_URL = f"https://{HOST}:{PORT}/SKLM/rest/v1/ckms/usermanagement/groups/"

    try:
        url = ''

        if (params['type'] == 'getUser'): 
            url = USER_URL
        elif(params['type'] == 'getUserInfo'):
            url = f"{USER_URL}{params['userName']}"
        elif(params['type'] == 'getGroupInfo'):
            url = f"{GROUP_URL}{params['groupName']}"

        headers = {
            "Authorization": f"SKLMAuth userAuthId={params['userAuthId']}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers, verify=False)
        res = ''
        usersList = []

        if (params['type'] == 'getUser'): 
            if(response.status_code == 200) :
                for x in response.json():
                    usersList.append(x["displayName"])

                if response.status_code == 200:
                    final_res = {
                        "headers": {
                            "Content-Type": "application/json",
                        },
                        "statusCode": 200,
                        "body": {
                            "usersList": usersList
                        }
                    }
                    return final_res
                else:
                    print(f"Error: {response.status_code}")
        elif(params['type'] == 'getUserInfo'):
            if(response.status_code == 200) :
                grpStr = ''
                roleStr = ''
                for x in response.json()['groups']:
                    if(len(grpStr) == 0):
                        grpStr = x["name"]
                    else:
                        grpStr = f"{grpStr}, {x['name']}"
                
                for x in response.json()['roles']:
                    if(len(roleStr) == 0):
                        roleStr = x["name"]
                    else:
                        roleStr = f"{roleStr}, {x['name']}"
                
                res = f"{response.json()['displayName']}, Groups assigned are {grpStr}, Roles assigned are {roleStr}"

                if response.status_code == 200:
                    return {
                        "headers": {
                            "Content-Type": "application/json",
                        },
                        "statusCode": 200,
                        "body": {
                            "response": res
                        }
                    }
                else:
                    print(f"Error: {response.status_code}")

        elif(params['type'] == 'getGroupInfo'):
            if(response.status_code == 200) :
                userStr = ''
                roleStr = ''
                for x in response.json()['users']:
                    if(len(userStr) == 0):
                        userStr = x
                    else:
                        userStr = f"{userStr}, {x}"
                
                for x in response.json()['roles']:
                    if(len(roleStr) == 0):
                        roleStr = x["name"]
                    else:
                        roleStr = f"{roleStr}, {x['name']}"
                
                res = f"{response.json()['name']}, Users in the group are {userStr}, Roles are {roleStr}"

                if response.status_code == 200:
                    return {
                        "headers": {
                            "Content-Type": "application/json",
                        },
                        "statusCode": 200,
                        "body": {
                            "response": res
                        }
                    }
                else:
                    print(f"Error: {response.status_code}")

        
    except Exception as e:
        print(f"API call failed {str(e)}")
