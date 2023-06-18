from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.proposals.models import ProposalField, FIELD_TYPES, LoanProposal


class ProposalModelTest(TestCase):
    def setUp(self):
        pass

    def test_create_proposal_field(self):
        # Create a ProposalField
        proposal_field = ProposalField.objects.create(
            name='Test Field',
            slug='test_field',
            required=True,
            type=FIELD_TYPES.TEXT,
            is_active=True
        )

        # check if the object was created correctly
        self.assertEqual(proposal_field.name, 'Test Field')
        self.assertEqual(proposal_field.slug, 'test_field')
        self.assertTrue(proposal_field.required)
        self.assertEqual(proposal_field.type, FIELD_TYPES.TEXT)
        self.assertTrue(proposal_field.is_active)

    def test_unique_slug_in_proposal_field(self):

        # Create a ProposalField
        ProposalField.objects.create(
            name="Proposal Field",
            slug="proposal_field",
            required=True,
            type=FIELD_TYPES.TEXT,
            is_active=True
        )

        # try to create a ProposalField with the same slug
        with self.assertRaises(Exception) as context:
            ProposalField.objects.create(
                name="Proposal Field Again",
                slug="proposal_field",  # Try to use the same slug
                required=True,
                type=FIELD_TYPES.TEXT,
                is_active=True
            )

        self.assertTrue('unique' in str(context.exception))


class ProposalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create ProposalFields
        ProposalField.objects.create(
            name='Name',
            slug='name',
            required=True,
            type=FIELD_TYPES.TEXT,
            is_active=True
        )
        ProposalField.objects.create(
            name='Address',
            slug='address',
            required=True,
            type=FIELD_TYPES.TEXT,
            is_active=False
        )
        ProposalField.objects.create(
            name='CPF',
            slug='cpf',
            required=True,
            type=FIELD_TYPES.NUMBER,
            is_active=True
        )
        ProposalField.objects.create(
            name='Is married',
            slug='is_married',
            required=False,
            type=FIELD_TYPES.CHECKBOX,
            is_active=True
        )
        ProposalField.objects.create(
            name='Loan Value',
            slug='loan_value',
            required=True,
            type=FIELD_TYPES.NUMBER,
            is_active=True
        )
        self.url = reverse('loanproposal-list')

    def test_create_proposal(self):
        """
        Create a loan proposal
        Should return 200 Ok
        """
        data = dict(
            field_values=[
                {
                    "field": "name",
                    "value": "Test"
                },
                {
                    "field": "cpf",
                    "value": "123"
                },
                {
                    "field": "is_married",
                    "value": "True"
                },
                {
                    "field": "loan_value",
                    "value": "100.00"
                }
            ]
        )
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoanProposal.objects.count(), 1)

    def test_try_create_proposal_without_required_field(self):
        """
        Try to create a loan proposal with missing fields
        Should return bad request 400

        """
        data = dict(
            field_values=[
                {
                    "field": "name",
                    "value": "Test"
                },
                {
                    "field": "is_married",
                    "value": "True"
                }

            ]
        )
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('is required', response.data['Error'][0])

    def test_try_create_proposal_with_inactive_field(self):
        """
        Try to create a loan proposal with inactive field (address)
        Should return bad request 400

        """
        data = dict(
            field_values=[
                {
                    "field": "name",
                    "value": "Test"
                },
                {
                    "field": "address",
                    "value": "Rua Test 2020"
                }
            ]
        )
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_try_create_proposal_with_invalid_blank_field(self):
        """
        Try to create a loan proposal with invalid field type
        Should return bad request 400

        """
        data = dict(
            field_values=[
                {
                    "field": "name",
                    "value": "Test"
                },
                {
                    "field": "cpf",
                    "value": ""
                },
                {
                    "field": "is_married",
                    "value": "True"
                },
                {
                    "field": "loan_value",
                    "value": "100.00"
                }
            ]
        )

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('may not be blank', response.data['Error'][0])

    def test_try_create_proposal_with_invalid_number_field(self):
        """
        Try to create a loan proposal with invalid field type
        Should return bad request 400

        """
        data = dict(
            field_values=[
                {
                    "field": "name",
                    "value": "Test"
                },
                {
                    "field": "cpf",
                    "value": "not is nummber"
                },
                {
                    "field": "is_married",
                    "value": "True"
                },
                {
                    "field": "loan_value",
                    "value": "100.00"
                }
            ]
        )

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('must be Decimal number', response.data['Error'][0])
