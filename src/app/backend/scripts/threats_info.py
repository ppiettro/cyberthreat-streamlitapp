import json
from dotenv import load_dotenv
from os import getenv
from github import Github
from github import Auth

class CyberThreatsData:
    def __init__(self):
        load_dotenv()
        self.repository_token = getenv("GITHUB_TOKEN")

    def update_data(self, data):
        auth = Auth.Token(self.repository_token)
        github = Github(auth=auth)
        repo = github.get_user().get_repo("cyberthreat-streamlitapp")

        contents = repo.get_contents("cyberthreats_data.csv")
        repo.update_file("cyberthreats_data.csv", "Updating cyberthreats data", content=data, sha=contents.sha)


class ThreatInfo:
    def __init__(self, threat):
        load_dotenv()
        self.repository_token = getenv("GITHUB_TOKEN")
        self.threat = threat

    def publish_data(self, threat_description):
        auth = Auth.Token(self.repository_token)
        github = Github(auth=auth)
        repo = github.get_user().get_repo("cyberthreat-streamlitapp")

        contents = repo.get_contents("threats_info.json")
        existing_data = json.loads(contents.decoded_content.decode("utf-8"))

        new_data = {
            self.threat: threat_description
        }

        existing_data.append(new_data)
        updated_data = json.dumps(existing_data, indent=4, ensure_ascii=False)

        repo.update_file("threats_info.json", "Updating threats info", content=updated_data, sha=contents.sha)


    def get_data(self):
        with open("src/data/threats_info.json", "r", encoding="utf-8") as file:
            existing_data = json.load(file)

        threats_list = [] 
        for dictionary in existing_data:
            for key in dictionary.keys():
                threats_list.append(key)

        if self.threat in threats_list:
            for dictionary in existing_data:
                if self.threat in dictionary:
                    return dictionary[self.threat]
        else:
            return "No data"
