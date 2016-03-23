// import React, {PropTypes} from 'react'
// import Reflux from 'reflux'
// import moment from 'moment'
// import api from 'data/api'

// import ChartInit from 'components/molecules/charts_d3/ChartInit'
// import Chart from 'components/molecules/Chart'
// import DownloadButton from 'components/molecules/DownloadButton'
// import DatabrowserTable from 'components/molecules/DatabrowserTable'

// import ChartDataSelect from 'components/organisms/data-explorer/ChartDataSelect'
// import ChartProperties from 'components/organisms/data-explorer/ChartProperties'
// import PreviewScreen from 'components/organisms/data-explorer/PreviewScreen'

// import DataExplorerActions from 'actions/DataExplorerActions'
// import ChartActions from 'actions/ChartActions'
// import DataExplorerStore from 'stores/DataExplorerStore'
// import LocationStore from 'stores/LocationStore'
// import IndicatorStore from 'stores/IndicatorStore'
// import OfficeStore from 'stores/OfficeStore'
// import CampaignStore from 'stores/CampaignStore'
// import ChartStore from 'stores/ChartStore'
// import ChartAPI from 'data/requests/ChartAPI'


// const defaultChartDef = {
//   type: 'RawData',
//   indicator_ids: [28,34],
//   location_ids: [1],
//   countries: [],
//   groupBy: 'indicator',
//   timeRange: null,
//   x: 0,
//   xFormat: ',.0f',
//   y: 0,
//   yFormat: ',.0f',
//   z: 0
// }

// let DataExplorer = React.createClass({
//   propTypes: {
//     chartDef: PropTypes.object,
//     chart_id: PropTypes.number
//   },

//   mixins: [
//     Reflux.connect(DataExplorerStore),
//     Reflux.connect(ChartStore, 'ThisChart'),
//     Reflux.connect(LocationStore, 'root-locations'),
//     Reflux.connect(IndicatorStore, 'root-indicators'),
//     Reflux.connect(OfficeStore, 'root-offices'),
//     Reflux.connect(CampaignStore, 'root-campaigns')
//   ],

//   componentDidMount () {
//     if (this.props.chart_id) {
//       ChartAPI.getChart(this.props.chart_id).then(response => DataExplorerActions.initialize(response))
//     } else {
//       this.chartDef = this.props.chartDef || defaultChartDef
//       DataExplorerActions.initialize(this.chartDef)
//     }
//   },

//   componentWillReceiveProps () {
//     DataExplorerActions.clear()
//   },

//   saveChart () {
//     DataExplorerActions.saveChart(data => {
//       var chart = {
//         id: this.props.chart_id,
//         title: this.state.title,
//         chart_json: JSON.stringify(this.state.chart.def)
//       }
//       api.post_chart(chart).then(res => {
//         window.location.replace('/charts/' + res.objects.id)
//       }, res => {
//         console.log('update chart error,', res)
//       })
//     })
//   },

//   _downloadRawData: function () {
//     let locations = this.state.locations.selected.map(location => location.id)
//     let indicators = this.state.indicators.selected.map(indicator => indicator.id)
//     let query = { 'format': 'csv' }

//     if (indicators.length > 0) query.indicator__in = indicators
//     if (locations.length > 0) query.location_id__in = locations
//     if (this.state.chart.def.startDate) query.campaign_start = moment(this.state.chart.def.startDate).format('YYYY-M-D')
//     if (this.state.chart.def.endDate) query.campaign_end = moment(this.state.chart.def.endDate).format('YYYY-M-D')

//     return api.datapoints.toString(query)
//   },

//   render: function () {
//     const chartDef = this.state.chart.def
//     const start_date = chartDef ? moment(chartDef.startDate, 'YYYY-MM-DD').toDate() : moment()
//     const end_date = chartDef ? moment(chartDef.endDate, 'YYYY-MM-DD').toDate() : moment()

//     if (!chartDef.type) {
//       return null
//     }

//     const download_button = <DownloadButton onClick={this._downloadRawData} enable={this.state.rawData} text='Download Raw Data' working='Downloading' cookieName='dataBrowserCsvDownload'/>

//     const data = this.state.ThisChart.chart_data
//     if (data) {
//       const features = features // To do
//       const results = ChartInit.chartInit(
//         this.state.chart.def,
//         data,
//         this.state.locations.selected,
//         this.state.campaigns.selected,
//         this.state.locations.index,
//         this.state.campaigns.index,
//         this.state.indicators.index,
//         features
//       )
//     }

//     const chart = (
//       <Chart
//         id='custom-chart'
//         type={chartDef.type}
//         data={this.state.chart.data}
//         options={this.state.chart.options}
//         campaigns={this.state.campaigns.filtered}
//         defaultCampaign={this.state.campaigns.selected}
//       />
//     )

//     const location_options = [
//       { title: 'by Status', value: this.state.location_lpd_statuses },
//       { title: 'by Country', value: this.state.locations.filtered }
//     ]

//     return (
//       <section className='data-explorer'>
//         <h1 className='medium-12 columns text-center'>Explore Data</h1>
//         <div className='row'>
//           <ChartDataSelect
//             start_date={start_date}
//             end_date={end_date}
//             all_indicators={this.state.indicators.list}
//             all_locations={location_options}
//             selected_indicators={this.state.indicators.selected}
//             selected_locations={this.state.locations.selected}
//             addLocation={DataExplorerActions.addLocation}
//             removeLocation={DataExplorerActions.removeLocation}
//             addIndicator={DataExplorerActions.addIndicator}
//             reorderIndicator={DataExplorerActions.reorderIndicator}
//             removeIndicator={DataExplorerActions.removeIndicator}
//             clearSelectedIndicators={DataExplorerActions.clearSelectedIndicators}
//             clearSelectedLocations={DataExplorerActions.clearSelectedLocations}
//             setDateRange={DataExplorerActions.updateDateRangePicker}
//           />
//           <div className='medium-9 columns'>
//             {
//               chartDef.type === 'RawData'
//               ? <DatabrowserTable
//                   data={this.state.rawData}
//                   selected_locations={this.state.locations.selected}
//                   selected_indicators={this.state.indicators.selected}
//                 />
//               : <PreviewScreen isLoading={this.state.isLoading}>
//                   {this.state.canDisplayChart ? chart : (<div className='empty'>No Data</div>) }
//                 </PreviewScreen>
//             }
//           </div>
//         </div>
//         <ChartProperties
//           selected_chart_type={this.state.chart.def.type}
//           selected_palette={this.state.chart.def.palette}
//           chart_title={this.state.title}
//           selectChartType={DataExplorerActions.changeChart}
//           selectPalette={DataExplorerActions.changePalette}
//           saveTitle={DataExplorerActions.editTitle}
//           saveChart={this.saveChart}
//           chartIsReady={!this.state.canDisplayChart}
//         />
//       </section>
//     )
//   }
// })

// export default DataExplorer