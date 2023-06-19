import "./App.css";
import DynamicForm from "./components/DynamicForm";

function App() {
  return (
    <>
      <div className="flex text-left w-1/2 m-auto justify-center my-5 ">
        <h1 className="text-3xl">Personal Loan Proposal</h1>
      </div>
      <div className="flex text-left w-1/2 m-auto justify-center  ">
        <DynamicForm />
      </div>
    </>
  );
}

export default App;
