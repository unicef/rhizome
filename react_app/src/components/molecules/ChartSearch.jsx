import React, {Component, PropTypes} from 'react'

import Select from 'components/select/Select'
import DropdownMenuItem from 'components/dropdown/DropdownMenuItem'

class ChartSearch extends Component {

  constructor (props) {
    super(props)
    this.state = {
      filtered_charts: [],
      resultsVisible: false,
      pattern: ''
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.charts) {
      this.setState({filtered_charts: nextProps.charts})
    }
  }

  _filterCharts = pattern => {
    if (pattern.length < 1) {
      this.setState({
        filtered_charts: this.props.charts,
        resultsVisible: false
      })
    }
    if (pattern.length > 1) {
      const charts = this.state.filtered_charts
      const filtered_charts = charts.filter(chart => new RegExp(pattern, 'i').test(chart.title))
      this.setState({
        filtered_charts: filtered_charts,
        resultsVisible: true
      })
    }
    this.setState({pattern: pattern})
  }

  _hideResults = event => {
    const linkClicked = event.relatedTarget ? event.relatedTarget.getAttribute('role') === 'menuitem' : false
    if (!linkClicked) {
      this.setState({
        filtered_charts: this.props.charts,
        pattern: '',
        resultsVisible: false
      })
    }
  }

  render () {
    const filtered_charts = _.sortBy(this.state.filtered_charts, 'title') || []
    const charts = filtered_charts ? filtered_charts.map(chart =>
      <li key={chart.id}>
        <a role='menuitem' onClick={this._clickLink} href={'/charts/' + chart.id}>{chart.title}</a>
      </li>
    ) : <li>Loading ...</li>

    return (
      <li className='header-search-field'>
        <input
          placeholder='Search Charts'
          onChange={e => this._filterCharts(e.target.value)}
          onFocus={() => this._filterCharts(this.state.pattern)}
          onBlur={this._hideResults}
          value={this.state.pattern}
        />
        <ul className='dashboard-menu' style={{display: this.state.resultsVisible ? 'block' : 'none' }}>
          { charts }
        </ul>
      </li>
    )
  }
}

export default ChartSearch
