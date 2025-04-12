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
import LoadingPage from "@client/components/UI/LoadingPage";
import { useMemo } from 'react';
  
  const getRandomInRange = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };

 

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
  const [isLoading, setIsLoading] = useState(true);
  const [ESG_report, setESG_report] = useState({});
  const randomStatValues = useMemo(() => ({
    positiveImpact: getRandomInRange(40, 90),            
    negativeRatio: getRandomInRange(5, 20),               
    transparency: getRandomInRange(0.5, 1),        
    rating: getRandomInRange(1, 5),
    mockESGScore : getRandomInRange(35, 65)                       
  }), []);

  const mockDetailsData = useMemo(() => {
    const generateSubDetails = (count) => {
      const categories = [
        "Emissions", "Resource Use", "Innovation",
        "Human Rights", "Product Responsibility", "Workforce", "Community",
        "Management", "Shareholders"
      ];
      const selected = categories.sort(() => 0.5 - Math.random()).slice(0, count);
      return selected.map((subCategory) => ({
        subCategory,
        score: getRandomInRange(30, 100),
      }));
    };
  
    return [
      {
        name: "Environment",
        value: getRandomInRange(60, 90),
        details: generateSubDetails(getRandomInRange(2, 4)),
      },
      {
        name: "Social",
        value: getRandomInRange(60, 90),
        details: generateSubDetails(getRandomInRange(3, 5)),
      },
      {
        name: "Governance",
        value: getRandomInRange(60, 90),
        details: generateSubDetails(getRandomInRange(2, 3)),
      },
    ];
  }, []);
  

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
 
  const fetchESGanswer = async () => {
    try {
        const res = await stock.post("/chatbot/evaluate/", {'message': `Xin chào, bạn hãy đánh giá ESG score của mã ${stockSymbol}` });
        setESG_report(res.data)

    } catch (error) {
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
        
    }
    
  };
  fetchESGanswer();
  
  const handleResize = () => {
    if (boxRef.current) {
        setChartWidth(boxRef.current.offsetWidth);
    }
  };

  const timer = setTimeout(() => {
    setIsLoading(false);
  }, 15000); 

  handleResize();

  window.addEventListener('resize', handleResize);

  return () => {
    clearTimeout(timer);
    window.removeEventListener('resize', handleResize);
  };
  
}, [stockData,stockSymbol, name]);

if (isLoading) {
  return (
    <LoadingPage/>
  );
}

  return (
    
    <div
      className={`min-h-screen overflow-y-auto grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-9 md:grid-rows-8 xl:grid-rows-7 auto-rows-fr gap-6 p-10 font-quicksand ${
        darkMode ? "bg-gray-900 text-gray-300" : "bg-neutral-100"
      }`}
    >
      <div className="col-span-3 row-span-1 grid grid-cols-4 gap-4 p-0">
        <Box backgroundColor="#ffff" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={`${randomStatValues.positiveImpact}%`}
            subtitle="Positive Impact"
            progress={randomStatValues.positiveImpact / 1000}
            increase={`+${randomStatValues.negativeRatio}%`}
            icon={<MonetizationOnIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#ffff" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={`${randomStatValues.negativeRatio}%`}
            subtitle="Negative Ratio"
            progress={randomStatValues.negativeRatio / 100}
            increase={`-${getRandomInRange(1, 10)}%`}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#ffff" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={randomStatValues.transparency.toLocaleString("de-DE")}
            subtitle="Transparent Data"
            progress={randomStatValues.transparency / 200_000}
            increase={`+${getRandomInRange(10, 30)}%`}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
        <Box backgroundColor="#ffff" display="flex" alignItems="center" justifyContent="center">
          <StatBox
            title={`${randomStatValues.rating}`}
            subtitle="Rating"
            progress={randomStatValues.rating / 5}
            increase={`+${Math.round(randomStatValues.rating / 5 * 100)}%`}
            icon={<PointOfSaleIcon sx={{ color: "#4951a3", fontSize: "26px" }} />}
          />
        </Box>
      </div>
                    
      <div className="col-span-2 row-span-4 grid grid-cols-10 gap-4 bg-transparent">

        <div className="bg-white rounded-xl shadow col-span-10 row-span-1 h-[300px] overflow-hidden">
        <ResponsiveContainer width="100%" height="100%">
          <ESGBarChart
            esgScore={randomStatValues.mockESGScore}
            data={mockDetailsData}
          />
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-xl shadow col-span-3 row-span-1">
          <ESGBarChart
            esgScore={randomStatValues.mockESGScore}
            data={mockDetailsData}
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
          change={35 / 12}
          changePercent={"5%"}
          currency={'VND'}
        />
      </div>

      {/* Details */}
      <div className="row-span-2 xl:row-span-3">
        <Details details={mockDetailsData} />
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
