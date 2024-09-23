import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, Field, EmailStr


'''Enums'''
class BusinessTypes(str, Enum):
    COMPANY = 'company'
    INDIVIDUAL = 'individual'
    NON_PROFIT = 'non_profit'


class BusinessStructureTypes(str, Enum):
    MULTI_MEMBER_LLC = 'multi_member_llc'
    PRIVATE_CORPORATION = 'private_corporation'
    PRIVATE_PARTNERSHIP = 'private_partnership'
    PUBLIC_CORPORATION = 'public_corporation'
    PUBLIC_PARTNERSHIP = 'public_partnership'
    SINGLE_MEMBER_LLC = 'single_member_llc'
    SOLE_PROPRIETORSHIP = 'sole_proprietorship'
    UNINCORPORATED_ASSOCIATION = 'unincorporated_association'


class FeePayerTypes(str, Enum):
    ACCOUNT = 'account'
    APPLICATION = 'application'


class GenderTypes(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


class PoliticalExposureType(str, Enum):
    EXISTING = 'existing'
    NONE = 'none'


'''Universal Models'''
class AddressObject(BaseModel):
    city: str
    country: str = Field(min_length=2, max_length=2)
    line1: str
    line2: str
    postal_code: str
    state: str


class DOBObject(BaseModel):
    date: int
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)


class RelationShipObject(BaseModel):
    director: Optional[bool]
    executive: Optional[bool]
    owner: Optional[bool]
    percent_ownership: Optional[float]
    title: str

'''Specific Models'''
class PaymentCapability(BaseModel):
    requested: bool


class CapabilitiesObjects(BaseModel):
    card_payments: Optional[PaymentCapability] = None
    acss_debit_payments: Optional[PaymentCapability] = None
    affirm_payments: Optional[PaymentCapability] = None
    afterpay_clearpay_payments: Optional[PaymentCapability] = None
    amazon_pay_payments: Optional[PaymentCapability] = None
    au_becs_debit_payments: Optional[PaymentCapability] = None
    bacs_debit_payments: Optional[PaymentCapability] = None
    bancontact_payments: Optional[PaymentCapability] = None
    bank_transfer_payments: Optional[PaymentCapability] = None
    blik_payments: Optional[PaymentCapability] = None
    boleto_payments: Optional[PaymentCapability] = None
    card_issuing: Optional[PaymentCapability] = None
    cartes_bancaires_payments: Optional[PaymentCapability] = None
    cashapp_payments: Optional[PaymentCapability] = None
    eps_payments: Optional[PaymentCapability] = None
    fpx_payments: Optional[PaymentCapability] = None
    gb_bank_transfer_payments: Optional[PaymentCapability] = None
    giropay_payments: Optional[PaymentCapability] = None
    grabpay_payments: Optional[PaymentCapability] = None
    ideal_payments: Optional[PaymentCapability] = None
    india_international_payments: Optional[PaymentCapability] = None
    jcb_payments: Optional[PaymentCapability] = None
    jp_bank_transfer_payments: Optional[PaymentCapability] = None
    klarna_payments: Optional[PaymentCapability] = None
    konbini_payments: Optional[PaymentCapability] = None
    legacy_payments: Optional[PaymentCapability] = None
    link_payments: Optional[PaymentCapability] = None
    mobilepay_payments: Optional[PaymentCapability] = None
    multibanco_payments: Optional[PaymentCapability] = None
    mx_bank_transfer_payments: Optional[PaymentCapability] = None
    oxxo_payments: Optional[PaymentCapability] = None
    p24_payments: Optional[PaymentCapability] = None
    paynow_payments: Optional[PaymentCapability] = None
    promptpay_payments: Optional[PaymentCapability] = None
    revolut_pay_payments: Optional[PaymentCapability] = None
    sepa_bank_transfer_payments: Optional[PaymentCapability] = None
    sepa_debit_payments: Optional[PaymentCapability] = None
    sofort_payments: Optional[PaymentCapability] = None
    swish_payments: Optional[PaymentCapability] = None
    tax_reporting_us_1099_k: Optional[PaymentCapability] = None
    tax_reporting_us_1099_misc: Optional[PaymentCapability] = None
    transfers: Optional[PaymentCapability] = None
    twint_payments: Optional[PaymentCapability] = None
    us_bank_account_ach_payments: Optional[PaymentCapability] = None
    us_bank_transfer_payments: Optional[PaymentCapability] = None
    zip_payments: Optional[PaymentCapability] = None


class VerificationDocument(BaseModel):
    back: str  # File Path to back of document image
    front: str  # File Path to back of document image


class CompanyVerificationObject(BaseModel):
    document: VerificationDocument
    additional_documents: VerificationDocument


class FeesObject(BaseModel):
    payer: Optional[FeePayerTypes] = FeePayerTypes.APPLICATION.value

    @field_validator('payer')
    @classmethod
    def validate_payer(cls, v:str) -> str:
        if v in [item.value for item in FeePayerTypes]:
            return v
        raise ValueError(f'payer must be of {[item.value for item in FeePayerTypes]}')


class LossesObject(BaseModel):
    payments: Optional[FeePayerTypes] = FeePayerTypes.APPLICATION.value

    @field_validator('payments')
    @classmethod
    def validate_payer(cls, v: str) -> str:
        if v in [item.value for item in FeePayerTypes]:
            return v
        raise ValueError(f'payments must be of {[item.value for item in FeePayerTypes]}')


class StripeDashboardObject(BaseModel):
    type: Optional[str] = "none"


class OwnershipDeclarationObject(BaseModel):
    date: DOBObject
    ip: str
    user_agent: str


class ControllerObject(BaseModel):
    fees: Optional[FeesObject] = FeesObject
    losses: Optional[LossesObject] = LossesObject
    requirement_collection: Optional[FeePayerTypes] = FeePayerTypes.APPLICATION.value
    stripe_dashboard: Optional[StripeDashboardObject] = StripeDashboardObject

    @field_validator('requirement_collection')
    @classmethod
    def validate_payer(cls, v: str) -> str:
        if v in [item.value for item in FeePayerTypes]:
            return v
        raise ValueError(f'requirement_collection must be of {[item.value for item in FeePayerTypes]}')

class TOSAcceptanceObject(BaseModel):
    date: int
    ip: str
    service_agreement: str
    user_agent: str


'''Main Objects'''
class IndividualObject(BaseModel):
    address: Optional[AddressObject] = None
    dob: Optional[DOBObject] = None
    email: EmailStr
    first_name: str
    gender: Optional[str] = None
    last_name: str
    maiden_name: Optional[str] = None
    phone: str
    political_exposure: Optional[str] = PoliticalExposureType.NONE.value
    registered_address: Optional[AddressObject] = None
    relationship: Optional[RelationShipObject] = None
    verification: Optional[CompanyVerificationObject] = None

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v: str) -> str:
        if v in [item.name for item in GenderTypes]:
            return v
        raise ValueError(f"gender must be of 'male', 'female'")


class CompanyObject(BaseModel):
    address: AddressObject
    directors_provided: Optional[bool] = False
    executives: Optional[bool] = False
    export_license_id: str
    export_purpose_code: str
    name: str
    owners_provided: Optional[bool] = False
    ownership_declaration: OwnershipDeclarationObject
    phone: str
    registration_number: str
    structure: Optional[str] = BusinessStructureTypes
    tax_id: str
    tax_id_registrar: str
    vat_id: str
    verification: CompanyVerificationObject

    @field_validator('structure')
    @classmethod
    def validate_structure(cls, v: str) -> str:
        if v in [item.name for item in BusinessStructureTypes]:
            return v
        raise ValueError(f"structure must be of {[item.name for item in BusinessStructureTypes]}")


class AccountObject(BaseModel):
    business_type: str
    capabilities: Optional[CapabilitiesObjects] = None
    company: Optional[CompanyObject] = None
    controller: Optional[ControllerObject] = None
    country: str = Field(min_length=2, max_length=2)
    email: EmailStr
    individual: IndividualObject
    tos_acceptance: TOSAcceptanceObject
    type: Optional[str] = 'custom'

    @field_validator('business_type')
    @classmethod
    def validate_business_type(cls, v: str) -> str:
        if v in [item.value for item in BusinessTypes]:
            return v
        raise ValueError(f"business_type must be of {[item.value for item in BusinessTypes]}")


class TokenCreateObject(BaseModel):
    account: AccountObject


class LoginObject(BaseModel):
    email: str
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        min_chars = 8
        min_nums = 2
        min_special_chars = 2

        # num_count = len(re.findall(r'\d', v))
        # special_char_count = len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', v))

        if len(v) < min_chars:
            raise ValueError(f"Password must be at least {min_chars} characters long.")
        if len(re.findall(r'\d', v)) < min_nums:
            raise ValueError(f"Password must contain at least {min_nums} numbers.")
        if len(re.findall(r'[!@#$%^&*(),.?":{}|<>]', v)) < min_special_chars:
            raise ValueError(f"Password must contain at least {min_special_chars} special characters.")

        return v


class SignUpObject(BaseModel):
    first_name: str
    last_name: str
    business_type: str

    @field_validator('business_type')
    @classmethod
    def validate_business_type(cls, v: str) -> str:
        if v in [item.value for item in BusinessTypes]:
            return v
        raise ValueError(f"business_type must be of {[item.value for item in BusinessTypes]}")
