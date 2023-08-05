# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CostSavingsChild(Model):
    """CostSavingsChild.

    :param cost_savings: The cost savings amount
    :type cost_savings: float
    :param cost_savings_unit: The cost savings unit
    :type cost_savings_unit: ~energycap.sdk.models.CostSavingsUnit
    """

    _attribute_map = {
        'cost_savings': {'key': 'costSavings', 'type': 'float'},
        'cost_savings_unit': {'key': 'costSavingsUnit', 'type': 'CostSavingsUnit'},
    }

    def __init__(self, cost_savings=None, cost_savings_unit=None):
        super(CostSavingsChild, self).__init__()
        self.cost_savings = cost_savings
        self.cost_savings_unit = cost_savings_unit
