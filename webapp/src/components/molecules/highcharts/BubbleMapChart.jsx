import React from 'react'

import HighChart from 'components/molecules/highcharts/HighChart'
import format from 'utilities/format'

class BubbleMapChart extends HighChart {

  setConfig = function () {
    const current_indicator = this.props.selected_indicators[0]
    // const palette = this.getColorPalette(this.props.palette)
    this.config = {
      mapNavigation: {
        enabled: true,
        enableMouseWheelZoom: false,
        buttonOptions: {
          verticalAlign: 'bottom'
        }
      },
      chart: {
        type: 'map'
      },
      legend: {
        enabled: false
      },
      series: this.setSeries()
    }
  }

  setSeries = function () {
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    let mapData = {'features': this.props.features, 'type': 'FeatureCollection'}
    //first object config for empty map
    //second object config for bubbles
    return [
      {
        name: 'base map',
        mapData: mapData,
        color: '#E0E0E0',
        enableMouseTracking: false
      },
      {
        type: 'mapbubble',
        mapData: mapData,
        name: current_indicator.name,
        joinBy: 'location_id',
        data: this.props.datapoints.meta.chart_data,
        minSize: 4,
        maxSize: '12%',
        tooltip: {
            pointFormat: '{point.z}'
        },
        color: '#000000'
      }
    ]
  }
  //move back into setSeries and customize when bubblemap is working
  // tooltip: {
  //       pointFormatter: function() {
  //         return (
  //           `<span> ${props.locations_index[this.location_id].name}:
  //           <strong> ${format.autoFormat(this.value, current_indicator.data_format)} </strong>
  //           </span>`
  //         )
  //       }
  //     }

  // getDataClasses (current_indicator, palette) {
  //   if (current_indicator.good_bound < current_indicator.bad_bound) {
  //     let temp_bound = current_indicator.good_bound
  //     current_indicator.good_bound = current_indicator.bad_bound
  //     current_indicator.bad_bound = temp_bound
  //     palette = palette.reverse()
  //   }
  //   let dataClasses = null
  //   if (current_indicator.data_format === 'bool') {
  //     dataClasses = [{to: current_indicator.bad_bound,color: palette[0]},
  //                    {from: current_indicator.good_bound,color: palette[2]}]
  //   } else {
  //     dataClasses = [{from:0, to:current_indicator.bad_bound, color:palette[0]},
  //                    {from:current_indicator.bad_bound, to:current_indicator.good_bound, color:palette[1]},
  //                    {from:current_indicator.good_bound, color:palette[2]}]
  //   }
  //   return dataClasses
  // }

  // getColorPalette (paletteType) {
  //   return paletteType === 'traffic_light' ? ['#FF9489', '#FFED89', '#83F5A2'] : []
  // }
}

export default BubbleMapChart
