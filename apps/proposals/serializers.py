from rest_framework import serializers
from apps.proposals import models


class ProposalFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProposalField
        fields = ['uuid', 'name', 'slug', 'type',
                  'required', 'is_active']


class ProposalFieldValueSerializer(serializers.ModelSerializer):
    field = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=models.ProposalField.objects.filter(is_active=True)
    )

    class Meta:
        model = models.ProposalFieldValue
        fields = ['field', 'value']


class LoanProposalSerializer(serializers.ModelSerializer):
    field_values = ProposalFieldValueSerializer(many=True)

    class Meta:
        model = models.LoanProposal
        fields = ['uuid', 'field_values', 'status', 'analized_at',
                  'created_at', 'updated_at']
