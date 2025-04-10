// NewsList.js
import React from "react";
import mockNews from "@assets/data/mocknews";

const NewsList = () => {
  return (
    <div className="h-full max-h-[400px] overflow-y-auto p-4 space-y-4">
      {mockNews.map((news) => (
        <div key={news.id} className="flex gap-4 bg-white rounded-lg shadow p-3">
          <img
            src={news.image}
            alt={news.title}
            className="w-32 h-20 object-cover rounded-lg"
          />
          <div>
            <h3 className="font-semibold text-lg mb-1">{news.title}</h3>
            <p className="text-sm text-gray-600 line-clamp-3">{news.content}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NewsList;
