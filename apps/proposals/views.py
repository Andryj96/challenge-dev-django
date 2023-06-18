from rest_framework import viewsets, generics
from apps.proposals import serializers, models


class ProposalFields(generics.ListAPIView, viewsets.GenericViewSet):
    """
    Get active Proposal fields Api
    """
    queryset = models.ProposalField.objects.filter(is_active=True)
    serializer_class = serializers.ProposalFieldSerializer
    pagination_class = None
