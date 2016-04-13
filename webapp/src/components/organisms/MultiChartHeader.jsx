import _ from 'lodash'
import React, {PropTypes} from 'react'

import IconButton from 'components/atoms/IconButton'
import ExportIcon from 'components/atoms/ExportIcon'
import TitleInput from 'components/molecules/TitleInput'

const MultiChartHeader = React.createClass({

  propTypes: {
    chart: PropTypes.object,
    setTitle: PropTypes.func,
    toggleEditMode: PropTypes.func,
    toggleSelectTypeMode: PropTypes.func,
    duplicateChart: PropTypes.func,
    saveChart: PropTypes.func,
    removeChart: PropTypes.func
  },

  getInitialState () {
    return {
      titleEditMode: false
    }
  },

  _toggleTitleEdit (title) {
    if (_.isString(title)) {
      this.props.setTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  render () {
    const props = this.props
    const chart = props.chart

    const remove_button = props.removeChart ? (
      <IconButton onClick={() => props.removeChart(chart.uuid)} icon='fa-times' text='Remove' />
    ) : null

    const duplicate_button = props.duplicateChart ? (
      <IconButton onClick={() => props.duplicateChart(chart.uuid)} icon='fa-copy' text='Duplicate' />
    ) : null

    const show_options_button = (
      <IconButton
        onClick={props.toggleEditMode}
        icon='fa-angle-double-left'
        text='Show Options'
        className={'chart-options-button ' + (chart.editMode ? 'hidden' : null) } />
    )

    return (
      <header className='row'>
        <div className='medium-12 columns chart-header text-center'>
          {
            this.state.titleEditMode ?
            <TitleInput initialText={chart.title} save={this._toggleTitleEdit}/>
            :
            <h2>
              <a onClick={this._toggleTitleEdit} style={{cursor: 'text'}}>
                {chart.title || 'Untitled Chart'}
              </a>
            </h2>
          }
         <div className='chart-actions'>
            {
              !props.readOnlyMode ?
                <span className='animated fadeInRight'>
                  <IconButton onClick={props.toggleSelectTypeMode} icon='fa-bar-chart' text='Change chart type' />
                  <ExportIcon exportPath={'/charts/' + chart.id}/>
                  <IconButton isBusy={chart.saving} onClick={() => props.saveChart(chart.uuid)} icon='fa-save' text='Save' alt_text='Saving ...'/>
                  { /* duplicate_button */ }
                  { remove_button }
                </span>
              : null
            }
            { show_options_button }
          </div>
        </div>
      </header>
    )
  }
})

export default MultiChartHeader
