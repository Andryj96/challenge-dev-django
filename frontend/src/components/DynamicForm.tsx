import React, { useState, useEffect } from "react";
import { createProposal, getProposalFields } from "../api/proposals.api";
import { ProposalField, CreateProposal } from "../api/proposals.interface";

const DynamicForm = () => {
  const [proposalFields, setProposalFields] = useState<ProposalField[]>([]);
  const [formValues, setFormValues] = useState<Record<string, string>>({});

  useEffect(() => {
    // Get proposal fields from api
    async function getProposalFieldsFromApi() {
      try {
        const response = await getProposalFields();
        setProposalFields(response.data);
      } catch (error) {
        console.log(error);
      }
    }
    getProposalFieldsFromApi();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;

    let checkedValue = "False";
    if (checked) checkedValue = "True";

    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: type === "checkbox" ? checkedValue : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const arrayValues = proposalFields.map((field) => {
      return {
        field: field.slug,
        value: formValues[field.slug],
      };
    });

    // Send values to api to create a proposal
    const data: CreateProposal = {
      field_values: arrayValues,
    };
    try {
      const response = await createProposal(data);
      console.log(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-10">
      {proposalFields.map((field, key) => (
        <div key={key} className="mb-4">
          {field.type === "checkbox" ? (
            <>
              <input
                className="mr-3 border border-blue-500 transition-all"
                type="checkbox"
                id={field.slug}
                name={field.slug}
                checked={formValues[field.slug] === "True"}
                onChange={handleInputChange}
              />
              <label className="font-bold mb-2" htmlFor={field.slug}>
                {field.name}
              </label>
            </>
          ) : (
            <>
              <label className="block font-bold mb-2" htmlFor={field.slug}>
                {field.name}
              </label>
              <input
                className="w-full px-3 py-2 border rounded-lg focus:outline-blue-700 border-blue-500 hover:border-blue-700 transition-all"
                type={field.type}
                id={field.slug}
                name={field.slug}
                value={formValues[field.slug] || ""}
                onChange={handleInputChange}
                required={field.required}
              />
            </>
          )}
        </div>
      ))}

      <button
        className="py-3 lg:py-4 px-12 lg:px-16 text-white-500 font-semibold rounded-lg bg-blue-500 hover:shadow-blue-md transition-all outline-none"
        type="submit"
      >
        Create Loan Proposal
      </button>
    </form>
  );
};

export default DynamicForm;
