#

from atlassian import Jira
from services.jira_service import JiraService
from repositories.redis_repository import RedisRepository
from cfg import cfg


class TicketServiceSuperset:

    jira = Jira(
        url=cfg.jira_server,
        token=cfg.jira_api,
        verify_ssl=False
    )

    jira_service = JiraService(jira)

    redis_repository = RedisRepository(f'{cfg.redis_base}:{cfg.redis_port}')
