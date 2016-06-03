import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import SourceDatasPage from 'components/pages/source_data/SourceDatasPage'
import SourceDataPage from 'components/pages/source_data/SourceDataPage'
import SourceDataEditPage from 'components/pages/source_data/SourceDataEditPage'

describe('SourceDatasPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<SourceDatasPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('SourceDataPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<SourceDataPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('SourceDataEditPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<SourceDataEditPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})
