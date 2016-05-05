import React from 'react'

import Select from 'components/atoms/select/Select'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

var IndicatorSelect = React.createClass({
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
      selected: {'name': 'Loading ...'}
    }
  },

  setPattern (value) {
    this.setState({ pattern: value })
    this.forceUpdate()
  },

  render () {
    this.indicators = this.props.indicators.filter(i => this.props.idsToRender.indexOf(i.id) !== -1)
    const selected_text = !this.props.selected.id && this.indicators.length > 0 ? 'Select Indicator' : this.props.selected.name
    const pattern = this.state.pattern
    const filtered_items = pattern.length > 2 ? this.indicators.filter(i => new RegExp(pattern, 'i').test(i.name)) : this.indicators
    const indicator_menu_items = filtered_items.map(indicator =>
      <DropdownMenuItem
        key={'indicator-' + indicator.id}
        text={indicator.name}
        onClick={this.props.sendValue.bind(this, indicator.id)}
        classes='indicator'
      />
    )

    return (
      <Select
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={selected_text}
        searchable
        onSearch={this.setPattern}>
        {indicator_menu_items}
      </Select>
    )
  }
})

export default IndicatorSelect
