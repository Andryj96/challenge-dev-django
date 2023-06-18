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
    """
    Loan Proposal serializer for creating and list proposals
    To up
    """
    field_values = ProposalFieldValueSerializer(many=True)

    class Meta:
        model = models.LoanProposal
        fields = ['uuid', 'field_values', 'status', 'analyzed_at',
                  'created_at', 'updated_at']
        read_only_fields = ['status', 'analyzed_at']

    def create(self, validated_data):
        field_values_data = validated_data.pop('field_values')
        proposal = models.LoanProposal.objects.create(**validated_data)

        for field_value_data in field_values_data:
            models.ProposalFieldValue.objects.create(
                proposal=proposal,
                **field_value_data
            )

        return proposal

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Update proposals not implemented')
