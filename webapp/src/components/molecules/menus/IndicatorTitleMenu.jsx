import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'components/molecules/menus/TitleMenu'
import TitleMenuItem from 'components/molecules/menus/TitleMenuItem'

var IndicatorTitleMenu = React.createClass({
  propTypes: {
    indicators: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  render () {
    const indicator_menu_items = this.props.indicators.map(indicator =>
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
        text={this.props.selected.name}>
        {indicator_menu_items}
      </TitleMenu>
    )
  }
})

export default IndicatorTitleMenu
