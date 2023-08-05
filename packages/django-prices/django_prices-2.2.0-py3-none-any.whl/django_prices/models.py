from decimal import Decimal

from django.core import validators
from django.db.models import Field
from prices import Money, TaxedMoney

from . import forms
from functools import total_ordering


@total_ordering
class NonDatabaseFieldBase:
    """Base class for all fields that are not stored in the database."""

    empty_values = list(validators.EMPTY_VALUES)

    # Field flags
    auto_created = False
    blank = True
    concrete = False
    editable = False
    unique = False

    is_relation = False
    remote_field = None

    many_to_many = None
    many_to_one = None
    one_to_many = None
    one_to_one = None

    def __init__(self):
        self.column = None
        self.primary_key = False

        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def __eq__(self, other):
        if isinstance(other, (Field, NonDatabaseFieldBase)):
            return self.creation_counter == other.creation_counter
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (Field, NonDatabaseFieldBase)):
            return self.creation_counter < other.creation_counter
        return NotImplemented

    def __hash__(self):
        return hash(self.creation_counter)

    def contribute_to_class(self, cls, name, **kwargs):
        self.attname = self.name = name
        self.model = cls
        cls._meta.add_field(self, private=True)
        setattr(cls, name, self)

    def clean(self, value, model_instance):
        # Shortcircut clean() because Django calls it on all fields with
        # is_relation = False
        return value


class MoneyField(NonDatabaseFieldBase):

    description = (
        "A field that combines an amount of money and currency code into Money"
        "It allows to store prices with different currencies in one database."
    )

    def __init__(
        self,
        amount_field="price_amount",
        currency_field="price_currency",
        verbose_name=None,
        **kwargs
    ):
        super(MoneyField, self).__init__()
        self.amount_field = amount_field
        self.currency_field = currency_field
        self.verbose_name = verbose_name

    def __str__(self):
        return "MoneyField(amount_field=%s, currency_field=%s)" % (
            self.amount_field,
            self.currency_field,
        )

    def __get__(self, instance, cls=None):
        if instance is None:
            return self

        amount = getattr(instance, self.amount_field)
        currency = getattr(instance, self.currency_field)
        if amount is not None and currency is not None:
            return Money(amount, currency)
        return self.get_default()

    def __set__(self, instance, value):
        amount = None
        currency = None
        if value is not None:
            amount = value.amount
            currency = value.currency
        setattr(instance, self.amount_field, amount)
        setattr(instance, self.currency_field, currency)

    def formfield(self, **kwargs):
        available_currencies = []
        if hasattr(self, "model"):
            available_currencies = self.model._meta.get_field(
                self.currency_field
            ).choices
        return forms.MoneyField(available_currencies=available_currencies)

    def get_default(self):
        default_currency = None
        default_amount = Decimal(0)
        if hasattr(self, "model"):
            default_currency = self.model._meta.get_field(
                self.currency_field
            ).get_default()
            default_amount = self.model._meta.get_field(self.amount_field).get_default()

        if default_amount is None:
            return None
        return Money(default_amount, default_currency)


class TaxedMoneyField(NonDatabaseFieldBase):

    description = "A field that combines net and gross fields values into TaxedMoney."

    def __init__(
        self,
        net_amount_field="price_amount_net",
        gross_amount_field="price_amount_gross",
        currency="currency",
        verbose_name=None,
        **kwargs
    ):
        super(TaxedMoneyField, self).__init__()
        self.net_amount_field = net_amount_field
        self.gross_amount_field = gross_amount_field
        self.currency = currency
        self.verbose_name = verbose_name

    def __str__(self):
        return (
            "TaxedMoneyField(net_amount_field=%s, gross_amount_field=%s, currency=%s)"
            % (self.net_amount_field, self.gross_amount_field, self.currency)
        )

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        net_amount = getattr(instance, self.net_amount_field)
        gross_amount = getattr(instance, self.gross_amount_field)
        currency = getattr(instance, self.currency)
        if net_amount is None or gross_amount is None:
            return None
        return TaxedMoney(Money(net_amount, currency), Money(gross_amount, currency))

    def __set__(self, instance, value):
        net_amount = None
        gross_amount = None
        currency = None
        if value is not None:
            net_amount = value.net.amount
            gross_amount = value.gross.amount
            currency = value.currency
        setattr(instance, self.net_amount_field, net_amount)
        setattr(instance, self.gross_amount_field, gross_amount)
        setattr(instance, self.currency, currency)
