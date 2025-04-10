// imports...
import React, { useContext, useEffect, useState, useRef } from "react";
import ThemeContext from "@context/ThemeContext";
import Overview from "@client/components/UI/StockChart/Overview";
import Details from "@client/components/UI/StockChart/Details";
import ESGScore from "@client/components/UI/ESGchart";
import Header from "@client/components/UI/StockChart/Header";
import StockContext from "@context/StockContext";
import ChatIcon from '@mui/icons-material/Chat';
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import useAxios from '@utils/useAxios';
import ESGBarChart from "@client/components/UI/ESGBarChart"; 
import { PieChart, Pie, Cell, Text,ResponsiveContainer } from 'recharts';
import NewsList from "@client/components/UI/NewsList";
import { Container, Row } from "reactstrap";
import StatBox from '@client/components/UI/StatBox';
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import CommentList from "@client/components/UI/CommentList";
import mockComments from "@assets/data/mockComment";

const detailsData = [
  {
    name: "Environment",
    value: 82,
    details: [
      { subCategory: "Emissions", score: 72 },
      { subCategory: "Resource Use", score: 86 },
      { subCategory: "Innovation", score: 83 },
    ],
  },
  {
    name: "Social",
    value: 83,
    details: [
      { subCategory: "Human Rights", score: 96 },
      { subCategory: "Product Responsibility", score: 77 },
      { subCategory: "Workforce", score: 73 },
      { subCategory: "Community", score: 92 },
    ],
  },
  {
    name: "Governance",
    value: 80,
    details: [
      { subCategory: "Management", score: 95 },
      { subCategory: "Shareholders", score: 38 },
    ],
  },
];

const ActionButton = ({ onClick, label }) => (
  <Button
    variant="contained"
    color="primary"
    onClick={onClick}
    sx={{
      padding: '16px 32px',
      fontSize: '14px',
      borderRadius: '8px',
      fontWeight: 'bold',
      backgroundColor: '#3f51b5',
      '&:hover': {
        backgroundColor: '#303f9f',
        transform: 'scale(1.05)',
      },
      boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
      transition: 'all 0.3s ease',
    }}
  >
    {label}
  </Button>
);

const ESGDashboard = () => {
  const boxRef = useRef(null);
  const { darkMode } = useContext(ThemeContext);
  const navigate = useNavigate();
  const stock = useAxios();
  const [stockData, setStockData]=useState([]);

  const [infoCompany, setInfo] = useState([]);
  const { stockSymbol } = useContext(StockContext);

  const [stockDetails, setStockDetails] = useState({});

  useEffect(() => {
    const updateStockDetails = async () => {
      try {
        const res = await stock.post("/stock/stocktracking/tracking_stockinformation/", {
          symbol: stockSymbol,
        });
        setStockDetails({
          name: res.data.overview.short_name,
          country: "Việt Nam",
          currency: "VND",
          exchange: res.data.overview.exchange,
          ipo: res.data.overview.established_year,
          marketCapitalization: `${Math.round(res.data.overview.issue_share[0])} triệu`,
          finnhubIndustry: res.data.overview.industry,
        });
      } catch (error) {
        setStockDetails({});
        console.log(error);
      }
    };

    updateStockDetails();
    const fetchCompanyInfo = async () => {
      try {
          const res = await stock.post("/stock/stocktracking/tracking_stockinformation/", {
              symbol: stockSymbol, 
            });
          setInfo(res.data)

      } catch (error) {
          console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
          
      }
      
    };


    fetchCompanyInfo();
  const handleResize = () => {
      if (boxRef.current) {
          setChartWidth(boxRef.current.offsetWidth);
      }
  };

  handleResize();

  window.addEventListener('resize', handleResize);

  return () => window.removeEventListener('resize', handleResize);
  
}, [stockData,stockSymbol, name]);

  return (
    
    <div
      className={`min-h-screen overflow-y-auto grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-9 md:grid-rows-8 xl:grid-rows-7 auto-rows-fr gap-6 p-10 font-quicksand ${
        darkMode ? "bg-gray-900 text-gray-300" : "bg-neutral-100"
      }`}
    >
      <div className="col-span-3 grid grid-cols-4 gap-4">
        <Box backgroundColor="#FFFFCC" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={infoCompany?.overview?.issue_share?.[0] ? `${Math.round(infoCompany.overview.issue_share[0])}B` : ""}
            subtitle="Market Capital"
            progress={Math.random()}
            increase={`+${Math.floor(Math.random() * 100)}%`}
            icon={<MonetizationOnIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#f0f3f7" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={infoCompany?.overview?.delta_in_month ?? ""}
            subtitle="Delta (month)"
            progress={Math.random()}
            increase={`+${Math.floor(Math.random() * 100)}%`}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#f0f3f7" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={infoCompany?.overview?.no_shareholders?.toLocaleString('de-DE') ?? ""}
            subtitle="Shareholders"
            progress={Math.random()}
            increase={`+${Math.floor(Math.random() * 100)}%`}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#f0f3f7" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={infoCompany?.overview?.stock_rating ?? "N/A"}
            subtitle="Rating"
            progress={infoCompany?.overview?.stock_rating ? infoCompany.overview.stock_rating / 5 : 0}
            increase={infoCompany?.overview?.stock_rating ? `+${Math.round(100 * infoCompany.overview.stock_rating / 5)}%` : "N/A"}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
      </div>
                    

      {/* ESG Section: Score (7) + Bar Chart (3) */}
      <div className="col-span-2 row-span-4 grid grid-cols-10 gap-4 bg-transparent">

        <div className="bg-white rounded-xl shadow col-span-10 row-span-1 h-[300px] overflow-hidden">
        <ResponsiveContainer width="100%" height="100%">
          <ESGBarChart
            esgScore={37}
            data={[
              {
                category: "Environmental",
                company: 61,
                industryMean: 33,
                industryBest: 95,
              },
              {
                category: "Social",
                company: 24,
                industryMean: 29,
                industryBest: 89,
              },
              {
                category: "Governance & Economic",
                company: 29,
                industryMean: 32,
                industryBest: 89,
              },
            ]}
          />
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl shadow col-span-3 row-span-1">
          <ESGBarChart
            esgScore={37}
            data={[
              {
                category: "Environmental",
                company: 61,
                industryMean: 33,
                industryBest: 95,
              },
              {
                category: "Social",
                company: 24,
                industryMean: 29,
                industryBest: 89,
              },
              {
                category: "Governance & Economic",
                company: 29,
                industryMean: 32,
                industryBest: 89,
              },
            ]}
          />
        </div>
        <div className="bg-white rounded-xl shadow col-span-7">
          <ESGScore />
        </div>

      </div>

      {/* Overview */}
      <div>
        <Overview
          symbol={stockSymbol}
          price={200}
          change={13 / 12}
          changePercent={"5%"}
          currency={'VND'}
        />
      </div>

      {/* Details */}
      <div className="row-span-2 xl:row-span-3">
        <Details details={detailsData} />
      </div>

      <div className="bg-white rounded-xl shadow col-span-2 row-span-2">
      <NewsList />
      </div>

      <div className="bg-white rounded-xl shadow col-span-1 row-span-2">
  
      <CommentList comments={mockComments}/>
      </div>

      <div className="col-span-1 md:col-span-2 xl:col-span-3 row-span-1" style={{ marginTop: "100px" }}>
        <Box display="grid" gridTemplateColumns="repeat(15, 1fr)" gridAutoRows="90px" gap="20px">
          <Box gridColumn="span 2" display="flex" justifyContent="center" alignItems="center" height="450">
            <ActionButton onClick={() => navigate('/stock-market')} label="Return" />
          </Box>
          <Box gridColumn="span 11" />
          <Box
            gridColumn="span 2"
            display="flex"
            alignItems="center"
            sx={{
              cursor: "pointer",
              color: "orange",
              fontWeight: "bold",
              '&:hover': {
                transform: "scale(1.1)",
                color: "#FF8C00",
              },
              transition: "all 0.3s ease",
            }}
            onClick={() => navigate('/chatbot')}
          >
            <ChatIcon sx={{ marginRight: "8px" }} />
            <Typography variant="h4">Go to Chatbot</Typography>
          </Box>
        </Box>
      </div>
    </div>
  );
};

export default ESGDashboard;
