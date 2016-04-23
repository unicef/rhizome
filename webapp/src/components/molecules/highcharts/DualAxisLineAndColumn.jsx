import _ from 'lodash'
import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class DualAxisLineAndColumn extends HighChart {

  setConfig = function () {
    const props = this.props
    const first_indicator = props.selected_indicators[0]
    const locations = props.datapoints.raw.map(datapoint => props.locations_index[datapoint.location])

    this.config = {
      chart: {
            zoomType: 'xy',
            // type: 'combo-dual-axes'
        },
        title: {
            text: 'Average Monthly Temperature and Rainfall in Tokyo'
        },
        subtitle: {
            text: 'Source: WorldClimate.com'
        },
        xAxis: [{
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            crosshair: true
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}°C',
                style: {
                    color: '#502d17'
                }
            },
            title: {
                text: 'Temperature',
                style: {
                    color: '#00059a'
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Rainfall',
                style: {
                    color: '#b00099'
                }
            },
            labels: {
                format: '{value} mm',
                style: {
                    color: '#fff9c5'
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: '#FFFFFF'
        },
    }
  }

  setSeries = function () {

    const series =  [{
           name: 'Rainfall',
           type: 'column',
           yAxis: 1,
           data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
           tooltip: {
               valueSuffix: ' mm'
           }

       }, {
           name: 'Temperature',
           type: 'spline',
           data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
           tooltip: {
               valueSuffix: '°C'
           }
       }]
    return series
  }
}

export default DualAxisLineAndColumn
