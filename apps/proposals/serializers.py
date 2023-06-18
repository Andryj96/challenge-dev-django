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
        queryset=models.ProposalField.objects.filter(is_active=True),
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

        # get defined field
        defined_fields = models.ProposalField.objects.filter(
            is_active=True,
        )

        # get a list of actives and required
        active_fields = defined_fields.values_list('slug', flat=True)
        required_fields = defined_fields.filter(
            required=True).values_list('slug', flat=True)

        # Validate fields properties
        for slug in active_fields:

            # filter data
            verify_slug = list(filter(
                lambda field_data: field_data['field'].slug == slug, field_values_data  # noqa
            ))

            if len(verify_slug) > 1:
                raise serializers.ValidationError(
                    {'Error': [f'Duplicate field slug: {slug}']})

            elif len(verify_slug) == 0 and slug in required_fields:
                raise serializers.ValidationError(
                    {'Error': [f'Field "{slug}" is required']})

            elif len(verify_slug):
                field_type = verify_slug[0]['field'].type
                field_value = verify_slug[0]['value']

                if not field_value and slug in required_fields:
                    raise serializers.ValidationError(
                        {'Error': [f'Field "{slug}" may not be blank.']})

                if field_type == models.FIELD_TYPES.NUMBER:
                    try:
                        Decimal(field_value)
                    except Exception:
                        raise serializers.ValidationError(
                            {'Error': [f'Field  "{slug}" must be Decimal number, ex: "50.00"']})  # noqa

                elif field_type == models.FIELD_TYPES.TEXT and \
                        not isinstance(field_value, str):  # noqa
                    raise serializers.ValidationError(
                        {'Error': [f'Field  "{slug}" must be string']})

                elif field_type == models.FIELD_TYPES.CHECKBOX and \
                        field_value not in ['True', 'False']:  # noqa
                    raise serializers.ValidationError(
                        {'Error': [f'Field  "{slug}" must be True or False']})

        return attrs

    def to_internal_value(self, data):
        """
        Redefine method to handlre error message as
        {
            "field_values": [
                {
                    "field": ["message"]
                }
            ]
        }
        """
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exc:
            error_dict = exc.detail

            error_dict['field_values'] = [
                error for error in error_dict['field_values'] if error]

            raise serializers.ValidationError(error_dict)

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
