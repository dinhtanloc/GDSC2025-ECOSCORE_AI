import React, { useEffect, useRef } from 'react';
import * as Plot from '@observablehq/plot';
import * as d3 from 'd3';
import '@client/styles/rada.css'
import phoneData from '@assets/data/radaChart.js'

const RadarChart = () => {
  const plotRef = useRef();

  useEffect(() => {
    const points = phoneData.flatMap(({ name, ...values }) =>
      Object.entries(values).map(([key, value]) => ({ name, key, value }))
    );

    const longitude = d3.scalePoint(new Set(Plot.valueof(points, "key")), [180, -180])
      .padding(0.5)
      .align(1);
    const chart = Plot.plot({
      width: 620,
      projection: {
        type: "azimuthal-equidistant",
        rotate: [0, -90],
        domain: d3.geoCircle().center([0, 90]).radius(0.625)()
      },
      color: { legend: true },
      marks: [
        Plot.geo([0.5, 0.4, 0.3, 0.2, 0.1], {
          geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
          stroke: "black",
          fill: "black",
          strokeOpacity: 0.3,
          fillOpacity: 0.03,
          strokeWidth: 0.5
        }),
        Plot.link(longitude.domain(), {
          x1: longitude,
          y1: 90 - 0.57,
          x2: 0,
          y2: 90,
          stroke: "white",
          strokeOpacity: 0.5,
          strokeWidth: 2.5
        }),
        Plot.text([0.3, 0.4, 0.5], {
          x: 180,
          y: (d) => 90 - d,
          dx: 2,
          textAnchor: "start",
          text: (d) => `${100 * d}%`,
          fill: "currentColor",
          stroke: "white",
          fontSize: 10
        }),
        Plot.text(longitude.domain(), {
          x: longitude,
          y: 90 - 0.57,
          text: Plot.identity,
          lineWidth: 5
        }),
        Plot.area(points, {
          x1: ({ key }) => longitude(key),
          y1: ({ value }) => 90 - value,
          x2: 0,
          y2: 90,
          fill: "name",
          stroke: "name",
          curve: "cardinal-closed"
        }),
        Plot.dot(points, {
          x: ({ key }) => longitude(key),
          y: ({ value }) => 90 - value,
          fill: "name",
          stroke: "white"
        }),
        Plot.text(
          points,
          Plot.pointer({
            x: ({ key }) => longitude(key),
            y: ({ value }) => 90 - value,
            text: (d) => `${(100 * d.value).toFixed(0)}%`,
            textAnchor: "start",
            dx: 4,
            fill: "currentColor",
            stroke: "white",
            maxRadius: 10
          })
        )
      ]
    });

    if (plotRef.current) {
      plotRef.current.innerHTML = "";
      plotRef.current.appendChild(chart);

      d3.select(plotRef.current)
        .select("svg")
        .append("style")
        .text(`
           
          g[aria-label=area] path {fill-opacity: 0.1; transition: fill-opacity .2s;}
          g[aria-label=area]:hover path:not(:hover) {fill-opacity: 0.05; transition: fill-opacity .2s;}
          g[aria-label=area] path:hover {fill-opacity: 0.3; transition: fill-opacity .2s;}
        `);
    }
  }, []);

  return <div ref={plotRef}></div>;
};

export default RadarChart;
