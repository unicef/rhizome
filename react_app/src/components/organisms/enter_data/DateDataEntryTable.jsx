import _ from 'lodash'
import React, {Component} from 'react'
import IconButton from 'components/button/IconButton'
import ResourceTable from 'components/molecules/ResourceTable'
import moment from 'moment'
import format from 'utilities/format'
import {AgGridReact, reactCellRendererFactory} from 'ag-grid-react'
import IntegerCell from 'components/table/IntegerCell'
import DateCell from 'components/table/DateCell'
import BoolCell from 'components/table/BoolCell'
import PercentCell from 'components/table/PercentCell'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import RhizomeAPI from 'utilities/api'


class DataEntryTable extends Component {
  constructor (props) {
    super(props)
    this.state = {
      new_date: new Date(),
      new_value: null
    }
  }

  _addDatapoint = () => {
    const new_value = this.refs.new_value.value
    const datapoint = {
      indicator_id: this.props.selected_indicators[0].id,
      location_id: this.props.selected_locations[0].id,
      data_date: moment(this.state.new_date).format('YYYY-MM-DD'),
      value: new_value
    }
    RhizomeAPI.post('/date_datapoint/', datapoint).then(result => {
      console.log('result', result)
      if (result.status === 201) {
        this.props.addDatapoint(result.data)
      }
    })
    this.refs.new_value.value = null
  }

  _removeDatapoint = datapoint => {
    if (confirm('Are you sure you want to delete this datapoint?')) {
      console.log('datapoint', datapoint)
    }
     // this.props.removeDatapoint(result.data)
  }

  render = () => {
    const props = this.props
    const datapoints = props.datapoints.flattened
    const sorted_datapoints = _.sortBy(props.datapoints.flattened, 'data_date')
    const indicator = props.selected_indicators[0]
    const cell_style = {
      width: '25rem',
      textAlign: 'center'
    }
    const rows = sorted_datapoints.map(datapoint => {
      const cellParams = {
        datapoint: datapoint,
        updateDatapoint: props.updateDatapoint,
        removeDatapoint: props.removeDatapoint
      }
      let value_cell = <IntegerCell cellParams={cellParams} input_style={{textAlign: 'center'}}/>
      if (indicator.data_format === 'bool') {
        value_cell = <BoolCell cellParams={cellParams}/>
      } else if (indicator.data_format === 'pct') {
        value_cell = <PercentCell cellParams={cellParams}/>
      }
      return (
        <tr>
          <td>
            <IconButton onClick={() => this._removeDatapoint(datapoint)} icon='fa-times-circle' text='Remove datapoint' />
          </td>
          <td style={cell_style}>{moment(datapoint.data_date).format('YYYY-MM-DD')}</td>
          <td style={cell_style}>{value_cell}</td>
        </tr>
      )
    })

    const new_datapoint_row = (
      <tr>
        <td></td>
        <td style={{width: '30rem'}}>
          <DateTimePicker
            style={{left: '.65rem'}}
            value={this.state.new_date}
            time={false}
            format={'YYYY-MM-DD'}
            onChange={date => this.setState({new_date: date})}
          />
        </td>
        <td>
          <input className='text-center' type='text' ref='new_value' defaultValue={this.state.new_value} />
        </td>
        <td style={{width: '20rem'}}>
          <button className='small button' onClick={this._addDatapoint}>Add Datapoint</button>
        </td>
      </tr>
    )

    return (
      <table style={{width: '30rem'}}>
        <thead>
          <tr>
            <th></th>
            <th style={cell_style}>Date</th>
            <th style={cell_style}>Value</th>
          </tr>
        </thead>
        <tbody>
          {rows}
          {new_datapoint_row}
        </tbody>
      </table>
    )
  }
}

export default DataEntryTable
