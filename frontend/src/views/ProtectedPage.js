import { useEffect, useState } from "react";
import useAxios from "../utils/useAxios";
import ExamForm from './ExamForm';

function ProtectedPage() {
  const [res, setRes] = useState("");
  const api = useAxios();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/test/");
        setRes(response.data.response);
      } catch {
        setRes("Something went wrong");
      }
    };
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div>
      <h1>Protected Page</h1>
      <ExamForm />
    </div>
  );
}

export default ProtectedPage;
