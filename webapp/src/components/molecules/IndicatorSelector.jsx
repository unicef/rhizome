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
      list: PropTypes.object
    }).isRequired,
    preset_indicator_ids: PropTypes.array,
    classes: PropTypes.string,
    multi: PropTypes.bool
  },

  getDefaultProps() {
    return {
      multi: false,
      preset_indicator_ids: null
    }
  },

  componentDidMount () {
    IndicatorStore.listen(indicators => {
      this.indicators_index = indicators.index
      this.indicators_raw = indicators.raw
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
        <h3>{ props.multi ? 'Indicators' : 'Indicator' }</h3>
        {
          props.multi ?
          <form>
            <DropdownMenu
              items={props.indicators.list}
              sendValue={IndicatorSelectorActions.selectIndicator}
              item_plural_name='Indicators'
              style='icon-button right'
              icon='fa-plus'
            />
            <a className='remove-filters-link' onClick={IndicatorSelectorActions.clearSelectedIndicators}>Remove All </a>
            <ReorderableList items={this.state.selected_indicators} removeItem={IndicatorSelectorActions.deselectIndicator} dragItem={IndicatorSelectorActions.reorderIndicator} />
          </form>
          :
          props.indicators.raw ?
            <IndicatorTitleMenu
              idsToRender={props.indicators.raw.map(indicator => indicator.id)}
              indicators={props.indicators.raw}
              selected={this.state.selected_indicators[0]}
              sendValue={IndicatorSelectorActions.selectIndicator}
            />
          : ''
        }
      </div>

    )
  }
})

export default IndicatorSelector
