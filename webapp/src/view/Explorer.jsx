import React from 'react'
import DateRangePicker from 'component/DateTimePicker.jsx'

var Explorer = React.createClass({
  render: function () {
    return (
      <div>
        <div className='row'>
          <div className='small-12 columns'>
            <h1 style={{textAlign: 'left'}}>Raw Data</h1>
          </div>
        </div>

        <div className='row'>
          <div className='medium-3 columns'>
            <from className='inline'>
              <label>
                <div>Time Period</div>
                <DateRangePicker />
              </label>

              <div>
                <label htmlFor='locations'>locations</label>
                <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
              </div>

              <div>
                <label htmlFor='indicators'>Indicators</label>
                <div id='indicatorSelector'></div>
                <div id='indicatorList'></div>
              </div>

              <div>
                <a className='button success' role='button' v-on='click : refresh({ offset: 0 })' v-class='disabled: !hasSelection' style={{marginTop: '21px'}}>
                  <i className='fa fa-fw fa-refresh' v-class='fa-spin : table.loading'></i>&emsp;Load Data
                </a>
              </div>
            </from>
          </div>

          <div className='medium-9 columns'>
            <vue-table v-with='table'></vue-table>

            <div className='medium-6 columns'
              v-component='vue-pagination'
              v-with='offset: pagination.offset,
                      limit: pagination.limit,
                      total_count: pagination.total_count'></div>

            <div className='medium-4 columns' style={{textAlign: 'right'}}>
              <a role='button' className='button success' aria-label='Download All'
                v-class='disabled: !hasSelection'
                v-on='click: download()'>
                <i className='fa fa-fw fa-download'></i>&emsp;Download All
              </a>
            </div>
          </div>
        </div>
        <iframe width='0' height='0' src='{{ src }}' className='hidden'></iframe>
      </div>
    )
  }
})

export default Explorer
