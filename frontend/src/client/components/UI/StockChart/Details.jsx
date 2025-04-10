import React, { useContext } from "react";
import Card from "./Card";
import ThemeContext from "@context/ThemeContext";

const Details = ({ details }) => {
  const { darkMode } = useContext(ThemeContext);

  // Dữ liệu giả định
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

  return (
    <Card>
      <ul
        className={`w-full h-full flex flex-col divide-y-1 ${
          darkMode ? "divide-gray-800" : null
        }`}
      >
        {detailsData.map((category, index) => (
          <li key={index} className="flex flex-col">
            {/* Tiêu đề chính */}
            <div className="flex items-center justify-between mb-2">
              <span
                className={`text-lg font-bold ${
                  category.name === "Environment"
                    ? "text-green-500"
                    : category.name === "Social"
                    ? "text-yellow-500"
                    : "text-red-500"
                }`}
              >
                {category.name}
              </span>
              <span className={`font-bold text-black`}>{category.value}</span>
            </div>

            {/* Chi tiết */}
            <ul className="flex flex-col divide-y-1">
              {category.details.map((detail, detailIndex) => (
                <li
                  key={detailIndex}
                  className="font-bold text-black flex items-center justify-between py-2"
                >
                  <span>{detail.subCategory}</span>
                  <span className="font-bold text-black">{detail.score}</span>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </Card>
  );
};

export default Details;