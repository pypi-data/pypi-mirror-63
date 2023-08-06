from dataclasses import dataclass


# https://community.finicity.com/s/article/Get-Account-Owner
@dataclass
class AccountOwner(object):
    ownerName: str
    ownerAddress: str
    asOfDate: int
    _unused_fields: dict  # this is for forward compatibility and should be empty

    @staticmethod
    def from_dict(data: dict):
        data = dict(data)  # don't mutate the original
        ownerName = data.pop('ownerName')
        ownerAddress = data.pop('ownerAddress')
        asOfDate = data.pop('asOfDate')
        return AccountOwner(
            ownerName=ownerName,
            ownerAddress=ownerAddress,
            asOfDate=-asOfDate,
            _unused_fields=data,
        )
