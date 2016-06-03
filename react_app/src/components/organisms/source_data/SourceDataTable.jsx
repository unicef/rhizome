import React, { PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';

const SourceDataList = ({ source_data, columnDefs }) => (
  <div className="ag-fresh" style={{height: '10rem'}}>
    <AgGridReact
        columnDefs={columnDefs}
        rowData={source_data} />
  </div>
)

SourceDataList.defaultProps = {
  source_data: [],
  columnDefs: [
    {headerName: "ID", field: "id"},
    {headerName: "Title", field: "title"},
  ]
}

SourceDataList.propTypes = {
  source_data: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired
  }).isRequired)

}

export default SourceDataList