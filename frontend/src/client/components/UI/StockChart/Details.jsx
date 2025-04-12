import React, { useContext } from "react";
import Card from "./Card";
import ThemeContext from "@context/ThemeContext";

const Details = ({ details }) => {
  const { darkMode } = useContext(ThemeContext);

  return (
    <Card>
      <ul
        className={`w-full h-full flex flex-col divide-y-1 ${
          darkMode ? "divide-gray-800" : null
        }`}
      >
        {details.map((category, index) => (
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