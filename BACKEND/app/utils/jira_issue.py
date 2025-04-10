from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class AvatarUrls:
    size_48x48: str
    size_24x24: str
    size_16x16: str
    size_32x32: str

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'AvatarUrls':
        return cls(
            size_48x48=data.get('48x48'),
            size_24x24=data.get('24x24'),
            size_16x16=data.get('16x16'),
            size_32x32=data.get('32x32')
        )

@dataclass
class User:
    self: str
    name: str
    key: str
    email_address: str
    avatar_urls: AvatarUrls
    display_name: str
    active: bool
    time_zone: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        return cls(
            self=data.get('self'),
            name=data.get('name'),
            key=data.get('key'),
            email_address=data.get('emailAddress'),
            avatar_urls=AvatarUrls.from_dict(data.get('avatarUrls', {})),
            display_name=data.get('displayName'),
            active=data.get('active'),
            time_zone=data.get('timeZone')
        )

@dataclass
class CustomFieldOption:
    self: str
    value: str
    id: str
    disabled: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomFieldOption':
        return cls(
            self=data.get('self'),
            value=data.get('value'),
            id=data.get('id'),
            disabled=data.get('disabled')
        )

@dataclass
class Priority:
    self: str
    icon_url: str
    name: str
    id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Priority':
        return cls(
            self=data.get('self'),
            icon_url=data.get('iconUrl'),
            name=data.get('name'),
            id=data.get('id')
        )

@dataclass
class StatusCategory:
    self: str
    id: int
    key: str
    color_name: str
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StatusCategory':
        return cls(
            self=data.get('self'),
            id=data.get('id'),
            key=data.get('key'),
            color_name=data.get('colorName'),
            name=data.get('name')
        )

@dataclass
class Status:
    self: str
    description: str
    icon_url: str
    name: str
    id: str
    status_category: StatusCategory

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Status':
        return cls(
            self=data.get('self'),
            description=data.get('description'),
            icon_url=data.get('iconUrl'),
            name=data.get('name'),
            id=data.get('id'),
            status_category=StatusCategory.from_dict(data.get('statusCategory', {}))
        )

@dataclass
class Progress:
    progress: int
    total: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Progress':
        return cls(
            progress=data.get('progress', 0),
            total=data.get('total', 0)
        )

@dataclass
class Votes:
    self: str
    votes: int
    has_voted: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Votes':
        return cls(
            self=data.get('self'),
            votes=data.get('votes', 0),
            has_voted=data.get('hasVoted', False)
        )

@dataclass
class Worklog:
    start_at: int
    max_results: int
    total: int
    worklogs: List[Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Worklog':
        return cls(
            start_at=data.get('startAt', 0),
            max_results=data.get('maxResults', 0),
            total=data.get('total', 0),
            worklogs=data.get('worklogs', [])
        )

@dataclass
class IssueType:
    self: str
    id: str
    description: str
    icon_url: str
    name: str
    subtask: bool
    avatar_id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IssueType':
        return cls(
            self=data.get('self'),
            id=data.get('id'),
            description=data.get('description'),
            icon_url=data.get('iconUrl'),
            name=data.get('name'),
            subtask=data.get('subtask', False),
            avatar_id=data.get('avatarId')
        )

@dataclass
class ProjectCategory:
    self: str
    id: str
    description: str
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectCategory':
        return cls(
            self=data.get('self'),
            id=data.get('id'),
            description=data.get('description'),
            name=data.get('name')
        )

@dataclass
class Project:
    self: str
    id: str
    key: str
    name: str
    project_type_key: str
    avatar_urls: AvatarUrls
    project_category: ProjectCategory

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        return cls(
            self=data.get('self'),
            id=data.get('id'),
            key=data.get('key'),
            name=data.get('name'),
            project_type_key=data.get('projectTypeKey'),
            avatar_urls=AvatarUrls.from_dict(data.get('avatarUrls', {})),
            project_category=ProjectCategory.from_dict(data.get('projectCategory', {}))
        )

@dataclass
class Watches:
    self: str
    watch_count: int
    is_watching: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Watches':
        return cls(
            self=data.get('self'),
            watch_count=data.get('watchCount', 0),
            is_watching=data.get('isWatching', False)
        )

@dataclass
class TimeTracking:
    original_estimate: Optional[str] = None
    remaining_estimate: Optional[str] = None
    time_spent: Optional[str] = None
    original_estimate_seconds: Optional[int] = None
    remaining_estimate_seconds: Optional[int] = None
    time_spent_seconds: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimeTracking':
        return cls(**data)

@dataclass
class CommentList:
    comments: List[Any]
    max_results: int
    total: int
    start_at: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CommentList':
        return cls(
            comments=data.get('comments', []),
            max_results=data.get('maxResults', 0),
            total=data.get('total', 0),
            start_at=data.get('startAt', 0)
        )

@dataclass
class JiraIssueFields:
    fix_versions: List[Any]
    organizations: List[Any]  # customfield_10110
    satisfaction: Optional[Any]  # customfield_10111
    user_id: Optional[Any]  # customfield_11200
    resolution: Optional[Any]
    satisfaction_date: Optional[Any]  # customfield_10112
    linked_major_incidents: Optional[Any]  # customfield_10500
    sprint: Optional[Any]  # customfield_10105
    groups: List[Any]  # customfield_10501
    business_approval: Optional[Any]  # customfield_10502
    approvals: Optional[Any]  # customfield_10107
    request_participants: List[User]  # customfield_10108
    issue_function: Optional[Any]  # customfield_10900
    customer_request_type: Optional[Any]  # customfield_10109
    release_date: Optional[Any]  # customfield_10903
    service_product: Optional[CustomFieldOption]  # customfield_10904
    branch: Optional[Any]  # customfield_10905
    problematic_server_pacs: Optional[Any]  # customfield_10906
    additional_info: Optional[Any]  # customfield_10907
    contact_feedback: Optional[Any]  # customfield_10908
    employees: Optional[Any]  # customfield_10909
    last_viewed: Optional[str]
    priority: Priority
    rank: str  # customfield_10100
    epic_link: Optional[Any]  # customfield_10101
    labels: List[str]
    time_estimate: Optional[int]
    aggregate_time_original_estimate: Optional[int]
    versions: List[Any]
    issue_links: List[Any]
    assignee: Optional[User]
    status: Status
    components: List[Any]
    analyst: Optional[Any]  # customfield_11420
    tester_cost_estimate: Optional[Any]  # customfield_11300
    queue: Optional[Any]  # customfield_11301
    archived_date: Optional[str]
    license_installation_location: Optional[Any]  # customfield_11302
    sysadmin_cost_estimate: Optional[Any]  # customfield_10324
    system: Optional[Any]  # customfield_11414
    ice: Optional[Any]  # customfield_11413
    program_increment: Optional[Any]  # customfield_10600
    business_owners: Optional[Any]  # customfield_10325
    end_date: Optional[Any]  # customfield_10601
    deadline: Optional[Any]  # customfield_11416
    curator_approval: Optional[Any]  # customfield_10326
    baseline_start_date: Optional[Any]  # customfield_10602
    owner: Optional[Any]  # customfield_11415
    baseline_end_date: Optional[Any]  # customfield_10603
    success_metrics: Optional[Any]  # customfield_11418
    aggregate_time_estimate: Optional[int]
    task_mode: Optional[Any]  # customfield_10604
    budget: Optional[Any]  # customfield_11417
    task_progress: Optional[Any]  # customfield_10605
    risk_consequence: Optional[Any]  # customfield_10606
    system_multiselect: Optional[Any]  # customfield_11419
    risk_probability: Optional[Any]  # customfield_10607
    start_date: Optional[Any]  # customfield_10608
    creator: User
    subtasks: List[Any]
    reporter: User
    aggregate_progress: Progress
    impact: Optional[Any]  # customfield_11410
    time_to_approve_normal_change: Optional[Any]  # customfield_10320
    product: Optional[Any]  # customfield_10200
    initiator: Optional[Any]  # customfield_10201
    easy: Optional[Any]  # customfield_11412
    analyst_cost_estimate: Optional[Any]  # customfield_10322
    confidence: Optional[Any]  # customfield_11411
    developer_cost_estimate: Optional[Any]  # customfield_10323
    root_cause: Optional[Any]  # customfield_10313
    install_inobitec: Optional[Any]  # customfield_11403
    workaround: Optional[Any]  # customfield_10314
    inobitec_product_code: Optional[Any]  # customfield_11402
    change_managers: Optional[Any]  # customfield_10315
    license_number: Optional[Any]  # customfield_11405
    cab: Optional[Any]  # customfield_10316
    previous_owner_fio: Optional[Any]  # customfield_11404
    time_to_resolution: Optional[Any]  # customfield_10317
    module: Optional[Any]  # customfield_11407
    time_to_first_response: Optional[Any]  # customfield_10318
    position: Optional[Any]  # customfield_11406
    time_to_close_after_resolution: Optional[Any]  # customfield_10319
    legal_entity: Optional[Any]  # customfield_11409
    department: Optional[Any]  # customfield_11408
    progress: Progress
    votes: Votes
    worklog: Worklog
    archived_by: Optional[Any]
    issue_type: IssueType
    time_spent: Optional[int]
    project: Project
    initiator_user: Optional[Any]  # customfield_11000
    influence: Optional[Any]  # customfield_11001
    aggregate_time_spent: Optional[int]
    operational_categorization: Optional[Any]  # customfield_10310
    source: Optional[Any]  # customfield_10311
    license_user: Optional[Any]  # customfield_11401
    investigation_reason: Optional[Any]  # customfield_10312
    license_owner_legal_entity: Optional[Any]  # customfield_11400
    impact_list: Optional[Any]  # customfield_10302
    change_type: Optional[Any]  # customfield_10303
    change_risk: Optional[Any]  # customfield_10304
    start_date_alt: Optional[Any]  # customfield_10700
    change_reason: Optional[Any]  # customfield_10305
    agreement: Optional[Any]  # customfield_10701
    start_datetime: Optional[Any]  # customfield_10306
    end_datetime: Optional[Any]  # customfield_10307
    urgency: Optional[Any]  # customfield_10308
    resolution_date: Optional[str]
    product_categorization: Optional[Any]  # customfield_10309
    work_ratio: int
    watches: Watches
    created: datetime
    pending_reason: Optional[Any]  # customfield_10300
    approvers: Optional[Any]  # customfield_10301
    updated: datetime
    time_original_estimate: Optional[int]
    description: str
    flagged: Optional[Any]  # customfield_11100
    time_tracking: TimeTracking
    parent_link: Optional[Any]  # customfield_10401
    target_start: Optional[Any]  # customfield_10402
    target_end: Optional[Any]  # customfield_10403
    original_story_points: Optional[Any]  # customfield_10404
    risks: Optional[Any]  # customfield_10800
    attachment: List[Any]
    milestones: Optional[Any]  # customfield_10801
    summary: str
    development: str  # customfield_10000
    team: Optional[Any]  # customfield_10400
    environment: Optional[Any]
    desired_completion_date: Optional[Any]  # customfield_10910
    due_date: Optional[str]
    comment: CommentList

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JiraIssueFields':
        return cls(
            fix_versions=data.get('fixVersions', []),
            organizations=data.get('customfield_10110', []),
            satisfaction=data.get('customfield_10111'),
            user_id=data.get('customfield_11200'),
            resolution=data.get('resolution'),
            satisfaction_date=data.get('customfield_10112'),
            linked_major_incidents=data.get('customfield_10500'),
            sprint=data.get('customfield_10105'),
            groups=data.get('customfield_10501', []),
            business_approval=data.get('customfield_10502'),
            approvals=data.get('customfield_10107'),
            request_participants=[User.from_dict(user) for user in data.get('customfield_10108', [])],
            issue_function=data.get('customfield_10900'),
            customer_request_type=data.get('customfield_10109'),
            release_date=data.get('customfield_10903'),
            service_product=CustomFieldOption.from_dict(data['customfield_10904']) if data.get('customfield_10904') else None,
            branch=data.get('customfield_10905'),
            problematic_server_pacs=data.get('customfield_10906'),
            additional_info=data.get('customfield_10907'),
            contact_feedback=data.get('customfield_10908'),
            employees=data.get('customfield_10909'),
            last_viewed=data.get('lastViewed'),
            priority=Priority.from_dict(data.get('priority', {})),
            rank=data.get('customfield_10100'),
            epic_link=data.get('customfield_10101'),
            labels=data.get('labels', []),
            time_estimate=data.get('timeestimate'),
            aggregate_time_original_estimate=data.get('aggregatetimeoriginalestimate'),
            versions=data.get('versions', []),
            issue_links=data.get('issuelinks', []),
            assignee=User.from_dict(data['assignee']) if data.get('assignee') else None,
            status=Status.from_dict(data.get('status', {})),
            components=data.get('components', []),
            analyst=data.get('customfield_11420'),
            tester_cost_estimate=data.get('customfield_11300'),
            queue=data.get('customfield_11301'),
            archived_date=data.get('archiveddate'),
            license_installation_location=data.get('customfield_11302'),
            sysadmin_cost_estimate=data.get('customfield_10324'),
            system=data.get('customfield_11414'),
            ice=data.get('customfield_11413'),
            program_increment=data.get('customfield_10600'),
            business_owners=data.get('customfield_10325'),
            end_date=data.get('customfield_10601'),
            deadline=data.get('customfield_11416'),
            curator_approval=data.get('customfield_10326'),
            baseline_start_date=data.get('customfield_10602'),
            owner=data.get('customfield_11415'),
            baseline_end_date=data.get('customfield_10603'),
            success_metrics=data.get('customfield_11418'),
            aggregate_time_estimate=data.get('aggregatetimeestimate'),
            task_mode=data.get('customfield_10604'),
            budget=data.get('customfield_11417'),
            task_progress=data.get('customfield_10605'),
            risk_consequence=data.get('customfield_10606'),
            system_multiselect=data.get('customfield_11419'),
            risk_probability=data.get('customfield_10607'),
            start_date=data.get('customfield_10608'),
            creator=User.from_dict(data.get('creator', {})),
            subtasks=data.get('subtasks', []),
            reporter=User.from_dict(data.get('reporter', {})),
            aggregate_progress=Progress.from_dict(data.get('aggregateprogress', {})),
            impact=data.get('customfield_11410'),
            time_to_approve_normal_change=data.get('customfield_10320'),
            product=data.get('customfield_10200'),
            initiator=data.get('customfield_10201'),
            easy=data.get('customfield_11412'),
            analyst_cost_estimate=data.get('customfield_10322'),
            confidence=data.get('customfield_11411'),
            developer_cost_estimate=data.get('customfield_10323'),
            root_cause=data.get('customfield_10313'),
            install_inobitec=data.get('customfield_11403'),
            workaround=data.get('customfield_10314'),
            inobitec_product_code=data.get('customfield_11402'),
            change_managers=data.get('customfield_10315'),
            license_number=data.get('customfield_11405'),
            cab=data.get('customfield_10316'),
            previous_owner_fio=data.get('customfield_11404'),
            time_to_resolution=data.get('customfield_10317'),
            module=data.get('customfield_11407'),
            time_to_first_response=data.get('customfield_10318'),
            position=data.get('customfield_11406'),
            time_to_close_after_resolution=data.get('customfield_10319'),
            legal_entity=data.get('customfield_11409'),
            department=data.get('customfield_11408'),
            progress=Progress.from_dict(data.get('progress', {})),
            votes=Votes.from_dict(data.get('votes', {})),
            worklog=Worklog.from_dict(data.get('worklog', {})),
            archived_by=data.get('archivedby'),
            issue_type=IssueType.from_dict(data.get('issuetype', {})),
            time_spent=data.get('timespent'),
            project=Project.from_dict(data.get('project', {})),
            initiator_user=data.get('customfield_11000'),
            influence=data.get('customfield_11001'),
            aggregate_time_spent=data.get('aggregatetimespent'),
            operational_categorization=data.get('customfield_10310'),
            source=data.get('customfield_10311'),
            license_user=data.get('customfield_11401'),
            investigation_reason=data.get('customfield_10312'),
            license_owner_legal_entity=data.get('customfield_11400'),
            impact_list=data.get('customfield_10302'),
            change_type=data.get('customfield_10303'),
            change_risk=data.get('customfield_10304'),
            start_date_alt=data.get('customfield_10700'),
            change_reason=data.get('customfield_10305'),
            agreement=data.get('customfield_10701'),
            start_datetime=data.get('customfield_10306'),
            end_datetime=data.get('customfield_10307'),
            urgency=data.get('customfield_10308'),
            resolution_date=data.get('resolutiondate'),
            product_categorization=data.get('customfield_10309'),
            work_ratio=data.get('workratio', -1),
            watches=Watches.from_dict(data.get('watches', {})),
            created=datetime.fromisoformat(data['created'].replace('Z', '+00:00')) if data.get('created') else None,
            pending_reason=data.get('customfield_10300'),
            approvers=data.get('customfield_10301'),
            updated=datetime.fromisoformat(data['updated'].replace('Z', '+00:00')) if data.get('updated') else None,
            time_original_estimate=data.get('timeoriginalestimate'),
            description=data.get('description'),
            flagged=data.get('customfield_11100'),
            time_tracking=TimeTracking.from_dict(data.get('timetracking', {})),
            parent_link=data.get('customfield_10401'),
            target_start=data.get('customfield_10402'),
            target_end=data.get('customfield_10403'),
            original_story_points=data.get('customfield_10404'),
            risks=data.get('customfield_10800'),
            attachment=data.get('attachment', []),
            milestones=data.get('customfield_10801'),
            summary=data.get('summary'),
            development=data.get('customfield_10000'),
            team=data.get('customfield_10400'),
            environment=data.get('environment'),
            desired_completion_date=data.get('customfield_10910'),
            due_date=data.get('duedate'),
            comment=CommentList.from_dict(data.get('comment', {}))
        )

@dataclass
class JiraIssue:
    expand: str
    id: str
    self: str
    key: str
    fields: JiraIssueFields

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JiraIssue':
        return cls(
            expand=data.get('expand'),
            id=data.get('id'),
            self=data.get('self'),
            key=data.get('key'),
            fields=JiraIssueFields.from_dict(data.get('fields', {}))
        )

    def work_data(cls, tg_user_id: int):
        data = dict(
            tg_user_id=tg_user_id,
            jsd_id=cls.key,
            issue_type=cls.fields.issue_type.id,
            title=cls.fields.summary,
            description=cls.fields.description,
            status=cls.fields.status.id,
            service=cls.fields.service_product.id,
            comments=cls.fields.comment.comments
        )
        return data