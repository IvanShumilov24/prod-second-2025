from app.business.models import BusinessModel
from app.business.schemas import BusinessCreateDB, BusinessUpdateDB
from app.dao import BaseDAO


class BusinessDAO(BaseDAO[BusinessModel, BusinessCreateDB, BusinessUpdateDB]):
    model = BusinessModel
