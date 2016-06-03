import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import AboutPage from 'components/pages/info/AboutPage'
import BugReportPage from 'components/pages/info/BugReportPage'
import ContactPage from 'components/pages/info/ContactPage'
import SitemapPage from 'components/pages/info/SitemapPage'

describe('AboutPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<AboutPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('BugReportPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<BugReportPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('ContactPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<ContactPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('SitemapPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<SitemapPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})
