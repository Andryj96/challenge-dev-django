import { AxiosResponse } from "axios";
import { axiosApi } from "../axios";
import { ProposalField, CreateProposal, Proposal } from "./proposals.interface";

const ENDPOINT = "/v1/proposals/";

export const createProposal = (
  body: CreateProposal
): Promise<AxiosResponse<Proposal>> => {
  return axiosApi.post(ENDPOINT + "create/", body);
};

export const getProposalFields = (): Promise<
  AxiosResponse<ProposalField[]>
> => {
  return axiosApi.get(ENDPOINT + "fields/");
};
