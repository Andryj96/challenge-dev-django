type FIELD_TYPES = "text" | "number" | "checkbox";
type PROPOSAL_STATUS = "APPROVED" | "DENIED" | "PENDING";

export interface ProposalField {
  uuid: string;
  name: string;
  slug: string;
  type: FIELD_TYPES;
  required: boolean;
  is_active: boolean;
}

export interface FieldValue {
  field: string;
  value: string;
}

export interface CreateProposal {
  field_values: FieldValue[];
}

export interface Proposal extends CreateProposal {
  uuid: string;
  status: PROPOSAL_STATUS;
  analyzed_at: string;
  created_at: string;
  updated_at: string;
}
