import _ from 'lodash'
import React from 'react'

import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import ChartFactory from 'components/molecules/charts_d3/ChartFactory'

function isEmpty (type, data, options) {
  // Bullet charts get special treatment because they're considered empty if
  // they have no current value, regardless of whether they have historical data
  // for the comparative measure
  if (type !== 'BulletChart') {
    return _.isEmpty(data)
  }

  var getValue = _.get(options, 'value', _.identity)
  // Map the value accessor across the data because data is always passed as
  // multiple series (an array of arrays), even if there is only one series (as
  // will typically be the case for bullet charts).
  return _(data).map(getValue).all(_.negate(_.isFinite))
}

export default React.createClass({
  propTypes: {
    data: React.PropTypes.array.isRequired,
    type: React.PropTypes.string.isRequired,
    id: React.PropTypes.string,
    loading: React.PropTypes.bool,
    options: React.PropTypes.object,
    isBulletChart: React.PropTypes.bool,
    campaigns: React.PropTypes.array,
    style: React.PropTypes.object,
    defaultCampaign: React.PropTypes.object
  },

  getInitialState: function () {
    return {
      campaign_id: null
    }
  },

  getDefaultProps: function () {
    return {
      loading: false
    }
  },

  setCampaign: function (id) {
    this.setState({campaign_id: id})
  },

  filterData: function () {
    if (this.props.type === 'TableChart' && this.props.options.campaign_ids) {
      return this.props.data.filter(d => d.campaign_id === this.props.options.campaign_ids[0])
    } else {
      return this.props.data
    }
  },

  componentDidMount: function () {
    var chartData = this.filterData()
    const container = React.findDOMNode(this)
    this._chart = ChartFactory(
      this.props.type,
      container,
      chartData,
      this.props.options)
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return ( nextProps.data !== this.props.data ||
       nextProps.loading !== this.props.loading ||
       this.state.campaign_id !== nextState.campaign_id
     )
  },

  componentWillReceiveProps: function (nextProps) {
    if (nextProps.type !== this.props.type) {
      React.findDOMNode(this).innerHTML = ''
      this._chart = ChartFactory( nextProps.type, React.findDOMNode(this), nextProps.data, nextProps.options)
    }
  },

  componentDidUpdate: function () {
    var chartData = this.filterData()
    const container = React.findDOMNode(this)
    this._chart.update(chartData, this.props.options, container)
  },

  render: function () {
    let overlay
    let message
    let campaignDropdown
    if (this.props.loading || isEmpty(this.props.type, this.props.data, this.props.options)) {
      const position = { top: 19, right: 0, bottom: 0,left: 0, zIndex: 9997 }

      if (this.props.loading) {
        message = <span><i className='fa fa-spinner fa-spin'></i>&nbsp;Loading</span>
      } else {
        message = <span className='empty'>No data</span>
      }

      if (this.props.isBulletChart) {
        overlay = (
          <div style={position} className='overlay chart__bullet--overlay'>
            <div className='chart__bullet--noData'>{message}</div>
          </div>
        )
      } else {
        overlay = (
          <div style={position} className='overlay'>
            <div>{message}</div>
          </div>
        )
      }
    }

    if (this.props.campaigns) {
      let campaignDropdownTitle = this.props.defaultCampaign.name
      let campaignIndex = _.indexBy(this.props.campaigns, 'id')
      if (this.state.campaign_id) {
        campaignDropdownTitle = campaignIndex[this.state.campaign_id].name
      }
      campaignDropdown = (
        <DropdownMenu
          items={this.props.campaigns}
          sendValue={this.setCampaign}
          item_plural_name='Campaigns'
          text={campaignDropdownTitle}
          title_field='name'
          value_field='id'
          uniqueOnly/>
      )
    }

    return (
      <div id={this.props.id} className={'chart ' + _.kebabCase(this.props.type)} style={this.props.style}>
        {campaignDropdown}
        {overlay}
      </div>
    )
  }
})
