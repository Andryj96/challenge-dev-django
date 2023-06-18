from rest_framework import serializers
from decimal import Decimal
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

    def validate(self, attrs):
        field_values_data = attrs.get('field_values', [])
        required_fields = models.ProposalField.objects.filter(
            required=True).values_list('slug', flat=True)

        # Validate ProposalFieldValue properties
        for slug in required_fields:
            # filter data
            verify_required_slug = list(filter(
                lambda field_data: field_data['field'].slug == slug, field_values_data  # noqa
            ))
            if len(verify_required_slug) == 0:
                raise serializers.ValidationError(
                    {'Error': [f'Field "{slug}" is required']})

            elif len(verify_required_slug) > 1:
                raise serializers.ValidationError(
                    {'Error': [f'Duplicate field slug: {slug}']})

            field_type = verify_required_slug[0]['field'].type
            field_value = verify_required_slug[0]['value']

            if field_type == models.FIELD_TYPES.NUMBER:
                try:
                    Decimal(field_value)
                except Exception:
                    raise serializers.ValidationError(
                        {'Error': [f'Field  "{slug}" must be Decimal number']})

            elif field_type == models.FIELD_TYPES.TEXT and \
                    not isinstance(field_value, str):  # noqa
                raise serializers.ValidationError(
                    {'Error': [f'Field  "{slug}" must be string']})

            elif field_type == models.FIELD_TYPES.CHECKBOX and \
                    field_value not in ['True', 'False']:  # noqa
                raise serializers.ValidationError(
                    {'Error': [f'Field  "{slug}" must be True or False']})

        return attrs

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
