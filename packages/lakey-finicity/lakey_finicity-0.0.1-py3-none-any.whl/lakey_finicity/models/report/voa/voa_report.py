from dataclasses import dataclass
from typing import List, Optional

from lakey_finicity.models.report.report_constraints import ReportConstraints
from lakey_finicity.models.report.report_status import ReportStatus
from lakey_finicity.models.report.report_type import ReportType
from lakey_finicity.models.report.voa.asset_record import AssetRecord
from lakey_finicity.models.report.voa.voa_institution_record import VoaInstitutionRecord


@dataclass
class VoaReport(object):
    id: str  # ID of the report (UUID with max length 32 characters).  VOI report ID will have “-voi” appended to the end of it to denote the report type.
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
    startDate: int
    endDate: int
    days: int
    seasoned: bool
    institutions: Optional[List[VoaInstitutionRecord]]
    assets: AssetRecord
    _unused_fields: dict  # this is for forward compatibility and should be empty

    @staticmethod
    def from_dict(data: dict):
        data = dict(data)  # don't mutate the original
        id = data.pop('id')
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
        startDate = data.pop('startDate')
        endDate = data.pop('endDate')
        days = data.pop('days')
        seasoned = data.pop('seasoned')
        institutions_raw = data.pop('institutions', None)
        institutions = [VoaInstitutionRecord.from_dict(d) for d in institutions_raw] if institutions_raw else None
        assets_raw = data.pop('assets')
        assets = AssetRecord.from_dict(assets_raw)
        return VoaReport(
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
            assets=assets,
            _unused_fields=data,
        )
