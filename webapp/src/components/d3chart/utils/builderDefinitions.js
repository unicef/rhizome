import _ from 'lodash'

export default {
  charts: [
    { name: 'RawData', groupBy: true, locationLevel: true },
    { name: 'TableChart', groupBy: false, locationLevel: true, timeRadios: ['1month'] },
    // { name: 'ChoroplethMap', groupBy: false, locationLevel: false, timeRadios: ['1month'] },
    { name: 'MapChart', groupBy: false, locationLevel: false, timeRadios: ['1month'] },
    { name: 'BubbleMap', groupBy: false, locationLevel: false, timeRadios: ['1month'] },
    { name: 'LineChart', groupBy: true, locationLevel: true, timeRadios: ['all', '1year', '3month'] },
    { name: 'ColumnChart', groupBy: true, locationLevel: true, timeRadios: ['1year', '3month', '1month'] },
    { name: 'BarChart', groupBy: true, locationLevel: true, timeRadios: ['1month'] }
    // { name: 'ScatterChart', groupBy: false, locationLevel: true, timeRadios: ['1month'] },
    // { name: 'PieChart', groupBy: false, locationLevel: true, timeRadios: ['1month'] }
  ],
  single_campaign_charts: ['TableChart', 'MapChart', 'BubbleMap'],
  grouped_charts: ['LineChart', 'ColumnChart', 'RawData'],
  multi_location_charts: ['TableChart', 'MapChart', 'BubbleMap', 'ColumnChart'],
  need_missing_data_charts: ['TableChart', 'RawData'],
  groups: [
    { value: 'indicator', title: 'Indicators' },
    { value: 'location', title: 'Locations' }
  ],
  times: [
    {
      value: 'all',
      title: 'All Time',
      getLower: start => null,
      json: null
    },
    {
      value: '1year',
      title: 'Past Year',
      getLower: start => start.clone().startOf('month').subtract(1, 'year'),
      json: { years: 1 }
    },
    {
      value: '3month',
      title: 'Past 3 Months',
      getLower: start => start.clone().startOf('month').subtract(3, 'month'),
      json: { months: 2 }
    },
    {
      value: '1month',
      title: 'Current Campaign',
      getLower: start => start.clone().startOf('month'),
      json: { months: 0 }
    }
  ],
  formats: [
    { value: ',.0f', title: 'Integer' },
    { value: ',.4f', title: 'Real Number' },
    { value: '%', title: 'Percentage' }
  ],
  locationLevels: [
    {
      value: 'selected',
      title: 'Selected location only',
      getAggregated: (locationSelected, locationIndex) => locationSelected
    },
    {
      value: 'type',
      title: 'Locations with the same level',
      getAggregated: (locationSelected, locationIndex) => {
        return _.filter(locationIndex,
          (locationSelected.parent_location_id && locationSelected.parent_location_id !== 'None')
            ? { location_type_id: locationSelected.location_type_id, office_id: locationSelected.office_id }
            : { location_type_id: locationSelected.location_type_id }
        )
      }
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
