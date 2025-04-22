import axios from "axios";

// Use 127.0.0.1 OR localhost — be consistent
const API_URL = "http://127.0.0.1:8000";

export async function getAnswer(question) {
  try {
    const response = await axios.post(`${API_URL}/get-answer`, {
      question: question,
    });
    return response.data.answer;
  } catch (error) {
    console.error("Error fetching answer:", error);
    if (error.response) {
      // Server responded with a status code
      console.error("Response error:", error.response.data);
    } else if (error.request) {
      // Request was made but no response
      console.error("No response received:", error.request);
    } else {
      // Something else
      console.error("Request setup error:", error.message);
    }
    throw error;
  }
}

// Optional: test CORS
export async function testCors() {
  try {
    const res = await axios.get(`${API_URL}/test-cors`);
    console.log("CORS test response:", res.data);
  } catch (err) {
    console.error("CORS test error:", err);
  }
}
