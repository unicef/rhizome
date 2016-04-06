// import { Component } from 'react'

import Highcharts from 'highcharts'
import HighChart from 'components/molecules/highcharts/HighChart'

import format from 'utilities/format'
import map_data from './afghan_map'

class MapChart extends HighChart {

  constructor (props) {
    super(props)
    console.log('props: ', props)

    const chart_data = this.props.datapoints.meta.chart_data

    console.log('chart_data: ', chart_data)

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
        mapData: map_data, // map parameters
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
