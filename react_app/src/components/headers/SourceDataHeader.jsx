import React from 'react'

const SourceDataHeader = props => {
  return (
    <header className='row page-header'>
      <div className='medium-12 columns medium-text-left small-text-center'>
        <h1>Source Data</h1>
      </div>
      <div className='medium-12 columns dashboard-actions'>
        { /* Any dropdown filters you might want go here */ }
      </div>
    </header>
  )
}

export default SourceDataHeader
