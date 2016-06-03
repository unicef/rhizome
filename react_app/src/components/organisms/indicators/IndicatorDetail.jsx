import React, { PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/molecules/Placeholder'

const IndicatorDetail = ({ indicator }) => {
  return indicator ? (
    <div>
      <h2>Indicator ID: {indicator.id}</h2>
      <p>There should be an indicator id</p>
      <form>
        <label>
          Name
          <input type='text' value={indicator.name}/>
        </label>
        <label>
          Short Name
          <input type='text' value={indicator.short_name}/>
        </label>
        <label>
          Source Name
          <input type='text' value={indicator.source_name}/>
        </label>
        <label>
          Low Bound
          <input type='text' value={indicator.low_bound}/>
        </label>
        <label>
          High Bound
          <input type='text' value={indicator.high_bound}/>
        </label>
      </form>
    </div>
  ) : <Placeholder />
}

IndicatorDetail.defaultProps = {
  indicator: null,
  columnDefs: [
    {headerName: "ID", field: "id"},
    {headerName: "Title", field: "title"},
  ]
}

IndicatorDetail.propTypes = {
  indicator: PropTypes.object
}

export default IndicatorDetail