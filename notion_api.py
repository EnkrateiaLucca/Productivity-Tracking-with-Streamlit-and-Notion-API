import json
import requests


# curl -X POST https://api.notion.com/v1/databases/8dbeef10972e4374866d905662bdd049/query

# -H 'Authorization: Bearer '"secret_cO0QMTTk4Jpj6ng6xYyXjmi83vh6BzynB0gJSu1Z7YJ"''

# -o database.json 

DATABASE_ID = "8dbeef10972e4374866d905662bdd049"
NOTION_URL = 'https://api.notion.com/v1/databases/'

class NotionSync:
    def __init__(self):
        pass    

    def query_databases(self,integration_token="secret_cO0QMTTk4Jpj6ng6xYyXjmi83vh6BzynB0gJSu1Z7YJ"):
        database_url = NOTION_URL + DATABASE_ID + "/query"
        response = requests.post(database_url, headers={"Authorization": f"{integration_token}"})
        if response.status_code != 200:
            raise ApiError(f'Response Status: {response.status_code}')
        else:
            return response.json()
    
    def get_projects_titles(self,data_json):
        return list(data_json["results"][0]["properties"].keys())
    

    def get_projects_data(self,data_json,projects):
        projects_data = {}
        for p in projects:
            if p!="Name" and p !="Date":
                projects_data[p] = [data_json["results"][i]["properties"][p]["checkbox"]
                                    for i in range(len(data_json["results"]))]
            elif p=="Date":
                dates = [data_json["results"][i]["properties"]["Date"]["date"]["start"]
                                    for i in range(len(data_json["results"]))]

        
        return projects_data,dates


if __name__=='__main__':
    nsync = NotionSync()
    data = nsync.query_databases()
    projects = nsync.get_projects_titles(data)
    projects_data,dates = nsync.get_projects_data(data,projects)