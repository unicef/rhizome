import _ from 'lodash'

export default {
  charts: [
    { name: 'LineChart', groupBy: true, locationLevel: true, chooseAxis: false, timeRadios: ['all', '1year', '3month'] },
    { name: 'PieChart', groupBy: false, locationLevel: true, chooseAxis: false, timeRadios: ['1month'] },
    { name: 'ChoroplethMap', groupBy: false, locationLevel: false, chooseAxis: false, timeRadios: ['1month'] },
    { name: 'ColumnChart', groupBy: true, locationLevel: true, chooseAxis: false, timeRadios: ['1year', '3month', '1month'] },
    { name: 'ScatterChart', groupBy: false, locationLevel: true, chooseAxis: true, timeRadios: ['1month'] },
    { name: 'BarChart', groupBy: true, locationLevel: true, chooseAxis: false, timeRadios: ['1month'] }
  ],
  groups: [
    { value: 'indicator', title: 'Indicators' },
    { value: 'location', title: 'Locations' }
  ],
  times: [
    {
      value: 'all',
      title: 'All Time',
      getLower: start => { return null },
      json: null
    },
    {
      value: '1year',
      title: 'Past Year',
      getLower: start => { return start.clone().startOf('month').subtract(1, 'year') },
      json: { years: 1 }
    },
    {
      value: '3month',
      title: 'Past 3 Months',
      getLower: start => { return start.clone().startOf('month').subtract(3, 'month') },
      json: { months: 2 }
    },
    {
      value: '1month',
      title: 'Current Campaign',
      getLower: start => { return start.clone().startOf('month') },
      json: { months: 0 }
    }
  ],
  formats: [
    {
      value: ',.0f',
      title: 'Integer'
    },
    {
      value: ',.4f',
      title: 'Real Number'
    },
    {
      value: '%',
      title: 'Percentage'
    }
  ],
  locationLevels: [
    {
      value: 'selected',
      title: 'Selected location only',
      getAggregated: (locationSelected, locationIndex) => { return locationSelected }
    },
    {
      value: 'sublocations',
      title: 'Sublocations 1 level below selected',
      getAggregated: (locationSelected, locationIndex) => {
        return _(locationSelected).map(location => {
          return _.filter(locationIndex, { parent_location_id: location.id })
        }).flatten().value()
      }
    }
  ]
}
