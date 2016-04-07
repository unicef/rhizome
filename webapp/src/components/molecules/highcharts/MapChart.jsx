// import { Component } from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'

class MapChart extends HighChart {

  constructor (props) {
    super(props)

    const chart_data = this.props.datapoints.meta.chart_data
    const db_map_data = {'features': this.props.features, 'type': 'FeatureCollection'}

    console.log('rh maps : ', db_map_data)
    console.log('chart_data : ', chart_data)

    this.data = {
      mapNavigation: {
        enabled: true,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      },
      colorAxis: {
        min: 0
      },
      series: [{
        data: chart_data, // pass transformed datapoints \\
        mapData: db_map_data, // map parameters
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

}

export default MapChart
