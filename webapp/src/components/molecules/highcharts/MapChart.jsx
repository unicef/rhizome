import _ from 'lodash'
import React, { Component, PropTypes } from 'react'

// import Highmaps from 'highcharts/highmaps'
// import Highmaps from 'react-highcharts/dist/highmaps'
// import Highmaps from 'highcharts'
// import ReactHighchart from 'react-highcharts/dist/highcharts'
// import ReactHighmap from 'react-highcharts/dist/highmaps'
// var HighchartsMore = require('highcharts-more');
// import Map from 'react-highcharts/dist/modules/map'
// We tell HighchartsMore to use the same Highcharts object as ReactHighcharts

import format from 'utilities/format'
import maps from './map_data'

class MapChart extends Component {

  constructor (props) {
    super(props)
    const first_indicator = props.selected_indicators[0]
    this.data = {
      chart: {
        // type: 'map',
        spacingBottom: 20
      },
      title: {
        text: 'Europe time zones'
      },

      legend: {
        enabled: true
      },

      plotOptions: {
        map: {
          allAreas: false,
          joinBy: ['iso-a2', 'code'],
          dataLabels: {
            enabled: true,
            color: 'white',
            style: {
              fontWeight: 'bold'
            }
          },
          mapData: maps,
          tooltip: {
            headerFormat: '',
            pointFormat: '{point.name}: <b>{series.name}</b>'
          }

        }
      },
      series: [{
        name: 'UTC',
        data: ['IE', 'IS', 'GB', 'PT'].map(function (code) {
          return { code: code };
        })
      }, {
        name: 'UTC + 1',
        data: ['NO', 'SE', 'DK', 'DE', 'NL', 'BE', 'LU', 'ES', 'FR', 'PL', 'CZ', 'AT', 'CH', 'LI', 'SK', 'HU', 'SI', 'IT', 'SM', 'HR', 'BA', 'YF', 'ME', 'AL', 'MK'].map(function (code) {
          return { code: code };
        })
      }]
    }
  }

  render () { console.info('------ MapChart.render')
    return (
      <div id='highchart-container'>
        <ReactHighchart config={this.data} isPureConfig/>
      </div>
    )
  }
}

export default MapChart

