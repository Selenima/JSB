import asyncio
from atlassian import Jira
from typing import Optional

from utils import auto_logger
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
            auto_logger.error(f'Issue creating: {e}')
            return None
        else:
            issue = self.jira.issue(issue.get('key'))
            auto_logger.debug(issue)
            issue = JiraIssue.from_dict(issue)
            auto_logger.debug(f'Issue created: {issue.key}')
            ticket = TicketResponse(
                id=None,
                tg_user_id=tg_user_id,
                jsd_id=issue.key,
                issue_type=int(issue.fields.issue_type.id),
                title=issue.fields.summary,
                description=issue.fields.description,
                status=int(issue.fields.status.id),
                service=0, #!
                comments=issue.fields.comment.comments
            )

            return ticket

    def create_data(self, ticket: TicketCreate) -> dict:
        data = dict(
            summary=ticket.title,
            project=dict(key=self.project_key),
            issuetype=dict(id=ticket.issue_type),
            description=ticket.description
        )
        return data
