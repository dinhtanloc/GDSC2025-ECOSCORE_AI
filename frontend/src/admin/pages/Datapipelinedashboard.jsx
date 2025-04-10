import React from "react";
import useData from "@context/dataContext";
import { Box, Typography } from "@mui/material";
import DateStockePicker from "@admin/components/UI/DateStockePicker";
// import ModelPerformance from "@admin/components/UI/ModelPerformance";
import { DotLoader } from "react-spinners";
import '@admin/styles/predictions.css';
// import QuoteLIneChart from '@admin/components/UI/QuoteLIneChart';
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
import { useState, useEffect} from "react";

export default function Datapipelinedashboard() {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [tickers, setTickers] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);

  const handleRunETL = async () => {
    setLoading(true);
    setStatus(null);
    try {
      const response = await axios.post("http://localhost:8000/api/etl/", {
        tickers: tickers.split(",").map((s) => s.trim()),
      });
      setStatus({ success: true, message: response.data.message });
    } catch (error) {
      setStatus({ success: false, message: error.response?.data?.error || "Unknown error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-8">
      <img
        src="/media/ETL.png"
        alt="ETL Process Illustration"
        className="mt-8 w-full max-w-xl mx-auto rounded-xl shadow-lg"
      />
      <div className="max-w-3xl mx-auto bg-white/10 p-10 rounded-2xl shadow-xl backdrop-blur-md">
        <h1 className="text-4xl font-bold text-center mb-6 text-cyan-300">🚀 ETL Dashboard</h1>
        <p className="text-sm text-gray-400 text-center mb-4">Nhập danh sách mã cổ phiếu, cách nhau bởi dấu phẩy</p>
        <textarea
          value={tickers}
          onChange={(e) => setTickers(e.target.value)}
          placeholder="VD: VNM, FPT, HPG"
          className="w-full p-3 rounded-lg bg-black/30 text-white border border-gray-600 mb-6 resize-none"
          rows={4}
        />
        <button
          onClick={handleRunETL}
          disabled={loading}
          className={`w-full py-3 rounded-xl text-lg font-semibold bg-cyan-500 hover:bg-cyan-400 transition ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loading ? "⏳ Đang chạy ETL..." : "▶️ Bắt đầu ETL"}
        </button>
        {status && (
          <div
            className={`mt-6 p-4 rounded-lg ${
              status.success ? "bg-green-600/70" : "bg-red-600/70"
            } text-white`}
          >
            {status.message}
          </div>
        )}
      </div>
      


    </div>
    
  );

 
  
}
