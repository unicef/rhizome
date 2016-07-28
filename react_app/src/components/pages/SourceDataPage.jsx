import React, {Component} from 'react'
import SourceDataHeader from 'components/headers/SourceDataHeader'

import ResourceTable from 'components/molecules/ResourceTable'
import Placeholder from 'components/global/Placeholder'

class SourceDataPage extends Component {

  componentDidMount() {
    if (!this.props.source_docs.raw) {
      this.props.getAllSourceDocs()
    }
  }

  render = () => {

    const columnDefs = [
      {headerName: "ID", field: "id"},
      {headerName: "Document", field: "doc_title", editable: true},
    ]

    const source_data_table  = (
        this.props.source_docs.raw ? (
          <ResourceTable
            rowData={this.props.source_docs.raw}
            onRefreshData={() => this.props.getAllSourceDocs()}
            columnDefs={columnDefs}
            resourcePath='campaigns' />
          ) : <Placeholder />
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
