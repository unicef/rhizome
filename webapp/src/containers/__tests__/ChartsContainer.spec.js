import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import _ from 'lodash'
import orderBy from 'lodash.orderby'
import uuid from 'uuid'
import sinon from 'sinon'

import ChartsContainer from '../ChartsContainer'
import ChartStore from '../../stores/ChartStore'
import ChartActions from '../../actions/ChartActions'

describe ('ChartsContainer', () => {
  let mockChartsContainer
  beforeEach(() => {
    mockChartsContainer = new ChartsContainer()
  })
  it ('exists', () => {
    expect (ChartsContainer).to.exist
  })
  describe ('#getInitialState()', () => {
    it ('has correct properties', () => {
      //remove 'charts' key if reflux is refactored out
      expect (mockChartsContainer.getInitialState()).to.have.all.keys('charts', 'sort_column', 'sort_desc')
    })
  })
  describe ('#sortCharts()', () => {
    it ('exists with 1 argument required', () => {
      expect (mockChartsContainer.sortCharts).to.exist.and.have.lengthOf(1)
    })
    context ('if sort_column is equal to state.sort_column', () => {
      it ('sets state of sort_desc to opposite value of itself', () => {
        mockChartsContainer.state.sort_column = 'title'
        const expected_sort_desc = mockChartsContainer.state.sort_desc
        const spy = sinon.spy(ChartsContainer.prototype, 'setState')
        const sort_column = 'title'
        mockChartsContainer.sortCharts(sort_column)
        spy.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith({ sort_desc: !expected_sort_desc })).to.be.true
      })
    })
    context ('if sort_column is not equal to state.sort_column', () => {
      it ('sets state of sort_column to value of sort_column', () => {
        const expected_sort_desc = mockChartsContainer.state.sort_desc
        const spy = sinon.spy(ChartsContainer.prototype, 'setState')
        const sort_column = 'title'
        mockChartsContainer.sortCharts(sort_column)
        spy.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith({ sort_column: sort_column })).to.be.true
      })
    })
  })
  describe ('#duplicateChart()', () => {
    it ('exists with 1 required argument', () => {
      expect (mockChartsContainer.duplicateChart).to.exist.and.have.lengthOf(1)
    })
    it.skip ('calls ChartActions.postChart() with correct argument', () => {
      const spy = sinon.spy(ChartStore, 'onPostChart')
      //come back to this once charts index is working again
      // chart variable needs real data object from application
      // move to chartcontainertest
      const chart = {
        title: 'foo',
        chart_json: {
          type: 'TableChart',
          start_date: 'January',
          end_date: 'December',
          campaign_ids: [ { id: 1, name: 'bar' }],
          location_ids: [ { id: 1, name: 'foo' }],
          indicator_ids: [{ id: 1, name: 'fooBar' }],
          indicator_colors: ['red', 'yellow', 'green'],
          groupBy: '',
          groupByTime: true,
          location_depth: 2
        }
      }
      const chart_def = chart.chart_json
      const post_chart_arg = {
        title: chart.title + ' Copy',
        uuid: uuid.v4(),
        chart_json: JSON.stringify({
          type: chart_def.type,
          start_date: chart_def.state_date,
          end_date: chart_def.end_date,
          campaign_ids: chart_def.campaign_ids,
          location_ids: chart_def.location_ids,
          indicator_ids: chart_def.indicator_ids,
          indicator_colors: chart_def.indicator_colors,
          groupBy: chart_def.groupBy,
          groupByTime: chart_def.groupByTime,
          location_depth: chart_def.location_depth
        })
      }
      mockChartsContainer.duplicateChart(chart)
      spy.restore()
      expect (spy.calledOnce).to.be.true
      expect (spy.calledWitch(post_chart_arg)).to.be.true
    })
  })
  describe ('#deleteChart()', () => {
    it ('exists with correct arguments', () => {
      expect (mockChartsContainer.deleteChart).to.exist.and.to.have.lengthOf(1)
    })
    context.skip ('if confirmed true', () =>{
      it ('calls ChartActions.deleteChart', () => {
        const id = 1
        const spy = sinon.spy(ChartStore, 'onDeleteChart')
        const stub = sinon.stub(window, 'confirm', () => true)
        mockChartsContainer.deleteChart(id)
        //not able to restore this method. react? reflux? not sure
        // confirm not showing up as available method to wrap. check global.
        spy.restore()
        stub.restore()
        expect (spy.calledOnce).to.be.true
        expect (spy.calledWith(id)).to.be.true
      })
    })
    context.skip ('if confirmed false', () =>{
      it ('calls ChartActions.deleteChart', () => {
        const id = 1
        const spy = sinon.spy(ChartStore, 'onDeleteChart')
        const stub = sinon.stub(window, 'confirm', () => false)
        mockChartsContainer.deleteChart(id)
        spy.restore()
        stub.restore()
        expect (spy.called).to.be.false
        expect (stub.calledOnce).to.be.true
      })
    })
  })
  describe ('#render()', () => {
    it ('exists', () => {
      expect (mockChartsContainer.render).to.exist
    })
    context ('if list of dashboards exists', () => {
      it ('renders correct jsx', () => {
        const state = ChartsContainerTest.getState()
        let actualComponent = shallow(<ChartsContainer />)
        actualComponent.setState(state)
        actualComponent = actualComponent.debug()
        const expectedComponent = shallow(ChartsContainerTest.getComponent(state)).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
    context ('if dashboard list is null', () => {
      it ('renders `Loading` message', () => {
        let actualComponent = shallow(<ChartsContainer />)
        actualComponent.setState({ charts: { list: null } })
        actualComponent = actualComponent.debug()
        const expectedComponent = shallow(ChartsContainerTest.getComponent()).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
  })
})

class ChartsContainerTest {
  static getState() {
    return (
      {
        charts: {
          list: [{
            id: 1,
            title: 'PCA # Children Missed',
            chart_json: { type: 'TableChart', start_date: 'January 01, 2016', end_date: 'January 31, 2016' }
          }]
        },
        sort_column: null,
        sort_desc: true
      }
    )
  }
  static getEmptyState() {
    return (
      {
        charts: {
          list: null
        },
        sort_column: null,
        sort_desc: true
      }
    )
  }
  static sortCharts (sort_column) {
    const state = this.getState()
    if (sort_column === state.sort_column) {
      this.setState({sort_desc: !state.sort_desc})
    } else {
      this.setState({sort_column: sort_column})
    }
  }
  static duplicateChart(id) {
    const chart_def = chart.chart_json
    ChartActions.postChart({
      title: chart.title + ' Copy',
      uuid: uuid.v4(),
      chart_json: JSON.stringify({
        type: chart_def.type,
        start_date: chart_def.start_date,
        end_date: chart_def.end_date,
        campaign_ids: chart_def.campaign_ids,
        location_ids: chart_def.location_ids,
        indicator_ids: chart_def.indicator_ids,
        indicator_colors: chart_def.indicator_colors,
        groupBy: chart_def.groupBy,
        groupByTime: chart_def.groupByTime,
        location_depth: chart_def.location_depth
      })
    })
  }
  static deleteChart(id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      ChartActions.deleteChart(id)
    }
  }
  static getComponent(state = this.getEmptyState()) {
    let rows = (
      <tr>
        <td colSpan='3'>
          No charts created yet.{' '}
          <a href='/charts/create' className='underlined'>Create your first chart</a>
        </td>
      </tr>
    )
    if (_.isNull(state.charts.list)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (state.charts.list.length > 0) {
      const order = state.sort_desc ? 'desc' : 'asc'
      const chart_list = orderBy(state.charts.list, state.sort_column, order)
      rows = chart_list.map(chart => {
        return (
          <tr>
            <td>
              <a href={'/charts/' + chart.id + '/'}>
              <strong>{chart.title}</strong> </a>
            </td>
            <td>{chart.chart_json.type}</td>
            <td>{chart.chart_json.start_date}</td>
            <td>{chart.chart_json.end_date}</td>
            <td>
              <a onClick={() => this.duplicateChart(chart)}>
                <i className='fa fa-clone'></i> Duplicate
              </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a onClick={() => this.deleteChart(chart.id) }>
                <i className='fa fa-trash'></i> Delete
              </a>
            </td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-12 medium-centered columns'>
          <h2 className='all-dashboard left'>All Saved Charts</h2>
          <a href='/charts/create' className='button success right'>Create New Chart</a>
          <table>
            <thead>
              <tr>
                <th><a onClick={this.sortCharts.bind(this, 'title')}>Title</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'chart')}>Chart Type</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'start')}>Start Date</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'end')}>End Date</a></th>
                <th><a onClick={this.sortCharts.bind(this, '&nbsp')}>&nbsp;</a></th>
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
}
