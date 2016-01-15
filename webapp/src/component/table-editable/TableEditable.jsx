import React from 'react'

var TableEditale = React.createClass({
  propTypes: {
    data: React.PropTypes.object,
    loaded: React.PropTypes.bool,
    indicatorSet: React.PropTypes.object,
    locations: React.PropTypes.object,
    indicatorMap: React.PropTypes.object
  },

  render: function () {
    let initMessage = (<div className='empty'>Use the options above to load a data entry form.</div>)
    let emptyMessage = (<div className='empty'>Use the options above to load a data entry form.</div>)
    let tableContent = (
      <div>
        <h5>
        data
        </h5>
      </div>
    )
    let table = this.props.loaded
      ? this.props.indicatorSet.indicators.length > 0 ? tableContent : emptyMessage
      : initMessage
    return (
      <div>
        {table}
      </div>
    )
  }
})

export default TableEditale
