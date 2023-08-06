from dataclasses import dataclass
from typing import List, Optional

from lakey_finicity.models.report.report_constraints import ReportConstraints
from lakey_finicity.models.report.report_status import ReportStatus
from lakey_finicity.models.report.report_type import ReportType
from lakey_finicity.models.report.voi.income_record import IncomeRecord
from lakey_finicity.models.report.voi.voi_institution_record import VoiInstitutionRecord


@dataclass
class VoiReport(object):
    id: str  # ID of the report (UUID with max length 32 characters).
    portfolioId: str
    requestId: str  # unique requestId for this specific call request
    title: str
    consumerId: str  # ID of the consumer (UUID with max length 32 characters)
    consumerSsn: str  # Last 4 digits of the report consumer's Social Security number
    requesterName: str
    constraints: Optional[ReportConstraints]
    type: ReportType  # voa or voi
    status: ReportStatus  # inProgress or success or failure
    createdDate: int
    startDate: Optional[int]
    endDate: Optional[int]
    days: Optional[int]
    seasoned: Optional[bool]
    institutions: Optional[List[VoiInstitutionRecord]]
    income: Optional[List[IncomeRecord]]
    customerId: Optional[str]  # TODO see if this is really optional
    customerType: Optional[str]  # TODO see if this is really optional
    _unused_fields: dict  # this is for forward compatibility and should be empty

    @staticmethod
    def from_dict(data: dict):
        data = dict(data)  # don't mutate the original
        id = data.pop('id')
        if id[-4:] == '-voi':
            id = id[:-4]
        requestId = data.pop('requestId')
        portfolioId = data.pop('portfolioId')
        title = data.pop('title')
        consumerId = data.pop('consumerId')
        consumerSsn = data.pop('consumerSsn')
        type = data.pop('type')
        constraints_raw = data.pop('constraints')
        requesterName = data.pop('requesterName')
        constraints = ReportConstraints.from_dict(constraints_raw) if constraints_raw else None
        status = data.pop('status')
        createdDate = data.pop('createdDate')
        startDate = data.pop('startDate', None)
        endDate = data.pop('endDate', None)
        days = data.pop('days', None)
        seasoned = data.pop('seasoned', None)
        institutions_raw = data.pop('institutions', None)
        institutions = [VoiInstitutionRecord.from_dict(d) for d in institutions_raw] if institutions_raw else None
        income_raw = data.pop('income', None)
        income = [IncomeRecord.from_dict(d) for d in income_raw] if income_raw else None
        customer_id = data.pop('customerId', None)
        customer_type = data.pop('customerType', None)
        return VoiReport(
            id=id,
            portfolioId=portfolioId,
            requestId=requestId,
            title=title,
            consumerId=consumerId,
            consumerSsn=consumerSsn,
            requesterName=requesterName,
            constraints=constraints,
            type=type,
            status=status,
            createdDate=createdDate,
            startDate=startDate,
            endDate=endDate,
            days=days,
            seasoned=seasoned,
            institutions=institutions,
            income=income,
            customerId=customer_id,
            customerType=customer_type,
            _unused_fields=data,
        )

    #
    # id: str  # ID of the report (UUID with max length 32 characters).  VOI report ID will have “-voi” appended to the end of it to denote the report type.
    # portfolioId: str
    # requestId: str  # unique requestId for this specific call request
    # title: str
    # consumerId: str  # ID of the consumer (UUID with max length 32 characters)
    # consumerSsn: str  # Last 4 digits of the report consumer's Social Security number
    # requesterName: str
    # constraints: Optional[ReportConstraints]
    # type: ReportType  # voa or voi
    # status: ReportStatus  # inProgress or success or failure
    # _unused_fields: dict  # this is for forward compatibility and should be empty
    # institutions: Optional[List[InstitutionRecord]]
    #
    # customerId: Optional[str]
    #
    # startDate: int
    # endDate: int
    # days: int
    # seasoned: bool

#
# @dataclass
# class Report(object):
#     id: str  # ID of the report (UUID with max length 32 characters).  VOI report ID will have “-voi” appended to the end of it to denote the report type.
#     requestId: str  # unique requestId for this specific call request
#     consumerId: str  # ID of the consumer (UUID with max length 32 characters)
#     consumerSsn: str  # Last 4 digits of the report consumer's Social Security number
#     type: ReportType  # voa or voi
#     requesterName: str
#     constraints: Optional[ReportConstraints]
#     status: ReportStatus  # inProgress or success or failure
#     _unused_fields: dict  # this is for forward compatibility and should be empty
#     institutions: Optional[List[InstitutionRecord]]
#
#     customerId: Optional[str]
#     createdDate: int
#
#     portfolioId: str
#     title: str
#     startDate: int
#     endDate: int
#     days: int
#     seasoned: bool
#
#     @staticmethod
#     def from_dict(data: dict):
#         data = dict(data)  # don't mutate the original
#         id = data.pop('id')
#         requestId = data.pop('requestId')
#         consumerId = data.pop('consumerId')
#         consumerSsn = data.pop('consumerSsn')
#         type = data.pop('type')
#         constraints_raw = data.pop('constraints')
#         constraints = ReportConstraints.from_dict(constraints_raw) if constraints_raw else None
#         status = data.pop('status')
#         institutions_raw = data.pop('institutions', None)
#         institutions = [InstitutionRecord.from_dict(d) for d in institutions_raw] if institutions_raw else None
#         return Report(
#             id=id,
#             requestId=requestId,
#             consumerId=consumerId,
#             consumerSsn=consumerSsn,
#             type=type,
#             constraints=constraints,
#             status=status,
#             institutions=institutions,
#             _unused_fields=data,
#         )
#
#
#     id: str  # ID of the report (UUID with max length 32 characters).  VOI report ID will have “-voi” appended to the end of it to denote the report type.
#     portfolioId: str
#     requestId: str  # unique requestId for this specific call request
#     title: str
#     consumerId: str  # ID of the consumer (UUID with max length 32 characters)
#     consumerSsn: str  # Last 4 digits of the report consumer's Social Security number
#     requesterName: str
#     constraints: Optional[ReportConstraints]
#     type: ReportType  # voa or voi
#     status: ReportStatus  # inProgress or success or failure
#     _unused_fields: dict  # this is for forward compatibility and should be empty
#     institutions: Optional[List[InstitutionRecord]]
#
#     customerId: Optional[str]
#
#     startDate: int
#     endDate: int
#     days: int
#     seasoned: bool
#
#
# @dataclass
# class VoiReport(Report):
#     _unused_fields: dict  # this is for forward compatibility and should be empty
#     pass
#     # income
#
#
#     # assets
#
#
#     @staticmethod
#     def from_dict(data: dict):
#         return VoiReport(
#             data = dict(data)  # don't mutate the original
#             _unused_fields=data,
#
#         )
