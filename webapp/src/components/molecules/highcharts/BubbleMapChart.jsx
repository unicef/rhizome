import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class BubbleMapChart extends HighChart {

      // legend: {
      //   layout: 'vertical',
      //   align: 'right',
      //   labelFormatter: function () {
      //     const boundTo = !isNaN(this.to) ? format.autoFormat(this.to, current_indicator.data_format) : null
      //     const boundFrom = !isNaN(this.from) ? format.autoFormat(this.from, current_indicator.data_format) : null
      //     const isBool = current_indicator.data_format === 'bool'
      //     return (
      //           (boundFrom || (isBool ? '' : '0')) +
      //           (isBool ? '': boundTo ? ' - ' : ' ') +
      //           (boundTo || (isBool ? '' : '+'))
      //     )
      //   },
      //   itemStyle: {
      //     'fontSize': '16px'
      //   }
      // },
      // colorAxis: {
      //   dataClasses: this.getDataClasses(current_indicator, palette),
      //   reversed: current_indicator.good_bound < current_indicator.bad_bound
      // },

  setConfig = function () {
    const current_indicator = this.props.selected_indicators[0]
    const palette = this.getColorPalette(this.props.palette)
    this.config = {
      mapNavigation: {
        enabled: true,
        enableMouseWheelZoom: false,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    return [{
      data: this.props.datapoints.meta.chart_data,
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      joinBy: 'location_id',
      name: current_indicator.name
    }]
  }
  // tooltip: {
  //       pointFormatter: function() {
  //         return (
  //           `<span> ${props.locations_index[this.location_id].name}:
  //           <strong> ${format.autoFormat(this.value, current_indicator.data_format)} </strong>
  //           </span>`
  //         )
  //       }
  //     }

  getDataClasses (current_indicator, palette) {
    if (current_indicator.good_bound < current_indicator.bad_bound) {
      let temp_bound = current_indicator.good_bound
      current_indicator.good_bound = current_indicator.bad_bound
      current_indicator.bad_bound = temp_bound
      palette = palette.reverse()
    }
    let dataClasses = null
    if (current_indicator.data_format === 'bool') {
      dataClasses = [{to: current_indicator.bad_bound,color: palette[0]},
                     {from: current_indicator.good_bound,color: palette[2]}]
    } else {
      dataClasses = [{from:0, to:current_indicator.bad_bound, color:palette[0]},
                     {from:current_indicator.bad_bound, to:current_indicator.good_bound, color:palette[1]},
                     {from:current_indicator.good_bound, color:palette[2]}]
    }
    return dataClasses
  }

  getColorPalette (paletteType) {
    return paletteType === 'traffic_light' ? ['#FF9489', '#FFED89', '#83F5A2'] : []
  }
}

export default BubbleMapChart
