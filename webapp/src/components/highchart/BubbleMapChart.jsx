import React from 'react'

import HighChart from 'components/highchart/HighChart'
import palettes from 'utilities/palettes'
import format from 'utilities/format'

class BubbleMap extends HighChart {
  setConfig = function () {
    this.config = {
      legend: {
        enabled: false
      },
      exporting: {
        buttons: {
          customButton: {
            text: 'Labels',
            onclick: this._toggleLabels,
            x: -65,
            y: -15,
            theme: {
              style: {
                color: '#039',
                textDecoration: 'underline'
              }
            }
          }
        }
      },
      mapNavigation: {
        enabled: false,
        enableTouchZoom: false,
        enableDoubleClickZoom: false,
        enableMouseWheelZoom: false,
        enableButtons: false
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    const color = this.props.indicator_colors[current_indicator.id]
    return [{
      mapData:  {'features': this.props.features, 'type': 'FeatureCollection'},
      color: '#E0E0E0',
      enableMouseTracking: false
    }, {
      name: current_indicator.name,
      type: 'mapbubble',
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      data: props.datapoints.flattened.map(d => ({z: d.value, location_id: d.location.id})),
      joinBy: 'location_id',
      dataLabels: {
        enabled: false,
        color: '#000',
        allowOverlap: true,
        formatter: function () {
          const location = props.locations_index[this.point.location_id]
          const value = format.autoFormat(this.point.z, current_indicator.data_format, 1)
          return location.name + '<br>' + value
        }
      },
      minSize: 4,
      maxSize: '12%',
      color: color,
      tooltip: {
        pointFormatter: function() {
          return (
            `<span> ${props.locations_index[this.location_id].name}:
            <strong> ${format.autoFormat(this.z, current_indicator.data_format, 1)} </strong>
            </span>`
          )
        }
      }
    }]
  }

  _toggleLabels = () => {
    const self = this
    var opt = this.chart.series[1].options;
    opt.dataLabels.enabled = !opt.dataLabels.enabled;
    this.chart.series[1].update(opt);
  }
}

export default BubbleMap
