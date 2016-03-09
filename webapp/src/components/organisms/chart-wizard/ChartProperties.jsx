import React, { Component, PropTypes } from 'react'
import builderDefinitions from 'stores/chartBuilder/builderDefinitions'
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
            value={props.selected_chart_type}
            onChange={props.selectChartType}/>
        </div>
        <div className='medium-2 columns'>
          <h3>Color Scheme</h3>
          <PalettePicker
            value={props.selected_palette}
            onChange={props.selectPalette}/>
        </div>
        <div className='medium-4 columns'>
          <div className='medium-8 columns'>
            <h3>Chart Title</h3>
            <TitleInput initialText={props.chart_title} save={props.saveTitle}/>
          </div>
          <div className='medium-4 columns'>
            <button className='right button success' disabled={props.chartIsReady} onClick={props.saveChart}>
              <i className='fa fa-save'></i> Save Chart
            </button>
          </div>
        </div>
      </footer>
    )
  }
}

ChartProperties.propTypes = {
  selected_chart_type: PropTypes.string,
  selected_palette: PropTypes.string,
  chart_title: PropTypes.string,
  selectChartType: PropTypes.func,
  selectPalette: PropTypes.func,
  saveTitle: PropTypes.func,
  saveChart: PropTypes.func,
  chartIsReady: PropTypes.bool
}

ChartProperties.defaultProps = {
  selected_palette: 'orange',
  selected_chart_type: 'RawData',
  chart_title: '',
  chartIsReady: false
}

export default ChartProperties