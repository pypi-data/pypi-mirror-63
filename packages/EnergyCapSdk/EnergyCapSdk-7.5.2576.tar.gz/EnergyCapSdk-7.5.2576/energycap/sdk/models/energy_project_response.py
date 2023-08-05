# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EnergyProjectResponse(Model):
    """EnergyProjectResponse.

    :param energy_project_id: The energy project identifier
    :type energy_project_id: int
    :param energy_project_code: The energy project code <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span> <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 32 characters</span>
    :type energy_project_code: str
    :param energy_project_info: The energy project info <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 50 characters</span> <span
     class='property-internal'>Required</span> <span
     class='property-internal'>Must be between 0 and 50 characters</span>
    :type energy_project_info: str
    :param installation_begin_date: The energy project installation begin date
    :type installation_begin_date: datetime
    :param installation_end_date: The energy project installation end date
    :type installation_end_date: datetime
    :param installation_cost: The energy project installation cost
    :type installation_cost: float
    :param utility_rebate: The rebate amount of energy project
    :type utility_rebate: float
    :param funding_source: The funding source of the project
    :type funding_source: str
    :param project_manager: The project manager of the energy project
    :type project_manager: str
    :param note: The miscellenous note about the project
    :type note: str
    :param energy_savings: The energy savings
    :type energy_savings: ~energycap.sdk.models.EnergySavingsChild
    :param cost_savings: The cost savings
    :type cost_savings: ~energycap.sdk.models.CostSavingsChild
    :param place: The place of the energy project
    :type place: ~energycap.sdk.models.EnergyProjectPlaceChild
    :param energy_project_type: The project type of the energy project
    :type energy_project_type: ~energycap.sdk.models.EnergyProjectType
    """

    _validation = {
        'energy_project_code': {'required': True, 'max_length': 32, 'min_length': 0},
        'energy_project_info': {'required': True, 'max_length': 50, 'min_length': 0},
    }

    _attribute_map = {
        'energy_project_id': {'key': 'energyProjectId', 'type': 'int'},
        'energy_project_code': {'key': 'energyProjectCode', 'type': 'str'},
        'energy_project_info': {'key': 'energyProjectInfo', 'type': 'str'},
        'installation_begin_date': {'key': 'installationBeginDate', 'type': 'iso-8601'},
        'installation_end_date': {'key': 'installationEndDate', 'type': 'iso-8601'},
        'installation_cost': {'key': 'installationCost', 'type': 'float'},
        'utility_rebate': {'key': 'utilityRebate', 'type': 'float'},
        'funding_source': {'key': 'fundingSource', 'type': 'str'},
        'project_manager': {'key': 'projectManager', 'type': 'str'},
        'note': {'key': 'note', 'type': 'str'},
        'energy_savings': {'key': 'energySavings', 'type': 'EnergySavingsChild'},
        'cost_savings': {'key': 'costSavings', 'type': 'CostSavingsChild'},
        'place': {'key': 'place', 'type': 'EnergyProjectPlaceChild'},
        'energy_project_type': {'key': 'energyProjectType', 'type': 'EnergyProjectType'},
    }

    def __init__(self, energy_project_code, energy_project_info, energy_project_id=None, installation_begin_date=None, installation_end_date=None, installation_cost=None, utility_rebate=None, funding_source=None, project_manager=None, note=None, energy_savings=None, cost_savings=None, place=None, energy_project_type=None):
        super(EnergyProjectResponse, self).__init__()
        self.energy_project_id = energy_project_id
        self.energy_project_code = energy_project_code
        self.energy_project_info = energy_project_info
        self.installation_begin_date = installation_begin_date
        self.installation_end_date = installation_end_date
        self.installation_cost = installation_cost
        self.utility_rebate = utility_rebate
        self.funding_source = funding_source
        self.project_manager = project_manager
        self.note = note
        self.energy_savings = energy_savings
        self.cost_savings = cost_savings
        self.place = place
        self.energy_project_type = energy_project_type
