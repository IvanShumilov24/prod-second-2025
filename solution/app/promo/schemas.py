from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, UUID4


class PromoMode(Enum):
    COMMON = "COMMON"
    UNIQUE = 'UNIQUE'


class Target(BaseModel):
    age_from: int = Field(ge=0, le=100)
    age_until: int = Field(ge=0, le=100)
    country: str
    categories: list[str]

    @field_validator('categories')
    def validate_categories(cls, categories):
        for category in categories:
            if not (2 <= len(category) <= 20):
                raise ValueError("Длина категории должна быть от 2 до 20 символов")
        return categories

    @field_validator('age_from')
    def validate_age_from(cls, age_from, values):
        if 'age_until' in values and age_from > values['age_until']:
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
    company_id: UUID4
    company_name: str = Field(max_length=50, min_length=5)
    like_count: int = Field(default=0)
    used_count: int = Field(default=0)
    active: bool = Field(default=True)

    @field_validator('active')
    def validate_active(cls, active, values):
        if not active:
            return False

        now = datetime.now().date()

        if values.get("active_from") and values.get("active_until"):
            if not (values["active_from"] <= now <= values["active_until"]):
                return False
        elif values.get("active_from") and now < values["active_from"]:
            return False
        elif values.get("active_until") and now > values["active_until"]:
            return False

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


class PromoUpdate(PromoBase):
    pass


class PromoForUser(PromoBase):
    promo_id: UUID4
    company_id: UUID4
    company_name: str = Field(max_length=50, min_length=5)
    active: bool = Field(default=True)
    like_count: int = Field(default=0)
    is_activated_by_user: bool
    is_liked_by_user: bool
    comment_count: int = Field(default=0)

    @field_validator('active')
    def validate_active(cls, active, values):
        if not active:
            return False

        now = datetime.now().date()

        if values.get("active_from") and values.get("active_until"):
            if not (values["active_from"] <= now <= values["active_until"]):
                return False
        elif values.get("active_from") and now < values["active_from"]:
            return False
        elif values.get("active_until") and now > values["active_until"]:
            return False


class PromoStat(BaseModel):
    activate_count: int
    countries: list[dict[str, int]]
