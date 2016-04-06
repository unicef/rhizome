// import { Component } from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'

import map_data from './afghan_map'

class MapChart extends HighChart {

  constructor (props) {
    super(props)
    console.log('props: ', props)

    const chart_data = this.props.datapoints.meta.chart_data

    console.log('high_chart_map_data: ', map_data)

    const db_map_data = {'features': this.props.features, 'type': 'FeatureCollection'}
    console.log('rh maps : ', db_map_data)

    this.data = {
      title: {
        text: 'Highmaps basic demo'
      },
      subtitle: {
        text: 'Maps'
      },
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
        joinBy: 'hc-key',
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
