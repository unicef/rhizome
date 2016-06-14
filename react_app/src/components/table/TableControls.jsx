import React from 'react'

const TableControls = (props) => (
  <section>
    <input type="text" onChange={props.onQuickFilterText} placeholder="Type text to filter..."/>
    <button onClick={props.onRefreshData}>Refresh Data</button>
  </section>
)

export default TableControls

