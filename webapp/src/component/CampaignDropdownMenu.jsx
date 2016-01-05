import _ from 'lodash'
import React from 'react'
import moment from 'moment'

import DropdownMenu from 'component/DropdownMenu.jsx'
import CampaignMenuItem from 'component/CampaignMenuItem.jsx'

function searchValue (campaign) {
  var m = moment(campaign.start_date)

  // Include several possible date formats for matching against
  return [
    m.format('YYYY-MM'),
    m.format('MM-YYYY'),
    m.format('YYYY-M'),
    m.format('M-YYYY'),
    m.format('MMMM YYYY'),
    m.format('YYYY/MM'),
    m.format('MM/YYYY'),
    m.format('YYYY/M'),
    m.format('M/YYYY'),
    m.format('YY-MM'),
    m.format('MM-YY'),
    m.format('YY-M'),
    m.format('M-YY'),
    m.format('MMMM YY'),
    m.format('YY/MM'),
    m.format('MM/YY'),
    m.format('YY/M'),
    m.format('M/YY')
  ].join(' ')
}

var CampaignDropdownMenu = React.createClass({
  propTypes: {
    campaigns: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  render: function () {
    var re = new RegExp(this.state.pattern, 'i')

    // If the pattern is longer than two characters, filter the list with it,
    // otherwise, return true to include all campaigns in the dropdown
    var filterCampaigns = !_.isEmpty(this.state.pattern)
      ? _.flow(searchValue, function (v) { return re.test(v) })
      : _.constant(true)

    var campaigns = _(this.props.campaigns)
      .filter(filterCampaigns)
      .sortBy(_.method('start_date.getTime'))
      .reverse()
      .map(campaign => {
        return (
          <CampaignMenuItem
            campaign={campaign}
            key={'campaign-' + campaign.id}
            sendValue={this.props.sendValue} />
        )
      })
      .value()

    var props = _.omit(this.props, 'campaigns', 'sendValue')

    return (
      <DropdownMenu icon='fa-calendar'
        searchable
        onSearch={this._setPattern}
        {...props}>

        {campaigns}

      </DropdownMenu>
    )
  },

  _setPattern: function (value) {
    this.setState({ pattern: value })
  }
})

export default CampaignDropdownMenu
