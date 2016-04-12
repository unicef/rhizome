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
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    return [{
      data: this.props.datapoints.meta.chart_data,
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      joinBy: 'location_id',
      name: current_indicator.name,
      states: {
        hover: {
          color: '#BADA55'
        }
      },
      tooltip: {
        pointFormatter: function() {
          return (
            '<span> '+ props.locations_index[this.location_id].name
            + '<strong> '+ format.autoFormat(this.value, current_indicator.data_format) + ' </strong>'
            + '</span>'
          )
        }
      }
    }]
  }
}

                  // "</b></span><br>" + location_names[this.location_id])
export default MapChart
