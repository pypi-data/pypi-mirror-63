# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ListIds(Model):
    """ListIds.

    :param ids:
    :type ids: list[int]
    """

    _attribute_map = {
        'ids': {'key': 'ids', 'type': '[int]'},
    }

    def __init__(self, ids=None):
        super(ListIds, self).__init__()
        self.ids = ids
