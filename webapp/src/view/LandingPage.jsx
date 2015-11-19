import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import NavigationStore from 'stores/NavigationStore'
import PermissionStore from 'stores/PermissionStore'

// function _loadCampaigns (campaigns, offices) {
//   var recent = _(campaigns)
//     .each(function (campaign, i) {
//       campaign.office = offices[campaign.office_id]
//     })
//     .sortBy('start_date')
//     .reverse()
//     .value()

//   // jshint validthis: true
//   this.setState({ campaigns: recent })
// }

// function _loadDocuments (documents) {
//   var recent = _.take(documents, 5)

//   this.setState({ uploads: recent })
// }

// function _includeDashboard (dashboard, office) {
//   var slug = dashboard.slug
//   var offices = dashboard.offices

//   return (slug !== 'management-dashboard' &&
//     slug !== 'district' &&
//     (_.isEmpty(offices) || offices.indexOf(office) > -1)
//   )
// }

function _dashboardSelect (dashboards, campaign) {
  if (_.isEmpty(dashboards)) {
    return null
  }

  // FIXME: This should render a dropdown with all other available dashboards
  return (
    <a href={'/datapoints/' + dashboards[0].path}>
      {dashboards[0].title}
    </a>
  )
}

function _campaignRow (campaign, i) {
  var country
  var district
  var others = []

  _.each(campaign.dashboards, function (d) {
    switch (d.title) {
      case 'Management Dashboard':
        country = (<a href={'/datapoints/' + d.path}>Country</a>)
        break
      case 'District Dashboard':
        district = (<a href={'/datapoints/' + d.path}>District</a>)
        break
      default:
        if (!d.hasOwnProperty('default_office_id') || d.default_office_id === campaign.office_id) {
          others.push(d)
        }
        break
    }
  })

  var cls = i % 2 === 0 ? 'even' : 'odd'

  return (
    <tr className={cls} key={campaign.id}>
      <td>{campaign.title}</td>
      <td>{(parseFloat(campaign.management_dash_pct_complete * 100).toFixed(1)) + '% complete' }</td>
      <td>{country}</td>
      <td>{district}</td>
      <td>{_dashboardSelect(others)}</td>
    </tr>
  )
}

export default React.createClass({
  mixins: [
    Reflux.connect(NavigationStore)
  ],

  getInitialState: function () {
    return {
      visibleCampaigns: 6,
      visibleUploads: 5
    }
  },

  showAllCampaigns: function (e) {
    this.setState({ visibleCampaigns: Infinity })
    e.preventDefault()
  },

  render: function () {
    var campaigns
    if (_.isFinite(this.state.visibleCampaigns)) {
      campaigns = _(this.state.campaigns)
                      .take(this.state.visibleCampaigns)
                      .map(_campaignRow)
                      .value()
    } else {
      campaigns = _(this.state.campaigns).map(_campaignRow).value()
    }

    // data entry section, according to permissions
    if (PermissionStore.userHasPermission('upload_csv') || PermissionStore.userHasPermission('data_entry_form')) {
      var csv_upload_button = ''
      if (PermissionStore.userHasPermission('upload_csv')) {
        csv_upload_button = (
                <a className='small button' href='/source_data/file_upload'>
                  <i className='fa fa-upload'></i>&emsp;Upload data
                </a>
              )
      }

      var data_entry_button = ''
      if (PermissionStore.userHasPermission('data_entry_form')) {
        data_entry_button = (
                <a className='small button' href='/datapoints/entry'>
                  <i className='fa fa-table'></i>&emsp;Data Entry Form
                </a>
              )
      }

      var uploads = <tr><td>No uploads yet.</td></tr>
      var dataEntry = (
          <div className='row'>
            <div className='medium-4 columns'>
              <h2>Enter Data</h2>
              {data_entry_button}
              &emsp
              {csv_upload_button}
            </div>
            <div className='medium-8 columns'>
              <h2>Your Recent CSV Uploads</h2>
              <table>
                <tbody>{uploads}</tbody>
                <tfoot>
                  <tr>
                    <td className='more' colSpan='3'>
                      <a href='/source_data/document_index/'>see all uploads</a>
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        )
    }

    return (
      <div className='row'>
        <div className='medium-9 columns'>

          <div className='row'>
            <div className='small-12 columns'>

              <p className='pageWelcome'>
                Welcome to UNICEF&rsquo;s Polio Eradication data portal.
              </p>

              <h2>Recent Campaigns</h2>
              <table>
                <tbody>{campaigns}</tbody>
                <tfoot>
                  <tr>
                    <td className='more' colSpan='6'>
                      <a href='#' onClick={this.showAllCampaigns}>see all campaigns</a>
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>

          {dataEntry}

        </div>

        <div className='about medium-3 columns'>
          <img src='/static/img/RhizomeLogo.png' alt='Rhizome Logo' width='100%' />
          <h2>About</h2>
          <p>Rhizomes are underground systems that produce stems and roots of plants, allowing them to grow and thrive. They store nutrients that help plants survive and regenerate in the most challenging conditions. Ceaselessly establishing new connections between them, rhizomes constitute resilient, flexible and dynamic systems, rooted in their local environments and primed for long-term sustainability.</p>
          <p>Rhizome DB supports the polio programme’s critical need to adapt, evolve and reach the unreached. Rhizome DB connects staff, managers and policy makers to the evidence they need to drive local solutions. Maximize your impact to eradicate polio.</p>
        </div>

      </div>
    )
  }
})
