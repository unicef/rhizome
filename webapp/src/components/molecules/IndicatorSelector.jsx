import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import ReorderableList from 'components/molecules/list/ReorderableList'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

import IndicatorSelectorStore from 'stores/IndicatorSelectorStore'
import IndicatorSelectorActions from 'actions/IndicatorSelectorActions'

const IndicatorSelector = React.createClass({
  mixins: [
    Reflux.connect(IndicatorSelectorStore, 'selected_indicators'),
  ],

  propTypes: {
    indicators: PropTypes.shape({
      list: PropTypes.array
    }).isRequired,
    classes: PropTypes.string
  },

  render () {
    const props = this.props

    return (
      <div className={props.classes}>
        <h3>
          Indicators
          <DropdownMenu
            items={props.indicators.list}
            sendValue={IndicatorSelectorActions.selectIndicator}
            item_plural_name='Indicators'
            style='icon-button right'
            icon='fa-plus' />
        </h3>
        <a className='remove-filters-link' onClick={IndicatorSelectorActions.clearSelectedIndicators}>Remove All </a>
        <ReorderableList items={this.state.selected_indicators} removeItem={IndicatorSelectorActions.deselectIndicator} dragItem={IndicatorSelectorActions.reorderIndicator} />
      </div>
    )
  }
})

export default IndicatorSelector
