import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import ChartsPage from 'components/pages/charts/ChartsPage'
import ChartPage from 'components/pages/charts/ChartPage'
import ChartEditPage from 'components/pages/charts/ChartEditPage'

describe('ChartsPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<ChartsPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('ChartPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<ChartPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('ChartEditPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<ChartEditPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})
