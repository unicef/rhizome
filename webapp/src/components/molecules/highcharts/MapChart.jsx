import _ from 'lodash'
import React, { Component, PropTypes } from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'

import format from 'utilities/format'
import maps from './map_data'

class MapChart extends HighChart {

  constructor (props) {
    super(props)

    const first_indicator = props.selected_indicators[0]
    this.data = {
      chart: {
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

}

export default MapChart

