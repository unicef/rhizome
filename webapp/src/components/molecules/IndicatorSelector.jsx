import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import IndicatorTitleMenu from 'components/molecules/menus/IndicatorTitleMenu'

import IndicatorStore from 'stores/IndicatorStore'
import IndicatorSelectorStore from 'stores/IndicatorSelectorStore'
import IndicatorSelectorActions from 'actions/IndicatorSelectorActions'

const IndicatorSelector = React.createClass({
  mixins: [
    Reflux.connect(IndicatorSelectorStore, 'selected_indicators'),
  ],

  indicators_index: null,

  propTypes: {
    indicators: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    preset_indicator_ids: PropTypes.array,
    classes: PropTypes.string,
    multi: PropTypes.bool
  },

  getDefaultProps () {
    return {
      multi: false,
      preset_indicator_ids: null
    }
  },

  componentDidMount () {
    IndicatorStore.listen(indicators => {
      if (this.props.preset_indicator_ids && indicators.index) {
        IndicatorSelectorActions.setSelectedIndicators(this.props.preset_indicator_ids)
      }
    })
  },

  componentWillReceiveProps(nextProps) {
    if (!_.isEmpty(nextProps.preset_indicator_ids) && nextProps.indicators.index && _.isEmpty(this.state.selected_indicators)) {
      this.setState({selected_indicators: nextProps.preset_indicator_ids.map(id => nextProps.indicators.index[id])})
    }
  },

  getAvailableIndicators () {
    const selected_ids = this.state.selected_indicators.map(indicator => indicator.id)
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
              sendValue={IndicatorSelectorActions.selectIndicator}
              item_plural_name='Indicators'
              style='icon-button right'
              icon='fa-plus'
            />
          </h3>
          <a className='remove-filters-link' onClick={IndicatorSelectorActions.clearSelectedIndicators}>Remove All </a>
          <ReorderableList items={this.state.selected_indicators} removeItem={IndicatorSelectorActions.deselectIndicator} dragItem={IndicatorSelectorActions.reorderIndicator} />
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Indicator</h3>
          <IndicatorTitleMenu
            idsToRender={raw_indicators.map(indicator => indicator.id)}
            indicators={raw_indicators}
            selected={this.state.selected_indicators[0]}
            sendValue={IndicatorSelectorActions.setSelectedIndicators}
          />
        </div>
      )
    }
  }
})

export default IndicatorSelector
