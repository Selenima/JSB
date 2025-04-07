import asyncio
from jira import JIRA
from typing import Optional

# jira_options = {'server': cfg.jira_server}
# jira = JIRA(options=jira_options, basic_auth=(cfg.jira_user, cfg.jira_api))

class JiraService:
    def __init__(self, jira_client: JIRA, project_key: str = "SD", issue_type: str = "Task"):
        self.jira = jira_client
        self.project_key = project_key
        self.issue_type = issue_type

    async def create_issue(self, title: str, description: str) -> Optional[str]:
        return await asyncio.to_thread(self._create_issue_sync, title, description)

    def _create_issue_sync(self, title: str, description: str) -> str:
        issue = self.jira.create_issue(
            project={"key": self.project_key},
            summary=title,
            description=description,
            issuetype={"name": self.issue_type}
        )
        return issue.key