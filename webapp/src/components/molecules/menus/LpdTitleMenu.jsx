import React from 'react'

import TitleMenu from 'components/molecules/menus/TitleMenu'
import TitleMenuItem from 'components/molecules/menus/TitleMenuItem'

var LpdTitleMenu = React.createClass({
  propTypes: {
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    idsToRender: React.PropTypes.array
  },

  getDefaultProps () {
    return {
      statuses: [],
      idsToRender: [],
      selected: {'name':'Loading ...'}
    }
  },

  render () {
    const lpd_statuses = [
      { id: 1, name: 'LPD 1'}, { id: 2, name: 'LPD 2'}, { id: 3, name: 'LPD 3'}
    ]

    const selected_text = !this.props.selected.id ? 'LPD Status' : this.props.selected.name

    const indicator_menu_items = lpd_statuses.map(status =>
      <TitleMenuItem
        key={'status-' + status.id}
        text={status.name}
        onClick={() => this.props.sendValue(status.id)}
        classes='status'
      />
    )

    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        searchable={false}
        text={selected_text}>
        {indicator_menu_items}
      </TitleMenu>
    )
  }
})

export default LpdTitleMenu
