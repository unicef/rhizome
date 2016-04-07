import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'

class MapChart extends HighChart {
  constructor (props) {
    super(props)
    this.data = {
      mapNavigation: {
        enabled: true,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      },
      colorAxis: {
        min: 0
      }
    }
  }

  getSeries () {
    return [{
      data: this.props.datapoints.meta.chart_data,
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      joinBy: 'location_id',
      name: 'Random data',
      states: {
        hover: {
          color: '#BADA55'
        }
      },
      dataLabels: {
        enabled: true,
        format: '{point.name}'
      }
    }]
  }
}

export default MapChart
