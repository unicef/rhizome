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
      data: this.props.datapoints.meta.chart_data,
      joinBy: 'location_id',
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
}

export default BubbleMap
