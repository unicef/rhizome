export default {
  charts: [
    {name: "LineChart", groupBy: true, chooseAxis: false, timeRadios: ["allTime","pastYear","3Months"]},
    {name: "PieChart", groupBy: false, chooseAxis: false, timeRadios :["current"]},
    {name: "ChoroplethMap" ,groupBy:false, chooseAxis:false, timeRadios: ["current"]},
    {name: "ColumnChart", groupBy: true, chooseAxis: false, timeRadios: ["pastYear","3Months","current"]},
    {name: "ScatterChart", groupBy: false, chooseAxis: true, timeRadios: ["current"]},
    {name: "BarChart", groupBy: true, chooseAxis: false, timeRadios: ["current"]}
  ],
  groups: [
    {value: "indicator", title: "Indicators"},
    {value: "location", title: "Locations"}
  ]

}
