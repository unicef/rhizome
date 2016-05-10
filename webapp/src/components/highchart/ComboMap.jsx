import React from 'react'
import _ from 'lodash'
import HighChart from 'components/highchart/HighChart'
import palettes from 'utilities/palettes'
import format from 'utilities/format'

class ComboMap extends HighChart {

  setConfig = function () {
    const current_indicator = this.props.selected_indicators[0]
    const palette = palettes[this.props.palette]
    const integerWithBounds = current_indicator.data_format === 'int' && current_indicator.good_bound < 2 && current_indicator.bad_bound < 2
    this.config = {
      series: this.setSeries(),
      colorAxis: {min: 0},
      mapNavigation: {
        enabled: false,
        enableTouchZoom: false,
        enableDoubleClickZoom: false,
        enableMouseWheelZoom: false,
        enableButtons: false
      }
    }
    if (!integerWithBounds) {
      this.config.colorAxis = {
        dataClasses: this.getDataClasses(current_indicator, palette),
      }
      this.config.legend = {
        layout: 'vertical',
        align: 'right',
        itemStyle: { 'fontSize': '14px' },
        labelFormatter: function () {
          const boundTo = !isNaN(this.to) ? format.autoFormat(this.to, current_indicator.data_format) : null
          const boundFrom = !isNaN(this.from) ? format.autoFormat(this.from, current_indicator.data_format) : null
          const isBool = current_indicator.data_format === 'bool'
          return (boundFrom || isBool ? '' : '0') + (isBool ? '': boundTo ? ' - ' : ' ') + (boundTo || isBool ? '' : '+')
        }
      }
    }

    const clickMap = this.props.onMapClick
    if (clickMap) {
      this.config.plotOptions = {
        series: {
          cursor: 'pointer',
          point: {
            events: {
              click: function (e) { clickMap(this.location_id) }
            }
          }
        }
      }
    }
  }

  setSeries = function () {
    const self = this
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    const base_map_series = {
      mapData: {'features': this.props.features, 'type': 'FeatureCollection'},
      joinBy: 'location_id',
      tooltip: {
        pointFormatter: function () { return self.tooltipFormatter(this) }
      }
    }

    const map_colors = Object.assign({}, base_map_series, {
      data: this.props.datapoints.meta.chart_data,
      name: current_indicator.name,
      borderColor: 'black',
      nullColor: '#D3D3D3',
      states: {
        hover: {
          color: "rgba(163, 232, 255, 1.0)"
        }
      }
    })

    const map_bubbles = Object.assign({}, base_map_series, {
      type: 'mapbubble',
      data: props.datapoints.meta.chart_data.map(d => ({z: d.value, location_id: d.location_id})),
      joinBy: 'location_id',
      minSize: 4,
      maxSize: '12%',
      color: this.props.indicator_colors[current_indicator.id]
    })

    return [map_colors, map_bubbles]
  }


  tooltipFormatter = function (point) {
    const props = this.props
    const current_indicator = this.props.selected_indicators[0]
    const value = point.value || point.z
    return (
      `<span> ${props.locations_index[point.location_id].name}:
      <strong> ${format.autoFormat(value, current_indicator.data_format, 1)} </strong>
      </span>`
    )
  }

  getDataClasses = function (current_indicator, palette) {
    let temp_good, temp_bad
    if (current_indicator.good_bound < current_indicator.bad_bound) {
      let temp_bound = current_indicator.good_bound
      temp_good = current_indicator.bad_bound
      temp_bad = temp_bound
      palette = _.clone(palette).reverse()
    }
    let dataClasses = null
    if (current_indicator.data_format === 'bool') {
      dataClasses = [{to: temp_bad,color: palette[0]},
                     {from: temp_good,color: palette[2]}]
    } else {
      dataClasses = [{from:0, to:temp_bad, color:palette[0]},
                     {from:temp_bad, to:temp_good, color:palette[1]},
                     {from:temp_good, color:palette[2]}]
    }
    return dataClasses
  }
}

export default ComboMap
