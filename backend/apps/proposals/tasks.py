from django.utils import timezone
from backend.celery import app
from .utils import loan_proposal_analyzer
from .models import LoanProposal


@app.task
def proposal_analizer_task(proposal_id):
    """
    Analyze and update proposal status
    """
    try:
        proposal = LoanProposal.objects.get(id=proposal_id)
    except LoanProposal.DoesNotExist:
        # Exit if proposal does not exist
        return

    status = loan_proposal_analyzer(proposal_id)
    proposal.status = status
    proposal.analyzed_at = timezone.now()
    proposal.save()
