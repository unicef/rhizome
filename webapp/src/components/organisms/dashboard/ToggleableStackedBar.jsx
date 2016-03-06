import _ from 'lodash'
import d3 from 'd3'
import React from 'react'

import Chart from 'components/molecules/Chart.jsx'

var ToggleableStackedBar = React.createClass({
  propTypes: {
    data: React.PropTypes.array.isRequired,
    title: React.PropTypes.string.isRequired,

    options: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getInitialState: function () {
    return {
      offset: 'zero'
    }
  },

  render: function () {
    var name = _.kebabCase(this.props.title)
    var props = _.omit(this.props, 'title', 'options')
    var options = _.assign({}, this.props.options, {
      offset: this.state.offset,
      xFormat: d3.format(this.state.offset === 'expand' ? '%' : 'n')
    })

    return (
      <div>
        <h4>
          <a name={name}>{this.props.title}</a>&ensp;
          <div className='medium inline'>
            <label>
              <input
                type='radio'
                name={name + '-offset'}
                value='zero'
                checked={this.state.offset === 'zero'}
                onChange={this.onOffsetChange} />
              &ensp;count
            </label>
            <label>
              <input
                type='radio'
                name={name + '-offset'}
                value='expand'
                checked={this.state.offset === 'expand'}
                onChange={this.onOffsetChange} />
              &ensp;percentage
            </label>
          </div>
        </h4>
        <Chart type='BarChart' options={options} {...props} ref='chart' />
      </div>
    )
  },

  onOffsetChange: function (evt) {
    this.setState({ offset: evt.currentTarget.value })
    this.refs.chart.forceUpdate()
  }
})

export default ToggleableStackedBar
