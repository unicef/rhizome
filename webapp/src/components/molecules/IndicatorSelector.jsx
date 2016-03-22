import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

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
      list: PropTypes.array
    }).isRequired,
    preset_indicator_ids: PropTypes.array,
    classes: PropTypes.string
  },

  getDefaultProps() {
    return {
      preset_indicator_ids: null
    }
  },

  componentDidMount () {
    IndicatorStore.listen(indicators => {
      this.indicators_index = indicators.index
      if (this.props.preset_indicator_ids) {
        IndicatorSelectorActions.setSelectedIndicators(this.props.preset_indicator_ids)
      }
    })
  },

  componentWillReceiveProps(nextProps) {
    if (!_.isEmpty(nextProps.preset_indicator_ids)) {
      this.setState({selected_indicators: nextProps.preset_indicator_ids.map(id => this.indicators_index[id])})
    }
  },

  render () {
    const props = this.props

    return (
      <div className={props.classes}>
        <h3>
          <DropdownMenu
            items={props.indicators.list}
            sendValue={IndicatorSelectorActions.selectIndicator}
            item_plural_name='Indicators'
            style='icon-button right'
            icon='fa-plus' />
          Indicators
        </h3>
        <a className='remove-filters-link' onClick={IndicatorSelectorActions.clearSelectedIndicators}>Remove All </a>
        <ReorderableList items={this.state.selected_indicators} removeItem={IndicatorSelectorActions.deselectIndicator} dragItem={IndicatorSelectorActions.reorderIndicator} />
      </div>
    )
  }
})

export default IndicatorSelector
