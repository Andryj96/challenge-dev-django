from django.db import models
from apps.core.models import GenericModel


class FIELD_TYPES(models.TextChoices):
    TEXT = 'text', 'text'
    NUMBER = 'number', 'number'
    CHECKBOX = 'checkbox', 'checkbox'


class ProposalField(GenericModel):
    """
    Proposal fields model to sava fields used in a personal loan proposal
    """
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    required = models.BooleanField(default=True)
    type = models.CharField(
        max_length=8,
        choices=FIELD_TYPES.choices,
        default=FIELD_TYPES.TEXT
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Proposal Field'
        verbose_name_plural = 'Proposal Fields'

    def __str__(self) -> str:
        return self.name


class PROPOSAL_STATUS(models.TextChoices):
    APPROVED = 'APPROVED', 'APPROVED'
    DENIED = 'DENIED', 'DENIED'
    PENDING = 'PENDING', 'PENDING'


class LoanProposal(GenericModel):
    status = models.CharField(
        max_length=8,
        choices=PROPOSAL_STATUS.choices,
        default=PROPOSAL_STATUS.PENDING
    )
    analyzed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Proposal {self.pk} - {self.status}'

    class Meta:
        verbose_name = 'Loan Proposal'
        verbose_name_plural = 'Loan Proposals'


class ProposalFieldValue(GenericModel):
    """
    Model for save proposal fields with values introduces by the users
    """
    field = models.ForeignKey(
        ProposalField,
        on_delete=models.CASCADE,
        related_name='+',
    )
    value = models.CharField(
        max_length=300,
        blank=True
    )
    proposal = models.ForeignKey(
        LoanProposal,
        on_delete=models.CASCADE,
        related_name='field_values'
    )

    class Meta:
        verbose_name = 'Proposal Field Value'
        verbose_name_plural = 'Proposal Field Values'

    def __str__(self) -> str:
        return f'{self.field}: {self.value}'
