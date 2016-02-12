import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavigationStore from 'stores/NavigationStore'

import api from 'data/api'

// function _tableRow (row) {
//   let path = '/datapoints/' + _.kebabCase(row.title) + '/'
//   let editPath = '/datapoints/dashboards/edit/' + row.id + '/'
//   let editLink = <span>(<a href={editPath}>edit</a>)</span>
//   return (
//       <tr>
//         <td><a href={path}>{row.title}</a> {editLink}</td>
//         <td>{row.description}</td>
//         <td>{row.owner_username}</td>
//       </tr>
//     )
// }

var Charts = React.createClass({
  mixins: [
    Reflux.connect(NavigationStore, 'store')
  ],

  getInitialState () {
    return {
      customCharts: []
    }
  },

  getCustomCharts () {
    let self = this
    api.get_chart(null, null, {'cache-control': 'no-cache'}).then(response => {
      let customCharts = _(response.objects).sortBy('id').reverse().value()
      self.setState({customCharts: customCharts})
    })
  },

  componentWillMount () {
    this.getCustomCharts()
  },

  render () {
    let self = this
    let rows = self.state.customCharts
    if (_.isNull(rows)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (rows.length > 0) {
      rows = rows.map(_tableRow)
    } else {
      rows = <tr><td colSpan='3'>No custom charts created yet.</td></tr>
    }

    return (
      <div className='row'>
        <div className='medium-12 columns'>
          <h5 className='all-dashboard'>all custom charts</h5>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
      </div>
    )
  }

})

export default Charts
