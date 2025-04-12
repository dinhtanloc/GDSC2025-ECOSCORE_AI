import React from 'react';
import { PieChart, Pie, Cell, Text,ResponsiveContainer } from 'recharts';
import "@client/styles/esg-chart.css";
import data01 from "@assets/data/mockData.js"
import data02 from "@assets/data/mockData.js"


const ESGScore = () => {
  return (
    <ResponsiveContainer width="100%" height="100%">
        <PieChart width={400} height={400}>
          <Pie
            data={data02}
            cx="50%"
            cy="50%"
            innerRadius={150}
            outerRadius={250}
            paddingAngle={1}
            dataKey="value"
            label
          >
            {data02.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  index < 3 ? '#34c759' : 
                  index < 6 ? '#ffcc00' : 
                  '#ff4d4d'             

                }
              />
            ))}
          </Pie>
          <Text x="100%" y="50%" textAnchor="middle" dominantBaseline="central" fontSize="48" fill="black">
          </Text>

          <Pie
            data={data01}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={120}
            paddingAngle={5}
            dataKey="value"
            // label
          >
            {data01.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  index === 0 ? '#34c759' : 
                  index === 1 ? '#ffcc00' : 
                  '#ff4d4d'             

                }
              />
            ))}
          </Pie>

          
        </PieChart>
        </ResponsiveContainer>
  );
};

export default ESGScore;