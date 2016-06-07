import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import Placeholder from 'components/global/Placeholder'

class MultiChart extends Component {
  render = function () {
    const chart = this.props.chart
    return chart ?  (
      <article className='multi-chart medium-12 columns' style={chart.type === 'RawData' ? {overflowX: 'auto'} : null}>
        <section className='row'>
        </section>
      </article>
    ) : <Placeholder />
  }
}

export default MultiChart

