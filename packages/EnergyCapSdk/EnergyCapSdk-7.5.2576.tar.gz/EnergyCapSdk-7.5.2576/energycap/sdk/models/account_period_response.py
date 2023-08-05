# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AccountPeriodResponse(Model):
    """AccountPeriodResponse.

    :param account_period_id: The account period identifier
    :type account_period_id: int
    :param period_number: The period number
    :type period_number: int
    :param name: The name of the period
    :type name: str
    """

    _attribute_map = {
        'account_period_id': {'key': 'accountPeriodId', 'type': 'int'},
        'period_number': {'key': 'periodNumber', 'type': 'int'},
        'name': {'key': 'name', 'type': 'str'},
    }

    def __init__(self, account_period_id=None, period_number=None, name=None):
        super(AccountPeriodResponse, self).__init__()
        self.account_period_id = account_period_id
        self.period_number = period_number
        self.name = name
