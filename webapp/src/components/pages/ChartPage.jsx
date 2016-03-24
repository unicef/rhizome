import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import Chart from 'components/molecules/charts/Chart'
import ExportPdf from 'components/molecules/ExportPdf'
import Placeholder from 'components/molecules/Placeholder'
import DatabrowserTable from 'components/molecules/DatabrowserTable'

import DropdownList from 'react-widgets/lib/DropdownList'
import RootStore from 'stores/RootStore'
import IndicatorStore from 'stores/IndicatorStore'
import LocationStore from 'stores/LocationStore'
import DataExplorerStore from 'stores/DataExplorerStore'
import DatapointStore from 'stores/DatapointStore'
import CampaignStore from 'stores/CampaignStore'
import DataExplorerActions from 'actions/DataExplorerActions'

var ChartPage = React.createClass({

  mixins: [
    Reflux.ListenerMixin,
    Reflux.connect(DataExplorerStore, 'chart'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(IndicatorStore, 'indicators'),
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(DatapointStore, 'datapoints')
  ],

  propTypes: {
    chart_id: React.PropTypes.number
  },

  componentWillMount () {
    Reflux.connect(LocationStore, 'chart')
    LocationStore.listen(this.getChart)
    IndicatorStore.listen(this.getChart)
  },

  getChart (locations, indicators) {
    if (this.state.locations.index && this.state.indicators.index) {
      DataExplorerActions.getChart(this.props.chart_id)
    }
  },

  render () {
    const chart = this.state.chart
    const campaigns = this.state.campaigns.raw || []
    let chart_component = <Placeholder height={200}/>

    if (!_.isEmpty(chart.data)) {
      chart_component = chart.def.type === 'RawData'
        ? <DatabrowserTable
            data={this.state.datapoints.raw}
            selected_locations={chart.def.selected_locations}
            selected_indicators={chart.def.selected_indicators}
          />
        : <Chart type={chart.def.type} data={chart.data} options={chart.def} />
    }

    return (
      <div>
        <form className='row no-print cd-titlebar'>
          <div className='medium-4 columns'>
            <a href={'/charts/' + this.props.chart_id + '/edit'} className='button small'>
              <i className='fa fa-pencil'></i> Edit Chart
            </a>
          </div>
          <div className='medium-4 columns'>
            <DropdownList
              data={campaigns}
              defaultValue={!_.isEmpty(campaigns) ? campaigns[0].id : null}
              textField='name'
              valueField='id'
              onChange={campaign => DataExplorerActions.setCampaignIds([campaign.id])}
            />
          </div>
          <div className='medium-4 columns'>
            <ExportPdf className='button small' />
          </div>
        </form>
        <div className='row layout-basic'>
          <div className='medium-12 columns text-center'>
            <h1>{ chart.def.title }</h1>
          </div>
          <div className='medium-12 columns'>
            { chart_component }
          </div>
        </div>
      </div>
    )
  }
})

export default ChartPage
