from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


'''Enums'''


class RecurringIntervalTypes(str, Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class BusinessTypes(str, Enum):
    COMPANY = 'company'
    INDIVIDUAL = 'individual'
    # NON_PROFIT = 'non_profit'
    # GOVERNMENT_ENTITY = 'government_entity'


class CompanyStructureTypes(str, Enum):
    MULTI_MEMBER_LLC = "multi_member_llc"
    PRIVATE_CORPORATION = "private_corporation"
    PRIVATE_PARTNERSHIP = "private_partnership"
    PUBLIC_CORPORATION = "public_corporation"
    PUBLIC_PARTNERSHIP = "public_partnership"
    SINGLE_MEMBER_LLC = "single_member_llc"
    SOLE_PROPRIETORSHIP = "sole_proprietorship"
    UNINCORPORATED_ASSOCIATION = "unincorporated_association"
    INCORPORATED_NON_PROFIT = "incorporated_non_profit"
    UNINCORPORATED_NON_PROFIT = "unincorporated_non_profit"
    GOVERNMENT_INSTRUMENTALITY = "government_instrumentality"
    GOVERNMENTAL_UNIT = "governmental_unit"
    TAX_EXEMPT_GOVERNMENT_INSTRUMENTALITY = "tax_exempt_government_instrumentality"


class InvoiceCollectionTypes(str, Enum):
    CHARGE_AUTOMATICALLY = 'charge_automatically'
    SEND_INVOICE = 'send_invoice'


class GenderTypes(str, Enum):
    MALE = 'male'
    FEMALE = 'female'


'''Models'''


class AddressObject(BaseModel):
    city: str
    country: str  # Do 2 char validation
    line1: str
    line2: str
    postal_code: str
    state: str


class DOBObject(BaseModel):
    # Apply Validators
    day: int
    month: int
    year: int


class OwnershipDeclaration(BaseModel):
    date: int  # Unix Epoch
    ip: str  # Request Object
    user_agent: str  # Request Object


class DocumentObject(BaseModel):
    back: str
    front: str


class VerificationObject(BaseModel):
    document: DocumentObject
    additional_document: Optional[DocumentObject] = None


class PaymentRequestedObject(BaseModel):
    requested: Optional[bool] = None


class RelationshipObject(BaseModel):
    director: Optional[bool] = None
    executive: Optional[bool] = None
    owner: Optional[bool] = None
    percent_ownership: Optional[float] = None
    title: Optional[str] = None


class IndividualObject(BaseModel):
    address: Optional[AddressObject] = None
    dob: Optional[DOBObject] = None
    email: EmailStr
    first_name: str
    last_name: str
    maiden_name: Optional[str] = None
    gender: Optional[str] = None  # Validator Required
    id_number: Optional[str] = None
    id_number_secondary: Optional[str] = None
    metadata: Optional[dict] = None
    phone: str
    political_exposure: Optional[str] = None # Grab this from the user when onboarding
    registered_address: Optional[str] = None
    relationship: Optional[RelationshipObject] = None
    verification: Optional[VerificationObject] = None
    tos_shown_and_accepted: Optional[bool] = None


class CompanyObject(BaseModel):
    address: Optional[AddressObject] = None
    directors_provided: Optional[bool] = None
    executives_provided: Optional[bool] = None
    name: Optional[str] = None  # Company Legal Name
    owners_provided: Optional[bool] = None
    ownership_declaration: Optional[OwnershipDeclaration] = None
    phone: str
    registration_number: Optional[str] = None
    structure: Optional[str] = None
    tax_id: Optional[str] = None
    vat_id: Optional[str] = None
    verification: Optional[VerificationObject] = None


class CapabilitiesObject(BaseModel):
    acss_debit_payments: Optional[PaymentRequestedObject] = None
    affirm_payments: Optional[PaymentRequestedObject] = None
    afterpay_clearpay_payments: Optional[PaymentRequestedObject] = None
    amazon_pay_payments: Optional[PaymentRequestedObject] = None
    au_becs_debit_payments: Optional[PaymentRequestedObject] = None
    bacs_debit_payments: Optional[PaymentRequestedObject] = None
    bancontact_payments: Optional[PaymentRequestedObject] = None
    bank_transfer_payments: Optional[PaymentRequestedObject] = None
    blik_payments: Optional[PaymentRequestedObject] = None
    boleto_payments: Optional[PaymentRequestedObject] = None
    card_issuing: Optional[PaymentRequestedObject] = None
    card_payments: Optional[PaymentRequestedObject] = None
    cartes_bancaires_payments: Optional[PaymentRequestedObject] = None
    cashapp_payments: Optional[PaymentRequestedObject] = None
    eps_payments: Optional[PaymentRequestedObject] = None
    fpx_payments: Optional[PaymentRequestedObject] = None
    gb_bank_transfer_payments: Optional[PaymentRequestedObject] = None
    giropay_payments: Optional[PaymentRequestedObject] = None
    grabpay_payments: Optional[PaymentRequestedObject] = None
    ideal_payments: Optional[PaymentRequestedObject] = None
    india_international_payments: Optional[PaymentRequestedObject] = None
    jcb_payments: Optional[PaymentRequestedObject] = None
    jp_bank_transfer_payments: Optional[PaymentRequestedObject] = None
    klarna_payments: Optional[PaymentRequestedObject] = None
    konbini_payments: Optional[PaymentRequestedObject] = None
    legacy_payments: Optional[PaymentRequestedObject] = None
    link_payments: Optional[PaymentRequestedObject] = None
    mobilepay_payments: Optional[PaymentRequestedObject] = None
    multibanco_payments: Optional[PaymentRequestedObject] = None
    mx_bank_transfer_payments: Optional[PaymentRequestedObject] = None
    oxxo_payments: Optional[PaymentRequestedObject] = None
    p24_payments: Optional[PaymentRequestedObject] = None
    paynow_payments: Optional[PaymentRequestedObject] = None
    promptpay_payments: Optional[PaymentRequestedObject] = None
    revolut_pay_payments: Optional[PaymentRequestedObject] = None
    sepa_bank_transfer_payments: Optional[PaymentRequestedObject] = None
    sepa_debit_payments: Optional[PaymentRequestedObject] = None
    sofort_payments: Optional[PaymentRequestedObject] = None
    swish_payments: Optional[PaymentRequestedObject] = None
    tax_reporting_us_1099_k: Optional[PaymentRequestedObject] = None
    tax_reporting_us_1099_misc: Optional[PaymentRequestedObject] = None
    transfers: Optional[PaymentRequestedObject] = None
    twint_payments: Optional[PaymentRequestedObject] = None
    us_bank_account_ach_payments: Optional[PaymentRequestedObject] = None
    us_bank_transfer_payments: Optional[PaymentRequestedObject] = None
    zip_payments: Optional[PaymentRequestedObject] = None


class FeePayerObject(BaseModel):
    payer: Optional[str] = 'application'


class LossesPayerObject(BaseModel):
    payments: Optional[str] = 'application'


class StripeDashboardObject(BaseModel):
    type: Optional[str] = 'none'


class ControllerObject(BaseModel):
    fees: Optional[FeePayerObject] = FeePayerObject
    losses: Optional[LossesPayerObject] = LossesPayerObject
    requirement_collection: Optional[str] = 'application'
    stripe_dashboard: Optional[StripeDashboardObject] = StripeDashboardObject


class CreateAccountObject(BaseModel):
    business_type: str  # Do business type validation
    capabilities: Optional[CapabilitiesObject] = None
    company: Optional[CompanyObject] = None
    controller: Optional[ControllerObject] = ControllerObject
    country: Optional[str] = None  # Validation Required
    email: Optional[EmailStr] = None  # Grab manually from DB
    individual: IndividualObject
    metadata: Optional[dict] = None
    tos_show_and_accepted: bool  # Generate and put at final stage of onboarding
    type: Optional[str] = 'custom'


    '''
        Let the user decide which capability they want
        when the time comes:

        Notes:
            - Could show them a few on signup
    '''


class TokenAccountObject(BaseModel):
    business_type: str  # Do business type validation
    company: Optional[CompanyObject] = None
    individual: IndividualObject


class TokenCreateObject(BaseModel):
    account: TokenAccountObject


class LoginObject(BaseModel):
    email: str
    password: str


class SignUpObject(LoginObject):
    first_name: str
    last_name: str
    phone: str
    business_type: str  # Validation


class StripeSignUpObject(SignUpObject):
    tos_shown_and_accepted: bool


class AccountToken(BaseModel):
    account_token: str


class RecurringObject(BaseModel):
    interval: str  # Must be a valid RecurringIntervalType
    interval_count: int = Field(ge=1)


class CustomerObject(BaseModel):
    name: str
    email: str
    description: Optional[str] = None


class ProductObject(BaseModel):
    name: str
    active: Optional[bool] = True
    recurring: Optional[RecurringObject] = None


class InvoiceIssuerObject(BaseModel):
    type: Optional[str] = 'account'
    account: Optional[str] = None


# class InvoiceObject(BaseModel):
#     # auto_advance: bool = False
#     applicant_fee_amount: Optional[int] = None
#     customer_id: Optional[str] = None
#     new_customer: Optional[CustomerObject] = None # Create a customer if None
#     currency: Optional[str] = Field(min_length=3, max_length=3)
#     issuer: Optional[InvoiceIssuerObject] = InvoiceIssuerObject
#     product: Optional[str] = None
#     new_product: Optional[ProductObject] = None  # Must send a product through so we can create a product for them
#     unit_amount: Optional[int] = None
#     due_date: Optional[str] = None


class InvoiceObject(BaseModel):
    product_id: Optional[str] = None
    new_product: Optional[ProductObject] = None
    customer_id: Optional[str] = None
    new_customer: Optional[CustomerObject] = None
    issuer: Optional[InvoiceIssuerObject] = InvoiceIssuerObject
    unit_amount: int = Field(ge=200)
    currency: str = Field(min_length=3, max_length=3)
    due_date: str
    applicant_fee_amount: Optional[int] = 50
