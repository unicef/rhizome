import _ from 'lodash'
import React, { PropTypes, Component } from 'react'
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react'
import { Link } from 'react-router'
import TableControls from 'components/table/TableControls'

export default class ResourceTable extends Component {

  constructor() {
    super()
    this.state = {
      quickFilterText: null,
      showToolPanel: false
    }
  }

  static propTypes = {
    resourcePath: PropTypes.string.isRequired,
    rowData: PropTypes.array.isRequired,
    columnDefs: PropTypes.array.isRequired
  }

  icons: {
    columnRemoveFromGroup: '<i class="fa fa-remove"/>',
    filter: '<i class="fa fa-filter"/>',
    sortAscending: '<i class="fa fa-long-arrow-down"/>',
    sortDescending: '<i class="fa fa-long-arrow-up"/>',
    groupExpanded: '<i class="fa fa-minus-square-o"/>',
    groupContracted: '<i class="fa fa-plus-square-o"/>',
    columnGroupOpened: '<i class="fa fa-minus-square-o"/>',
    columnGroupClosed: '<i class="fa fa-plus-square-o"/>'
  }

  onGridReady = (params) => {
    this.api = params.api
    this.columnApi = params.columnApi
  }

  onToggleToolPanel = (event) => {
    this.setState({showToolPanel: event.target.checked})
  }

  onQuickFilterText = (event) => {
    this.setState({quickFilterText: event.target.value})
  }

  renderControlCell = (cell) => {
    const item = cell.params.data
    return (
      <span>
        <a href={this.props.resourcePath + '/' + item.id}>Show</a> &nbsp;
        <a href={this.props.resourcePath + '/' + item.id + '/edit'}>Edit</a>
      </span>
    )
  }

  componentWillMount = () => {
    this.columnDefs = this.props.columnDefs
  }

  render = () => {
    this.columnDefs.push({headerName: 'Edit', cellRenderer: reactCellRendererFactory(this.renderControlCell)})
    return (
      <div style={{width: '100vw'}}>
        <div style={{padding: '4px'}}>
          <TableControls
            onQuickFilterText={this.onQuickFilterText}
            onToggleToolPanel={this.onToggleToolPanel}
            onRefreshData={this.props.onRefreshData} />
          <div style={{height: 400}} className="ag-fresh">
            <AgGridReact
              gridOptions={this.gridOptions}
              onGridReady={this.onReady}
              showToolPanel={this.state.showToolPanel}
              quickFilterText={this.state.quickFilterText}
              icons={this.icons}
              columnDefs={this.props.columnDefs}
              rowData={this.props.rowData}
              rowSelection="multiple"
              enableColResize="true"
              enableSorting="true"
              enableFilter="true"
              groupHeaders="true"
              suppressCellSelection="true"
              rowHeight="50"
              debug="false"/>
          </div>
        </div>
      </div>
    )
  }

}
