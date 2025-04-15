from atlassian import Jira
from cfg import cfg

from .jira_service import JiraService
from .ticket_service import TicketService
from .auth_service import AuthService


jira = Jira(
    url=cfg.jira_server,
    token=cfg.jira_api,
    verify_ssl=False
)

jira_service = JiraService(jira)

ticket_service = TicketService(jira_service)

auth_service = AuthService()

__all__ = ['jira_service', 'ticket_service', 'auth_service']
