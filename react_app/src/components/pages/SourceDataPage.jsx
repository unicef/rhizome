import React, {Component} from 'react'
import SourceDataHeader from 'components/headers/SourceDataHeader'

class SourceDataPage extends Component {

  componentDidMount() {
    if (!this.props.source_docs.raw) {
      this.props.getAllSourceDocs()
    }
  }

  render = () => {
    console.log('locations', this.props.locations)
    console.log('campaigns', this.props.campaigns)
    console.log('indicators', this.props.indicators)

  	const source_data_table = (
  		<div>
  			{ /* Main content for source data */ }
  		</div>
  	)

    return (
      <div className='data-entry-page'>
        <SourceDataHeader />
        <div className='row'>
          <div className='medium-12 columns'>
          	{ source_data_table }
          </div>
        </div>
      </div>
    )

  }
}

export default SourceDataPage