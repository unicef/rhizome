import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import IndicatorTitleMenu from 'components/molecules/menus/IndicatorTitleMenu'


const IndicatorSelector = React.createClass({

  propTypes: {
    indicators: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    selected_indicators: PropTypes.array,
    setIndicators: PropTypes.func,
    selectIndicator: PropTypes.func,
    deselectIndicator: PropTypes.func,
    clearSelectedIndicators: PropTypes.func,
    reorderIndicator: PropTypes.func,
    classes: PropTypes.string,
    multi: PropTypes.bool,
    avoidBooleans: PropTypes.bool
  },

  getDefaultProps () {
    return {
      avoidBooleans: false,
      multi: false,
      selected_indicators: []
    }
  },

  getAvailableIndicators () {
    const selected_ids = this.props.selected_indicators.map(indicator => indicator.id)
    const indicators_list = this.props.indicators.list
    indicators_list.forEach(indicator_group => {
      indicator_group.children.forEach(indicator => {
        indicator.disabled = selected_ids.indexOf(indicator.id) > -1
      })
    })
    return indicators_list
  },

  render () {
    const props = this.props
    const raw_indicators = props.indicators.raw || []
    if (props.multi) {
      const available_indicators = this.getAvailableIndicators()
      return (
        <form className={props.classes}>
          <h3>Indicators
            <DropdownMenu
              items={available_indicators}
              sendValue={this.props.selectIndicator}
              item_plural_name='Indicators'
              style='icon-button right'
              icon='fa-plus'
            />
          </h3>
          { props.selected_indicators.length > 0 ? <a className='remove-filters-link' onClick={props.clearSelectedIndicators}>Remove All </a> : '' }
          <ReorderableList items={props.selected_indicators} removeItem={props.deselectIndicator} dragItem={props.reorderIndicator} />
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Indicator</h3>
          <IndicatorTitleMenu
            idsToRender={raw_indicators.map(indicator => indicator.id)}
            indicators={props.avoidBooleans ? raw_indicators.filter(i => i.data_format !== 'bool') : raw_indicators}
            selected={props.selected_indicators[0]}
            sendValue={props.setIndicators}
          />
        </div>
      )
    }
  }
})

export default IndicatorSelector
