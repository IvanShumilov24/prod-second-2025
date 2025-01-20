from solution.app.business.models import BusinessModel


class BusinessDAO(BaseDAO[BusinessModel, BusinessCreateDB, BusinessUpdateDB]):
    model = BussinesModel
