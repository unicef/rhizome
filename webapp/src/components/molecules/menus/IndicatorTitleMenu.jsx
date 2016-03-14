import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'components/molecules/menus/TitleMenu'
import TitleMenuItem from 'components/molecules/menus/TitleMenuItem'

var IndicatorTitleMenu = React.createClass({
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
      return this.props.indicators.filter(indicator => {
        return new RegExp(this.state.pattern, 'i').test(indicator.name)
      })
    } else {
      return this.props.indicators
    }
  },
  render () {
    this.props.indicators = this.indicatorsFilteredBySet()
    const indicator_menu_items = this.filteredMenuItems().map(indicator =>
      <TitleMenuItem
        key={'indicator-' + indicator.id}
        text={indicator.name}
        onClick={this.props.sendValue.bind(this, indicator.id)}
        classes='indicator'
      />
    )

    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={this.props.selected.name}
        searchable
        onSearch={this.setPattern}>
        {indicator_menu_items}
      </TitleMenu>
    )
  }
})

export default IndicatorTitleMenu
