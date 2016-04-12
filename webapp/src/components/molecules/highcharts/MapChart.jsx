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
    const self = this
    const currentIndicator = this.props.selected_indicators[0]
    const currentLocation = this.props.selected_locations[0]
    let locationNames = {}
    this.props.datapoints.meta.chart_data.forEach(datapoint => {
      locationNames[datapoint.location_id] = self.props.locations_index[datapoint.location_id].name
    })
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
          return ("<span><b>" + format.autoFormat(this.value, currentIndicator.data_format) +
                  "</b></span><br>" + locationNames[this.location_id])
        }
      }
    }]
  }
}

export default MapChart
