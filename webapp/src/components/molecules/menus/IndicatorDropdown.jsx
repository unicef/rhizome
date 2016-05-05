import React from 'react'

import Dropdown from 'components/atoms/dropdowns/DropdownSelect'
import DropdownItem from 'components/atoms/dropdowns/DropdownItem'

var IndicatorDropdown = React.createClass({
  propTypes: {
    indicators: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    idsToRender: React.PropTypes.array
  },

  getInitialState () {
    return {
      pattern: ''
    }
  },

  getDefaultProps () {
    return {
      indicators: [],
      idsToRender: [],
      selected: {'name':'Loading ...'}
    }
  },

  setPattern (value) {
    this.setState({ pattern: value })
    this.forceUpdate()
  },

  indicatorsFilteredBySet(){
    //grab current indicators based on camp/location.
    const currentIndicators = this.props.indicators.filter(indicator =>
        this.props.idsToRender.indexOf(indicator.id) !== -1
      )
    return currentIndicators
  },

  filteredMenuItems () {
    if (this.state.pattern.length > 2) {
      return this.indicators.filter(indicator => {
        return new RegExp(this.state.pattern, 'i').test(indicator.name)
      })
    } else {
      return this.indicators
    }
  },

  render () {
    this.indicators = this.indicatorsFilteredBySet()
    const selected_text = !this.props.selected.id && this.indicators.length > 0 ? 'Select Indicator' : this.props.selected.name
    const indicator_menu_items = this.filteredMenuItems().map(indicator =>
      <DropdownItem
        key={'indicator-' + indicator.id}
        text={indicator.name}
        onClick={this.props.sendValue.bind(this, indicator.id)}
        classes='indicator'
      />
    )

    return (
      <Dropdown
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable
        onSearch={this.setPattern}>
        {indicator_menu_items}
      </Dropdown>
    )
  }
})

export default IndicatorDropdown
