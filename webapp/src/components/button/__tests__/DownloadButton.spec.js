import React from 'react'
import chai, { expect } from 'chai'
import { shallow } from 'enzyme'
import DownloadButton from '../DownloadButton'
import sinon from 'sinon'

describe ('DownloadButton', () => {
  it ('exists', () => {
    expect (DownloadButton).to.exist
  })
  describe ('.propTypes', () => {
    it ('is static and exists', () => {
      expect (DownloadButton.propTypes).to.exist
    })
    it ('has specified properties', () => {
      expect (DownloadButton.propTypes).to.have.all.keys('data', 'working', 'enable', 'text', 'cookieName', 'onClick', 'classes')
    })
  })
  describe ('#defaults', () => {
    let mockDownloadButton
    beforeEach (() => {
      mockDownloadButton = new DownloadButton()
    })
    it ('has specified properties', () => {
      expect (mockDownloadButton.defaults).to.have.all.keys('url', 'isWorking')
    })
    it ('has correct initial values', () => {
      expect (mockDownloadButton.defaults.isWorking).to.eq(false)
      expect (mockDownloadButton.defaults.url).to.eq('about:blank')
    })
  })
  describe ('#getInitialState()', () => {
    it ('returns defaults', () => {
      const mockDownloadButton = new DownloadButton()
      expect (mockDownloadButton.getInitialState()).to.deep.eq(mockDownloadButton.defaults)
    })
  })
  describe.skip ('#_completeDownload()', () => {

  })
  describe.skip ('#_download()', () => {

  })
  describe.skip ('#_getCookie()', () => {

  })
  describe ('#render()', () => {
    it ('renders the proper ')
  })
})
class DownloadButtonTest {
  static mockComponent() {
    let text = this.state.isWorking ? this.props.working : this.props.text
    let classesString = this.props.enable && !this.state.isWorking ? 'button success expand ' : 'button success expand disabled '
    return (
      <button role='button'
        className={classesString + this.props.classes}
        onClick={this._download}>
        <i className='fa fa-fw fa-download' /> {text}
        <iframe width='0' height='0' className='hidden' src={this.state.url}></iframe>
      </button>
    )
  }
}