from enum import Enum
from typing import Optional

from pydantic import BaseModel


'''Universal Models'''
#class AddressObject(BaseModel):


'''Models'''
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
