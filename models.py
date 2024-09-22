from typing import Optional
from enum import Enum

# FastAPI Modules
from fastapi import Request
from pydantic import BaseModel, EmailStr, field_validator, Field


# Enums
class BusinessTypes(Enum):
    COMPANY = 'company'
    GOVERNMENT_ENTITY = 'government_entity'
    INDIVIDUAL = 'individual'
    NON_PROFIT = 'non_profit'


# Universal Models
class Address(BaseModel):
    city: str
    country: str = Field(min_length=2, max_length=2)
    line1: str
    line2: str
    postal_code: str
    state: str


class OwnerShipDeclaration(BaseModel):
    """
    Optionals to be processed upon arrival in endpoint
    """
    date: int
    ip: Optional[str]
    user_agent: Optional[dict]


class AccessDebitPayments(BaseModel):
    requested: Optional[bool] = False

class AffirmPayments(BaseModel):
    requested: Optional[bool] = False

class AfterPayClearPayPayments(BaseModel):
    requested: Optional[bool] = False

class AmazonPayPayments(BaseModel):
    requested: Optional[bool] = False

class AuBecsDebitPayments(BaseModel):
    requested: Optional[bool] = False

class BacsDebitPayments(BaseModel):
    requested: Optional[bool] = False

class BancontactPayments(BaseModel):
    requested: Optional[bool] = False

class BankTransferPayments(BaseModel):
    requested: Optional[bool] = True

class BlikPayments(BaseModel):
    requested: Optional[bool] = False

class BoletoPayments(BaseModel):
    requested: Optional[bool] = False

class CardIssuing(BaseModel):
    requested: Optional[bool] = False

class CardPayments(BaseModel):
    requested: Optional[bool] = True

class CartesBancairesPayments(BaseModel):
    requested: Optional[bool] = False

class CashAppPayments(BaseModel):
    requested: Optional[bool] = False

class EpsPayments(BaseModel):
    requested: Optional[bool] = False

class FpxPayments(BaseModel):
    requested: Optional[bool] = False

class GbBankTransferPayments(BaseModel):
    requested: Optional[bool] = False

class GiropayPayments(BaseModel):
    requested: Optional[bool] = False

class GrabPayPayments(BaseModel):
    requested: Optional[bool] = False

class IdealPayments(BaseModel):
    requested: Optional[bool] = False

class IndiaInternationalPayments(BaseModel):
    requested: Optional[bool] = False

class JcbPayments(BaseModel):
    requested: Optional[bool] = False

class JpBankTransferPayments(BaseModel):
    requested: Optional[bool] = False

class KlarnaPayments(BaseModel):
    requested: Optional[bool] = False

class KonbiniPayments(BaseModel):
    requested: Optional[bool] = False

class LegacyPayments(BaseModel):
    requested: Optional[bool] = False

class LinkPayments(BaseModel):
    requested: Optional[bool] = False

class MobilePayPayments(BaseModel):
    requested: Optional[bool] = False

class MultibancoPayments(BaseModel):
    requested: Optional[bool] = False

class MxBankTransferPayments(BaseModel):
    requested: Optional[bool] = False

class OxxoPayments(BaseModel):
    requested: Optional[bool] = False

class P24Payments(BaseModel):
    requested: Optional[bool] = False

class PaynowPayments(BaseModel):
    requested: Optional[bool] = False

class PromptPayPayments(BaseModel):
    requested: Optional[bool] = False

class RevolutPayPayments(BaseModel):
    requested: Optional[bool] = False

class SepaBankTransferPayments(BaseModel):
    requested: Optional[bool] = False

class SepaDebitPayments(BaseModel):
    requested: Optional[bool] = False

class SofortPayments(BaseModel):
    requested: Optional[bool] = False

class SwishPayments(BaseModel):
    requested: Optional[bool] = False

class TaxReportingUS1099K(BaseModel):
    requested: Optional[bool] = False

class TaxReportingUS1099Misc(BaseModel):
    requested: Optional[bool] = False

class Transfers(BaseModel):
    requested: Optional[bool] = False

class TwintPayments(BaseModel):
    requested: Optional[bool] = False

class UsBankAccountAchPayments(BaseModel):
    requested: Optional[bool] = False

class UsBankTransferPayments(BaseModel):
    requested: Optional[bool] = False

class ZipPayments(BaseModel):
    requested: Optional[bool] = False


class Capabilities(BaseModel):
    afterpay_clearpay_payments: Optional[AfterPayClearPayPayments] = None
    amazon_pay_payments: Optional[AmazonPayPayments] = None
    au_becs_debit_payments: Optional[AuBecsDebitPayments] = None
    bacs_debit_payments: Optional[BacsDebitPayments] = None
    bancontact_payments: Optional[BancontactPayments] = None
    bank_transfer_payments: Optional[BankTransferPayments] = None
    blik_payments: Optional[BlikPayments] = None
    boleto_payments: Optional[BoletoPayments] = None
    card_issuing: Optional[CardIssuing] = None
    card_payments: Optional[CardPayments] = None
    cartes_bancaires_payments: Optional[CartesBancairesPayments] = None
    cashapp_payments: Optional[CashAppPayments] = None
    eps_payments: Optional[EpsPayments] = None
    fpx_payments: Optional[FpxPayments] = None
    gb_bank_transfer_payments: Optional[GbBankTransferPayments] = None
    giropay_payments: Optional[GiropayPayments] = None
    grabpay_payments: Optional[GrabPayPayments] = None
    ideal_payments: Optional[IdealPayments] = None
    india_international_payments: Optional[IndiaInternationalPayments] = None
    jcb_payments: Optional[JcbPayments] = None
    jp_bank_transfer_payments: Optional[JpBankTransferPayments] = None
    klarna_payments: Optional[KlarnaPayments] = None
    konbini_payments: Optional[KonbiniPayments] = None
    legacy_payments: Optional[LegacyPayments] = None
    link_payments: Optional[LinkPayments] = None
    mobilepay_payments: Optional[MobilePayPayments] = None
    multibanco_payments: Optional[MultibancoPayments] = None
    mx_bank_transfer_payments: Optional[MxBankTransferPayments] = None
    oxxo_payments: Optional[OxxoPayments] = None
    p24_payments: Optional[P24Payments] = None
    paynow_payments: Optional[PaynowPayments] = None
    promptpay_payments: Optional[PromptPayPayments] = None
    revolut_pay_payments: Optional[RevolutPayPayments] = None
    sepa_bank_transfer_payments: Optional[SepaBankTransferPayments] = None
    sepa_debit_payments: Optional[SepaDebitPayments] = None
    sofort_payments: Optional[SofortPayments] = None
    swish_payments: Optional[SwishPayments] = None
    tax_reporting_us_1099_k: Optional[TaxReportingUS1099K] = None
    tax_reporting_us_1099_misc: Optional[TaxReportingUS1099Misc] = None
    transfers: Optional[Transfers] = None
    twint_payments: Optional[TwintPayments] = None
    us_bank_account_ach_payments: Optional[UsBankAccountAchPayments] = None
    us_bank_transfer_payments: Optional[UsBankTransferPayments] = None
    zip_payments: Optional[ZipPayments] = None


class Company(BaseModel):
    address: Address # TODO: Continue here
    directors_provided: bool = False
    executives_provided: bool = False
    company_name: str
    owners_provided: bool = False
    ownership_declaration: OwnerShipDeclaration
    phone: str
    registration_number: str # Use some sort of API or tool to verify
    structure


class AccountObject(BaseModel):
    business_type: BusinessTypes
    capabilities: Capabilities
    company: Company


# Auth Models
class User(BaseModel):
    email: EmailStr
    password: Optional[str]

    @field_validator('password')
    @classmethod
    def check_password(cls, password: str):
        min_nums = 2
        min_length = 8
        min_special_characters = 2
        special_charset = [
            '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',',
            '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\',
            ']', '^', '_', '`', '{', '|', '}', '~', '£', '€', '¥', '©', '®'
        ]

        if len(password) <= min_length:
            raise ValueError("Password must have minimum 8 characters")
        if sum(1 for char in password if char.isdigit()) < min_nums:
            raise ValueError(f"Password must have minimum {min_nums} characters")
        if sum(1 for char in password if char in special_charset) < min_special_characters:
            raise ValueError(f"Password must have minimum {min_special_characters} special characters")
        return password
