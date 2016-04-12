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
    const indicators_list = this.props.indicators.list
    const selected_ids = this.props.selected_indicators.map(indicator => indicator.id)
    indicators_list.forEach(indicator_group => {
      this.markDisabledIndicators(indicator_group.children, selected_ids)
    })
    return indicators_list
  },

  markDisabledIndicators (items, selected_ids) {
    items.forEach(item => {
      item.disabled = selected_ids.indexOf(item.id) > -1
      if (item.children && item.children.length > 0) {
        this.markDisabledIndicators(item.children, selected_ids)
      }
    })
    return items
  },

  render () {
    const props = this.props
    const raw_indicators = props.indicators.raw || []
    const available_indicators = this.getAvailableIndicators()
    if (props.multi) {
      return (
        <form className={props.classes}>
          <h3 style={{marginBottom: '.1rem'}}>Indicators
            <DropdownMenu
              items={available_indicators}
              sendValue={this.props.selectIndicator}
              item_plural_name='Indicators'
              style='icon-button right pad-right'
              icon='fa-plus'
            />
          </h3>
          <ReorderableList items={props.selected_indicators} removeItem={props.deselectIndicator} dragItem={props.reorderIndicator} />
          { props.selected_indicators.length > 1 ? <a className='remove-filters-link' onClick={props.clearSelectedIndicators}>Remove All </a> : '' }
        </form>
      )
    } else {
      const selected_indicator = _.isEmpty(this.props.selected_indicators) ? {name: 'Select Indicator'} : this.props.selected_indicators[0]
      return (
        <form className={props.classes}>
          <h3>Indicator</h3>
          <DropdownMenu
            items={available_indicators}
            sendValue={this.props.setIndicators}
            item_plural_name='Indicators'
            style='dropdown-list'
            text={selected_indicator.name}
          />
        </form>
      )
    }
  }
})

export default IndicatorSelector
