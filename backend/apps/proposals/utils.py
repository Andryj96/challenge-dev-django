from .models import PROPOSAL_STATUS


def loan_proposal_analyzer(proposal_id: int) -> PROPOSAL_STATUS:
    """
    Analyze a given personal loan proposal

    Returns if a proposal was APPROVED or DENIED based in
    its id for test purposes

    Even id will be approved and odd id will be denied

    Args:
        proposal_id: Proposal object id

    Returns:
        PROPOSAL_STATUS
    """

    return PROPOSAL_STATUS.APPROVED if proposal_id % 2 == 0 else PROPOSAL_STATUS.DENIED  # noqa
