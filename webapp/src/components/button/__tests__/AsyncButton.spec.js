import React from 'react'
import { expect } from 'chai'
import { shallow } from 'enzyme'
import AsyncButton from '../AsyncButton'
import sinon from 'sinon'

chai.config.truncateThreshold = 0

describe ('AsyncButton', () => {

  it ('exists if instantiated', () => {
    const mockAsyncButton = new AsyncButton()
    expect (mockAsyncButton).to.exist
  })
  it ('extends React Component', () => {
    const mockAsyncButton = new AsyncButton()
    expect (mockAsyncButton instanceof React.Component).is.eq(true)
  })
  describe ('.propTypes', () => {
    it ('is static and exists', () => {
      expect (AsyncButton.propTypes).to.exist
    })
    it ('has specified properties in it', () => {
      expect (AsyncButton.propTypes).to.have.all.keys('text', 'alt_text', 'disabled', 'isBusy', 'onClick', 'icon', 'classes', 'style')
    })
  })
  describe ('.defaultProp', () => {
    it ('is static and exists', () => {
      expect (AsyncButton.defaultProps).to.exist
    })
    it ('has specified properties in it', () => {
      expect (AsyncButton.defaultProps).to.have.all.keys('text', 'icon', 'classes')
    })
    it ('default values are set correctly', () => {
      expect (AsyncButton.defaultProps.text).to.be.null
      expect (AsyncButton.defaultProps.icon).to.be.null
      expect (AsyncButton.defaultProps.classes).to.eq(' button ')
    })
  })
  describe ('#render()', () => {
    let expectedComponent
    let wrapper
    beforeEach(() => {
      expectedComponent = AsyncButtonTest.mockComponent()
      wrapper = shallow(<AsyncButton {...AsyncButtonTest.getProps()}/>)
    })
    it ('renders a button', () => {
      expect (wrapper.find('button')).to.have.length(1)
    })
    it ('has a span within', () => {
      expect (wrapper.contains(AsyncButtonTest.getSpan())).to.eq(true)
    })
  })
})
//Warning: Failed propType: Required prop `onClick` was not specified in `AsyncButton`
class AsyncButtonTest {
  static getProps() {
    return {
      text: 'Save Dashboard',
      alt_text: 'Saving ...',
      isBusy: true,
      classes: ' button ',
      onClick: () => {}
    }
  }
  static mockComponent() {
    const props = this.getProps()
    const icon_string = props.isBusy ? 'spinner fa-spin saving-icon' : props.icon
    return (
      <button disabled={props.disabled} className={props.classes} onClick={props.onClick} style={props.style}>
        { props.icon ? <i className={'fa fa-' + icon_string}></i> : '' }
        { this.getSpan() }
      </button>
    )
  }
  static getSpan() {
    const props = this.getProps()
    return (
        <span>
          { props.isBusy ? props.alt_text : props.text }
        </span>
      )
  }
}