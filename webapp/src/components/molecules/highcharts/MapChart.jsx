import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class MapChart extends HighChart {
  setConfig () {
    this.config = {
      mapNavigation: {
        enabled: true,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      },
      colorAxis: {
        min: 0
      },
      series: this.setSeries()
    }
  }

  setSeries () {
    const currentIndicator = this.props.selected_indicators[0]
    return [{
      data: this.props.datapoints.meta.chart_data,
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      joinBy: 'location_id',
      name: currentIndicator.name,
      states: {
        hover: {
          color: '#BADA55'
        }
      },
      tooltip: {
        pointFormatter: function(){
          return "<span><b>" + format.autoFormat(this.value, currentIndicator.data_format) + "</b></span>"
        }
      }
    }]
  }
}

export default MapChart
