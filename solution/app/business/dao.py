from solution.app.business.models import BusinessModel
from solution.app.business.schemas import BusinessCreateDB, BusinessUpdateDB
from solution.app.dao import BaseDAO


class BusinessDAO(BaseDAO[BusinessModel, BusinessCreateDB, BusinessUpdateDB]):
    model = BusinessModel
