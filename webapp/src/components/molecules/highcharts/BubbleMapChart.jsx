import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import palettes from 'utilities/palettes'
import format from 'utilities/format'

class BubbleMap extends HighChart {
  setConfig = function () {
    this.config = {
      legend: {
        enabled: false
      },
      series: this.setSeries(),
      mapNavigation: {
        enabled: true,
        enableMouseWheelZoom: false,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      }
    }
  }

  setSeries = function () {
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
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
      tooltip: {
        pointFormatter: function() {
          return (
            `<span> ${props.locations_index[this.location_id].name}:
            <strong> ${format.autoFormat(this.z, current_indicator.data_format)} </strong>
            </span>`
          )
        }
      }
    }]
  }
}

export default BubbleMap
