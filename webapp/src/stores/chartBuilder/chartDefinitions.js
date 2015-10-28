export default {
  charts: [
    {name: 'LineChart', groupBy: true, chooseAxis: false, timeRadios: ['allTime', 'pastYear', '3Months']},
    {name: 'PieChart', groupBy: false, chooseAxis: false, timeRadios :['current']},
    {name: 'ChoroplethMap' ,groupBy:false, chooseAxis:false, timeRadios: ['current']},
    {name: 'ColumnChart', groupBy: true, chooseAxis: false, timeRadios: ['pastYear', '3Months', 'current']},
    {name: 'ScatterChart', groupBy: false, chooseAxis: true, timeRadios: ['current']},
    {name: 'BarChart', groupBy: true, chooseAxis: false, timeRadios: ['current']}
  ],
  groups: [
    {value: 'indicator', title: 'Indicators'},
    {value: 'location', title: 'Locations'}
  ],
  times: [
    {
      value: 'all',
      title:'All Time',
      getLower: start => { return null },
      json: null
    },
    {
      value: '1year',
      title:'Past Year',
      getLower: start => { return start.clone().startOf('month').subtract(1,'year') },
      json: {years: 1}
    },
    {
      value: '3month',
      title: 'Past 3 Months',
      getLower: start => { return start.clone().startOf('month').subtract(3,'month') },
      json: {months: 2}
    },
    {
      value: '1month',
      title: 'Current Campaign',
      getLower: start => { return start.clone().startOf('month') },
      json: {months: 0}
    }
  ]
}
