import asyncio
from atlassian import Jira
from typing import Optional

from models.ticket import Ticket
from schemas.ticket import TicketCreate, TicketResponse
from utils.jira_issue import JiraIssue


# jira_options = {'server': cfg.jira_server}
# jira = JIRA(options=jira_options, basic_auth=(cfg.jira_user, cfg.jira_api))

class JiraService:
    def __init__(self, jira_client: Jira, project_key: str = "SD"):
        self.jira = jira_client
        self.project_key = project_key

    async def create_issue(self, ticket: TicketCreate):
        fields = self.create_data(ticket)
        return await asyncio.to_thread(self._create_issue_sync, fields, ticket.tg_user_id)

    def _create_issue_sync(self, fields: dict, tg_user_id: int) -> Optional[TicketResponse]:
        try:
            issue = self.jira.create_issue(fields=fields)
        except Exception as e:
            return None #log
        else:
            issue = JiraIssue.from_dict(issue)
            ticket = TicketResponse.model_validate(issue.work_data(tg_user_id))
            return ticket

    def create_data(self, ticket: TicketCreate) -> dict:
        data = dict(
            summary=ticket.title,
            project=dict(key=self.project_key),
            issuetype=dict(id=ticket.issue_type.service),
            description=ticket.description
        )
        return data
