import React, { Component, PropTypes } from 'react'
import builderDefinitions from 'components/molecules/charts_d3/utils/builderDefinitions'
import TitleInput from 'components/molecules/TitleInput'
import ChartSelect from 'components/organisms/chart-wizard/ChartSelect'
import PalettePicker from 'components/organisms/chart-wizard/preview/PalettePicker'

class ChartProperties extends Component {
  render () {
    const props = this.props
    return (
      <footer className='row'>
        <div className='medium-6 columns'>
          <h3>Chart Type</h3>
          <ChartSelect
            charts={builderDefinitions.charts}
            value={props.chart.def.type}
            onChange={props.selectChartType}/>
        </div>
        <div className='medium-2 columns'>
          <h3>Color Scheme</h3>
          <PalettePicker
            value={props.chart.def.palette}
            onChange={props.selectPalette}/>
        </div>
        <div className='medium-4 columns'>
          <div className='medium-8 columns'>
            <h3>Chart Title</h3>
            <TitleInput initialText={props.chart.def.title} save={props.saveTitle}/>
          </div>
          <div className='medium-4 columns'>
            <button className='right button success' disabled={!props.chart.data} onClick={props.saveChart}>
              <i className='fa fa-save'></i> Save Chart
            </button>
          </div>
        </div>
      </footer>
    )
  }
}

ChartProperties.propTypes = {
  chart: PropTypes.object,
  selectChartType: PropTypes.func,
  selectPalette: PropTypes.func,
  saveTitle: PropTypes.func,
  saveChart: PropTypes.func
}

ChartProperties.defaultProps = {
  selected_palette: 'orange',
  selected_chart_type: 'RawData',
  chart_title: ''
}

export default ChartProperties