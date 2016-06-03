import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import IndicatorsPage from 'components/pages/indicators/IndicatorsPage'
import IndicatorPage from 'components/pages/indicators/IndicatorPage'
import IndicatorEditPage from 'components/pages/indicators/IndicatorEditPage'

describe('IndicatorsPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<IndicatorsPage />)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => expect(output.type).toBe('div'))
})

describe('IndicatorPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<IndicatorPage />)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => expect(output.type).toBe('div'))
})

describe('IndicatorEditPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<IndicatorEditPage params={{indicator_id: 750}}/>)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => expect(output.type).toBe('div'))
})
