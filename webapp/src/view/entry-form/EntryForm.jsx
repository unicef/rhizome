import React from 'react'
import Reflux from 'reflux'

import EntryFormStore from 'stores/EntryFormStore'
import EntryFormActions from 'actions/EntryFormActions'

let EntryForm = React.createClass({
  mixins: [Reflux.connect(EntryFormStore)],

  getInitialState: function () {
    return {
      indicatorSets: require('./structure/indicator_sets')
    }
  },

  _setIndicator: function (event) {
    EntryFormActions.setIndicator(event.target.value)
  },

  render () {
    let indicationOptions = (
      <select value={this.state.indicationSelected} onChange={this._setIndicator}>
        {this.state.indicatorSets.map(data => {
          return (<option value={data.id}>{data.title}</option>)
        })}
      </select>
    )

    let indicatorSet = (
      <div className='medium-2 columns'>
        <label htmlFor='sets'>Indicator Set</label>
        {indicationOptions}
      </div>
    )

    return (
      <div>
        <form className='inline'>
          <div className='row'>
            {indicatorSet}
          </div>
        </form>
      </div>
    )
  }
})

export default EntryForm
