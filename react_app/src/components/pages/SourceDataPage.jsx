import React from 'react'
import SourceDataHeader from 'components/headers/SourceDataHeader'

const SourceDataPage = props => {
	const source_data_table = (
		<div>
			{ /* Main content for source data */ }
		</div>
	)

  return (
    <div className='data-entry-page'>
      <SourceDataHeader {...props} />
      <div className='row'>
        <div className='medium-12 columns'>
        	{ source_data_table }
        </div>
      </div>
    </div>
  )
}

export default SourceDataPage