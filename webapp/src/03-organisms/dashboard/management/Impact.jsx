import React from 'react'

import PolioCasesYTD from '03-organisms/dashboard/management/PolioCasesYTD.jsx'
import ImmunityGap from '03-organisms/dashboard/management/ImmunityGap.jsx'

var Impact = React.createClass({
  propTypes: {
    campaign: React.PropTypes.object,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      loading: false
    }
  },

  render: function () {
    var data = this.props.data
    var campaign = this.props.campaign
    var loading = this.props.loading

    return (
      <div className='medium-2 columns'>
        <h3>Impact</h3>
        <PolioCasesYTD data={data.polioCasesYtd} campaign={campaign} loading={loading} />
        <ImmunityGap data={data.underImmunizedChildren} campaign={campaign} loading={loading} />
      </div>
    )
  }
})

export default Impact
