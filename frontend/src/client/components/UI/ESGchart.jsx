// src/components/ESGScore.js
import React from 'react';
import { PieChart, Pie, Cell, Text,ResponsiveContainer } from 'recharts';
import "@client/styles/esg-chart.css";

// Dữ liệu cho lớp bên trong (3 lĩnh vực chính)
const data01 = [
  { name: 'Environment', value: 82 },
  { name: 'Social', value: 83 },
  { name: 'Governance', value: 80 },
];

// Dữ liệu cho lớp bên ngoài (chi tiết của từng lĩnh vực)
const data02 = [
  // Environment
  { name: 'Emissions', value: 72 },
  { name: 'Resource Use', value: 86 },
  { name: 'Innovation', value: 83 },

  // Social
  { name: 'Human Rights', value: 96 },
  { name: 'Product Responsibility', value: 77 },
  { name: 'Workforce', value: 73 },
  { name: 'Community', value: 92 },

  // Governance
  { name: 'Management', value: 95 },
  { name: 'Shareholders', value: 38 },
];

const ESGScore = () => {
  return (
    <ResponsiveContainer width="100%" height="100%">
        <PieChart width={400} height={400}>
          {/* Lớp ngoài cùng (chi tiết từng lĩnh vực) */}
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
            {/* Ánh xạ màu cho từng phần */}
            {data02.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={
                  index < 3 ? '#34c759' : // Environment
                  index < 6 ? '#ffcc00' : // Social
                  '#ff4d4d' // Governance
                }
              />
            ))}
          </Pie>
          <Text x="100%" y="50%" textAnchor="middle" dominantBaseline="central" fontSize="48" fill="black">
            {/* 82tỷtyhrt */}
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
                  index === 0 ? '#34c759' : // Environment
                  index === 1 ? '#ffcc00' : // Social
                  '#ff4d4d' // Governance
                }
              />
            ))}
          </Pie>

          {/* Trung tâm (hiển thị điểm số tổng thể) */}
          
        </PieChart>
        </ResponsiveContainer>
  );
};

export default ESGScore;