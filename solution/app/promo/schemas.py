from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, UUID4, ConfigDict
from pydantic_extra_types.country import CountryAlpha2


class PromoMode(Enum):
    COMMON = "COMMON"
    UNIQUE = 'UNIQUE'


class Target(BaseModel):
    age_from: int = Field(ge=0, le=100)
    age_until: int = Field(ge=0, le=100)
    country: CountryAlpha2
    categories: list[str]

    @field_validator('categories')
    def validate_categories(cls, categories):
        for category in categories:
            if not (2 <= len(category) <= 20):
                raise ValueError("Длина категории должна быть от 2 до 20 символов")
        return categories

    @field_validator('age_from')
    def validate_age_from(cls, age_from, values):
        if 'age_until' in values.data and values['age_until'] is not None:
            if age_from > values['age_until']:
                raise ValueError("age_from не должен превышать age_until.")
        return age_from


class Promo(BaseModel):
    description: str = Field(max_length=300, min_length=10)
    image_url: str = Field(max_length=350)
    target: Target
    max_count: int
    active_from: date
    active_until: date
    mode: PromoMode
    promo_common: str = Field(min_length=5, max_length=30)
    promo_unique: list[str] = Field(default_factory=list, max_length=5000, min_length=1)
    promo_id: UUID4
    company_id: UUID4
    company_name: str = Field(max_length=50, min_length=5)
    like_count: int = Field(default=0)
    used_count: int = Field(default=0)
    active: bool = Field(default=True)

    @field_validator('active')
    def validate_active(cls, active, values):
        model_config = ConfigDict(from_attributes=True)
        if not active:
            return False

        now = datetime.now().date()

        active_from = values.data.get("active_from")
        active_until = values.data.get("active_until")

        if active_from and active_until:
            if not (active_from <= now <= active_until):
                return False
        elif active_from and now < active_from:
            return False
        elif active_until and now > active_until:
            return False

        return True

    @field_validator("promo_unique")
    def validate_promo_unique(cls, promo_unique):
        for promo in promo_unique:
            if len(promo) > 30:
                raise ValueError("Длина промокода не может превышать 30 символов")
        return promo_unique


class PromoBase(BaseModel):
    description: str = Field(max_length=300, min_length=10)
    image_url: str = Field(max_length=350)
    target: Target
    max_count: int
    active_from: date
    active_until: date


class PromoCreate(PromoBase):
    mode: PromoMode
    promo_common: str = Field(min_length=5, max_length=30)
    promo_unique: list[str] = Field(default_factory=list, max_length=5000, min_length=1)

    @field_validator("promo_unique")
    def validate_promo_unique(cls, promo_unique):
        for promo in promo_unique:
            if len(promo) > 30:
                raise ValueError("Длина промокода не может превышать 30 символов")
        return promo_unique

    # @field_validator('promo_common', 'promo_unique', mode='after')
    # def validate_promo_fields(cls, value: Any, info: FieldSerializationInfo):
    #     mode = info.context.get('mode')
    #     if mode is None:
    #         raise ValueError("Mode must be provided in context")
    #     field_name = info.field_name
    #     if mode == PromoMode.COMMON and field_name == 'promo_common':
    #         if value is None:
    #             raise ValueError("For 'common' mode 'promo_common' field is required")
    #         return value
    #     elif mode == PromoMode.COMMON and field_name == 'promo_unique' and value:
    #         raise ValueError("For 'common' mode 'promo_unique' field must be empty")
    #
    #     if mode == PromoMode.UNIQUE and field_name == 'promo_unique':
    #         if not value:
    #             raise ValueError("For 'unique' mode 'promo_unique' field is required")
    #         return value
    #
    #     elif mode == PromoMode.UNIQUE and field_name == 'promo_common' and value is not None:
    #         raise ValueError("For 'unique' mode 'promo_common' field must be empty")
    #
    #     return value
    #
    #
    # @model_validator(mode='before')
    # def validate_before_model(cls, values):
    #     mode = values.get('mode')
    #     if mode is None:
    #         raise ValueError("Mode must be provided")
    #     return values


class PromoCreateDB(PromoBase):
    mode: PromoMode
    promo_common: str = Field(min_length=5, max_length=30)
    promo_unique: list[str] = Field(default_factory=list, max_length=5000, min_length=1)
    company_id: UUID4
    company_name: str = Field(max_length=50, min_length=5)
    like_count: int = Field(default=0)
    used_count: int = Field(default=0)
    active: bool = Field(default=True)

    @field_validator("promo_unique")
    def validate_promo_unique(cls, promo_unique):
        for promo in promo_unique:
            if len(promo) > 30:
                raise ValueError("Длина промокода не может превышать 30 символов")
        return promo_unique


class PromoUpdate(PromoBase):
    pass


class PromoForUser(PromoBase):
    model_config = ConfigDict(from_attributes=True)

    promo_id: UUID4
    company_id: UUID4
    company_name: str = Field(max_length=50, min_length=5)
    active: bool = Field(default=True)
    like_count: int = Field(default=0)
    is_activated_by_user: bool
    is_liked_by_user: bool
    comment_count: int = Field(default=0)


class PromoStat(BaseModel):
    activate_count: int
    countries: list[dict[str, int]]


class PromoCreatedResponse(BaseModel):
    id: UUID4
