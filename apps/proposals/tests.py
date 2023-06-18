from django.test import TestCase
from apps.proposals.models import ProposalField


class ProposalModelTest(TestCase):
    def setUp(self):
        pass

    def test_create_proposal_field(self):
        # Create a ProposalField
        proposal_field = ProposalField.objects.create(
            name='Test Field',
            slug='test_field',
            required=True,
            type='text',
            is_active=True
        )

        # check if the object was created correctly
        self.assertEqual(proposal_field.name, 'Test Field')
        self.assertEqual(proposal_field.slug, 'test_field')
        self.assertTrue(proposal_field.required)
        self.assertEqual(proposal_field.type, 'text')
        self.assertTrue(proposal_field.is_active)

    def test_unique_slug_in_proposal_field(self):

        # Create a ProposalField
        ProposalField.objects.create(
            name="Proposal Field",
            slug="proposal_field",
            required=True,
            type="text",
            is_active=True
        )

        # try to create a ProposalField with the same slug
        with self.assertRaises(Exception) as context:
            ProposalField.objects.create(
                name="Proposal Field Again",
                slug="proposal_field",  # Try to use the same slug
                required=True,
                type="text",
                is_active=True
            )

        self.assertTrue('unique' in str(context.exception))
