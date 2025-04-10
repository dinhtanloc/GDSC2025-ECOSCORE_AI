import React from "react";

const ESGBarChart = ({ esgScore, data }) => {
  return (
    <div className="p-6 h-full flex flex-col justify-between overflow-hidden">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">ESG Score</h2>
        <div className="text-5xl font-extrabold text-blue-600 mb-6 animate-pulse">{esgScore}</div>
      </div>

      {/* Bar section */}
      <div className="flex-1 space-y-6 overflow-y-auto pr-2">
        {data.map((item, index) => (
          <div key={index}>
            <div className="text-sm font-semibold text-gray-700 mb-1">{item.category}</div>

            {/* Bar Group */}
            <div className="space-y-1">
              {/* Company */}
              <div className="flex items-center gap-2">
                <div className="w-16 text-xs text-gray-600">Company</div>
                <div className="flex-1 bg-gray-200 h-3 rounded-full relative overflow-hidden">
                  <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{ width: `${item.company}%` }}
                  ></div>
                </div>
                <div className="w-10 text-xs text-right text-gray-600">{item.company}</div>
              </div>

              {/* Mean */}
              <div className="flex items-center gap-2">
                <div className="w-16 text-xs text-gray-600">Mean</div>
                <div className="flex-1 bg-gray-200 h-3 rounded-full relative overflow-hidden">
                  <div
                    className="bg-gray-500 h-3 rounded-full opacity-70"
                    style={{ width: `${item.industryMean}%` }}
                  ></div>
                </div>
                <div className="w-10 text-xs text-right text-gray-600">{item.industryMean}</div>
              </div>

              {/* Best */}
              <div className="flex items-center gap-2">
                <div className="w-16 text-xs text-gray-600">Best</div>
                <div className="flex-1 bg-gray-200 h-3 rounded-full relative overflow-hidden">
                  <div
                    className="bg-orange-400 h-3 rounded-full"
                    style={{ width: `${item.industryBest}%` }}
                  ></div>
                </div>
                <div className="w-10 text-xs text-right text-gray-600">{item.industryBest}</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ESGBarChart;
