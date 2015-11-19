import _ from 'lodash'
import React from 'react'

import Chart from 'component/Chart.jsx'

var PieChartList = React.createClass({
  propTypes: {
    data: React.PropTypes.array.isRequired,
    keyPrefix: React.PropTypes.string.isRequired,
    options: React.PropTypes.object,
    name: React.PropTypes.func,
    emptyText: React.PropTypes.string,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      name: _.property('indicator.short_name'),
      emptyText: 'No data',
      loading: false
    }
  },

  render: function () {
    var loading = this.props.loading

    var pies = _.map(this.props.data, (d, i) => (
        <tr key={this.props.keyPrefix + '-' + i}>
          <td><Chart type='PieChart' data={d} options={this.props.options} loading={loading} /></td>
          <td>{this.props.name(d)}</td>
        </tr>
      )
    )

    if (_.isEmpty(pies)) {
      pies = (<tr><td>{this.props.emptyText}</td></tr>)
    }

    return (
      <table className='pie-charts'>{pies}</table>
    )
  }

})

export default PieChartList
