import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import DropdownButton from '../DropdownButton'
import sinon from 'sinon'

describe.skip ('DropdownButton', () => {
  it ('exists', () => {
    expect (DropdownButton).to.exist
  })
  describe.skip ('.propTypes', () => {
    it ('is static and exists', () => {
      expect (DropdownButton.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DropdownButton.propTypes).to.have.all.keys('data', 'working', 'enable', 'text', 'cookieName', 'onClick', 'classes')
    })
  })
  describe.skip ('#defaults', () => {
    let mockDropdownButton
    beforeEach (() => {
      mockDropdownButton = new DropdownButton()
    })
    it ('has specified properties', () => {
      expect (mockDropdownButton.defaults).to.have.all.keys('url', 'isWorking')
    })
    it ('has correct initial values', () => {
      const state = DropdownButtonTest.getState()
      expect (mockDropdownButton.defaults.isWorking).to.eq(state.isWorking)
      expect (mockDropdownButton.defaults.url).to.eq(state.url)
    })
  })
  describe.skip ('#getInitialState()', () => {
    it ('returns defaults', () => {
      const mockDropdownButton = new DropdownButton()
      expect (mockDropdownButton.getInitialState()).to.deep.eq(mockDropdownButton.defaults)
    })
  })
  describe.skip ('#_completeDownload()', () => {
    it.skip ('completes download', () => {

    })
  })
  describe.skip ('#_download()', () => {
    it.skip ('downloads', () => {

    })
  })
  describe.skip ('#_getCookie()', () => {
    it.skip ('gets cookie', () => {

    })
  })
  describe.skip ('#render()', () => {
    let wrapper, expectedComponent
    beforeEach (() => {
      wrapper = shallow(<DropdownButton {...DropdownButtonTest.getProps()}/>)
      expectedComponent = DropdownButtonTest.mockComponent()
    })
    it.skip ('renders correct components', () => {
      expect (wrapper.equals(expectedComponent)).to.eq(true)
    })
    it ('contains a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it.skip ('contains an inner component', () => {
      expect (wrapper.contains(DropdownButtonTest.mockInnerComponent())).to.eq(true)
    })
    it ('simulates click events', () => {
      let spy = sinon.spy(DropdownButton.prototype.__reactAutoBindMap, "_download")
      wrapper = shallow(<DropdownButton {...DropdownButtonTest.getProps()} />)
      wrapper.find('button').simulate('click')
      expect (spy.calledOnce).to.equal(true)
      spy.restore()
    })
  })
})
class DropdownButtonTest {
  static getProps() {
    //update working variable if isWorking is switched to true
    return {
      text: 'stuff',
      enable: true,
      classes: '',
      working: 'bar',
      cookieName: 'foo',
      onClick: () => {}
    }
  }
  static getState() {
    return {
      isWorking: false,
      url: 'about:blank'
    }
  }
  static _download () {

  }
  static mockComponent() {
    const props = this.getProps()
    const state = this.getState()
    let text = state.isWorking ? props.working : props.text
    let classesString = props.enable && !state.isWorking ? 'button success expand ' : 'button success expand disabled '
    return (
      <button role='button'
        className={classesString + props.classes}
        onClick={this._download}>
        <i className='fa fa-fw fa-download' /> {text}
        <iframe width='0' height='0' className='hidden' src={state.url}></iframe>
      </button>
    )
  }
  static mockInnerComponent() {
    const props = this.getProps()
    const state = this.getState()
    let text = state.isWorking ? props.working : props.text
    let classesString = props.enable && !state.isWorking ? 'button success expand ' : 'button success expand disabled '
    //return needs to be fixed. div should be removed.
    return (
      <div>
        <i className='fa fa-fw fa-download' /> {text}
        <iframe width='0' height='0' className='hidden' src={state.url}></iframe>
      </div>
    )
  }
}