import React, { useState, useEffect } from "react";
import { createProposal, getProposalFields } from "../api/proposals.api";
import { ProposalField, CreateProposal } from "../api/proposals.interface";
import { toast } from "react-toastify";
import { FaSpinner } from "react-icons/fa";
// eslint-disable-next-line
import { AxiosError } from "axios";

const DynamicForm = () => {
  const [proposalFields, setProposalFields] = useState<ProposalField[]>([]);
  const [formValues, setFormValues] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Get proposal fields from api
    async function getProposalFieldsFromApi() {
      const initialFormValues: Record<string, string> = {};

      try {
        const response = await getProposalFields();
        setProposalFields(response.data);

        response.data.forEach((field) => {
          if (field.type === "checkbox") {
            initialFormValues[field.slug] = "False";
          } else if (field.type === "number") {
            initialFormValues[field.slug] = "0";
          } else {
            initialFormValues[field.slug] = "";
          }
        });
        setFormValues(initialFormValues);

        // eslint-disable-next-line
      } catch (error: AxiosError | any) {
        toast.error(
          <div>
            <h3>Error Ocurred!</h3>
            <p>
              {error.response?.data
                ? (Object.values(error.response.data)[0] as string)
                : error.message}
            </p>
          </div>,
          {
            position: "top-right",
            autoClose: 5000,
            hideProgressBar: true,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
          }
        );
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

    setIsLoading(true);

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
      await createProposal(data);

      toast.success("Proposal Created!", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: true,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });

      // eslint-disable-next-line
    } catch (error: AxiosError | any) {
      toast.error(
        <div>
          <h3>Error Ocurred!</h3>
          <p>
            {error.response?.data
              ? (Object.values(error.response.data)[0] as string)
              : error.message}
          </p>
        </div>,
        {
          position: "top-right",
          autoClose: 5000,
          hideProgressBar: true,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        }
      );
    } finally {
      setTimeout(() => {
        setIsLoading(false);
      }, 800);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-10">
      <h3
        className="text-center py-10 text-xl"
        hidden={!!proposalFields.length}
      >
        There are no proposal fields available to fill out
      </h3>
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
                onChange={handleInputChange}
                value={formValues[field.slug]}
                required={field.required}
              />
            </>
          )}
        </div>
      ))}
      <button
        className="py-3 w-full px-16 text-white-500 font-semibold rounded-lg bg-blue-500 hover:shadow-blue-md transition-all outline-none"
        type="submit"
        disabled={isLoading || !proposalFields.length}
      >
        {isLoading ? (
          <FaSpinner className="my-1 mx-auto" color="white" />
        ) : (
          "Create Loan Proposal"
        )}
      </button>
    </form>
  );
};

export default DynamicForm;
