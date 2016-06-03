import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import LocationsPage from 'components/pages/locations/LocationsPage'
import LocationPage from 'components/pages/locations/LocationPage'
import LocationEditPage from 'components/pages/locations/LocationEditPage'

describe('LocationsPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<LocationsPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('LocationPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<LocationPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('LocationEditPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<LocationEditPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})
