import React from 'react'
import { expect } from 'chai'
import { render, shallow } from 'enzyme'
import DashboardsContainer from '../DashboardsContainer'
import DashboardActions from 'actions/DashboardActions'

describe ('DashboardsContainer', () => {
  it ('exists', () => {
    expect (DashboardsContainer).to.exist
  })
  describe ('#render()', () => {
    it ('exists', () => {
      const mockDropdownMenuItem = new DashboardsContainer()
      expect (mockDropdownMenuItem.render).to.exist
    })
    it.skip ('renders correct jsx', () => {
      const props = DashboardsContainerTest.getProps()
      const actualComponent = shallow(<DashboardsContainer {...props}/>).debug()
      const expectedComponent = shallow(DashboardsContainerTest.getComponent()).debug()
      expect (actualComponent).to.equal(expectedComponent)
    })
  })
})

class DashboardsContainerTest {
  static getProps() {
    return {
      values: [{check: {value: 1, title: 'foo'}}, {check: {value: 2, title: 'bar'}}, {check: {value: 3, title: 'foobar'}}],
      value: '1',
      name: 'foo',
      prefix: '',
      horizontal: false,
      title: 'bar',
      onChange: () => null
    }
  }
  static getDefaultProps () {
    return {
      prefix: '',
      horizontal: false
    }
  }
  deleteDashboard(id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      DashboardActions.deleteDashboard(id)
    }
  }
  static getComponent() {
    const props = this.getProps()
    const radios = props.values.map((radio, index) => {
      return (
        <div key={radio.value} className={props.horizontal ? 'horizontal' : null}>
          <input type='radio' name={props.name} id={`${props.prefix}${radio.value}`}
            value={radio.value}
            checked={props.value === radio.value ? 'checked' : false}
            onChange={() => props.onChange(radio.value)}
            />
          <label htmlFor={`${props.prefix}${radio.value}`}>{radio.title}</label>
        </div>
      )
    })
    return (
      <div className='radio-group-container'>
        <h4>{props.title}</h4>
        {radios}
      </div>
    )
  }
}
