import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import _ from 'lodash'
// import DashboardContainer from '../DashboardContainer'
import sinon from 'sinon'

describe.skip ('DashboardContainer', () => {
  let mockDashboardContainer
  beforeEach(() => {
    mockDashboardContainer = new DashboardContainer()
  })
  it ('exists', () => {
    expect (DashboardContainer).to.exist
  })
  describe ('.propTypes', () => {
    it ('has correct properties', () => {
      expect (DashboardContainer.propTypes).to.have.all.keys('dashboard_id')
    })
  })
  describe.skip ('#deleteDashboard()', () => {
    it ('exists with correct arguments', () => {
      expect (mockDashboardContainer.deleteDashboard).to.exist.and.to.have.lengthOf(1)
    })
  })
  describe.skip ('#render()', () => {
    it ('exists', () => {
      expect (mockDashboardContainer.render).to.exist
    })
    context ('if list of dashboards exists', () => {
      it ('renders correct jsx', () => {
        const state = DashboardContainerTest.getState()
        let actualComponent = shallow(<DashboardContainer />)
        actualComponent.instance().state.dashboards.raw = state.dashboards.raw
        actualComponent = actualComponent.debug()
        const expectedComponent = shallow(DashboardContainerTest.getComponent(state)).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
    context ('if dashboard list is null', () => {
      it ('renders `Loading` message', () => {
        let actualComponent = shallow(<DashboardContainer {...{ dashboards: { raw: null } }}/>)
        actualComponent = actualComponent.debug()
        const expectedComponent = shallow(DashboardContainerTest.getComponent()).debug()
        expect (actualComponent).to.equal(expectedComponent)
      })
    })
  })
  describe.skip ('events', () => {
    describe ('when onClick is clicked with `accept` response', () => {
      it.skip ('`DashboardContainerActions.deleteDashboard(id)` is called', () =>{
        //refactor if/when redux
        //circle back to update window logic. breaks on CI.
        const spy = sinon.spy(DashboardContainerActions, 'deleteDashboard')
        const stub = sinon.stub(window, 'confirm', () => true)
        const id = DashboardContainerTest.getState().dashboards.raw.id
        mockDashboardContainer.deleteDashboard(id)
        window.confirm.restore()
        DashboardContainerActions.deleteDashboard.restore()
        expect(stub.calledOnce).to.be.true
        expect(stub.calledWitch('Are you sure you want to delete this chart?')).to.be.true
        expect(spy.calledOnce).to.be.true
        expect(spy.calledWith(id)).to.be.true
      })
    })
    describe ('when onClick is clicked with `accept` response', () => {
      it.skip ('`DashboardContainerActions.deleteDashboard(id)` is called', () =>{
        //refactor if/when redux
        //circle back to update window logic. breaks on CI.
        const spy = sinon.spy(DashboardContainerActions, 'deleteDashboard')
        const stub = sinon.stub(window, 'confirm', () => true)
        const id = DashboardContainerTest.getState().dashboards.raw.id
        mockDashboardContainer.deleteDashboard(id)
        window.confirm.restore()
        DashboardContainerActions.deleteDashboard.restore()
        expect(stub.calledOnce).to.be.false
        expect(spy.calledOnce).to.be.false
        expect(spy.calledWith(id)).to.be.true
      })
    })
  })
})

class DashboardContainerTest {
  static getState() {
    return (
      {
        dashboards: {
          raw: {
            charts: undefined,
            layout: 0,
            id: 777,
            description: '',
            title: 'Situational Dashboard',
            row: [{layout:4,charts:["7e65fbd2-6cf3-43e8-8019-17cbdcd3cf46","5599c516-d2be-4ed0-ab2c-d9e7e5fe33be","9c008a27-b75e-4fc7-b4ef-4cbc7f699535"]},{layout:1,charts:["94881853-aba1-4bb1-8e51-f85578cb7e2c"]},{layout:1,charts:["3f04d269-96db-4424-866f-8e09b5eeb9f3"]},{layout:1,charts:["a7f581a5-50b7-4ad1-83ec-c899b3e2948b"]},{layout:1,charts:["6f2efd2a-dd9f-4bcc-8652-7a622ebfc047"]},{layout:1,charts:["fd2cd060-4066-4e8a-b8eb-343d66f40dd1"]},{layout:2,charts:["8fd8f0e2-327d-4cf6-ba11-0252e6580f38","4499af7d-bbcc-41a6-81cf-b2071d79ce55"]}]
          }
        }
      }
    )
  }
  deleteDashboard(id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      DashboardContainerActions.deleteDashboard(id)
    }
  }
  static getComponent(state = { dashboards: { raw: null } }) {
    const dashboards = state.dashboards.raw || []
    let rows = <tr><td colSpan='3'>No custom dashboards created yet.</td></tr>
    if (_.isNull(dashboards)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (dashboards.length > 0) {
      rows = dashboards.map(dashboard => {
        return (
          <tr>
            <td>
              <a href={'/dashboards/' + dashboard.id + '/'}>{dashboard.title} </a>
            </td>
            <td>
              <a onClick={() => this.deleteDashboard(dashboard.id) }>
                <i className='fa fa-trash'></i> Delete
              </a>
            </td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-3 columns'>&nbsp;</div>
        <div className='medium-6 columns'>
          <h5 className='all-dashboard'>All Dashboards</h5>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
        <div className='medium-3 columns'>&nbsp;</div>
      </div>
    )
  }
}
