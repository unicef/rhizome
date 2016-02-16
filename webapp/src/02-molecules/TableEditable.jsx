import React from 'react'
import Reflux from 'reflux'
import _ from 'lodash'
import d3 from 'd3'

// import Cell from '02-molecules/TableEditableCell.jsx'
import DatabrowserTable from '02-molecules/DatabrowserTable'
import TableEditableStore from 'stores/TableEditableStore'
import TableEditableActions from 'actions/TableEditableActions'

let TableEditable = React.createClass({
  mixins: [Reflux.connect(TableEditableStore)],

  propTypes: {
    data: React.PropTypes.array,
    loaded: React.PropTypes.bool,
    formDefinition: React.PropTypes.object,
    indicatorMap: React.PropTypes.object,
    locationMap: React.PropTypes.object,
    locations: React.PropTypes.array,
    campaignId: React.PropTypes.string,
    indicators: React.PropTypes.array,
    locationSelected: React.PropTypes.array,
    indicatorSelected: React.PropTypes.array
  },

  componentWillReceiveProps: function (nextProps) {
    if (!this.props.loaded && nextProps.loaded) {
      TableEditableActions.init(nextProps.data, nextProps.formDefinition,
        nextProps.indicatorMap, nextProps.locationMap,
        nextProps.locations, nextProps.campaignId)
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return !_.isEqual(nextProps.loaded, this.props.loaded) ||
      !_.isEqual(this.state.processed, nextState.processed) ||
      nextState.total !== this.state.total
  },

  completionClass: function (v) {
    if (v === 0) {
      return 'statusText-bad'
    } else if (v === 1) {
      return 'statusText-good'
    } else if (v > 0 && v < 1) {
      return 'statusText-okay'
    }
    return null
  },

  percent: function (v) {
    const percent = d3.format('%')
    return percent(v)
  },

  _buildTable: function () {
    let contentTitle = (
      <div>
        <h5> Data Entry Form </h5>
      </div>
    )

    // let tableHeader = ''
    // let tableBody = ''

    // if (this.state.table.rows.length > 0) {
    //   tableHeader = this.state.table.columns.map((column, index) => {
    //     // let isShowLabel = column.type !== 'value'
    //     // let className = (isShowLabel ? 'col' : this.completionClass(this.state.byColumn[index].complete / this.state.byColumn[index].total)) + ' completionStatus'
    //     // let headerContent = isShowLabel ? '' : this.state.byColumn[index].complete + ' / ' + this.state.byColumn[index].total
    //     return (
    //       <th className={column.headerClasses}>
    //         <div className='th-inner'>
    //           {column.header}
    //         </div>
    //       </th>
    //     )
    //   })
    // }

    // tableBody = this.state.table.rows.map((row, index) => {
    //   let cellItems = row.map(item => <Cell item={item} />)
    //   return (
    //     <tr>
    //       {cellItems}
    //     </tr>
    //   )
    // })

    let locationData = []
    let indicatorData = []
    let tableContent =  (
      <div>
        {contentTitle}
      <DatabrowserTable
        data={this.props.data}
        selected_locations={this.props.locationSelected}
        selected_indicators={this.props.indicatorSelected}
    />
    </div>
)

    // let tableContent = (
    //   <div>
    //     {contentTitle}
    //     <div className='fixed-table-container'>
    //       <div className='fixed-table-container-inner'>
    //         <table>
    //           <thead>
    //             <tr>
    //               <th></th>
    //               {tableHeader}
    //             </tr>
    //           </thead>
    //           <tbody>
    //           {tableBody}
    //           </tbody>
    //         </table>
    //       </div>
    //     </div>
    //   </div>
    // )

    return tableContent
  },

  render: function () {
    if (!this.props.loaded || !this.state.processed) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else if (this.props.formDefinition.indicators.length < 1) {
      return (<div className='empty'>Use the options above to load a data entry form.</div>)
    } else {
      return this._buildTable()
    }
  }
})

export default TableEditable