from django.urls import path, include
from rest_framework import routers
from apps.proposals import views

router = routers.DefaultRouter()

router.register(r'v1/proposals/fields', views.ProposalFields)
router.register(r'v1/proposals/create', views.LoanProposals)

urlpatterns = [
    path('', include(router.urls)),
]
