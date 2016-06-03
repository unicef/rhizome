import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import ManageSystemPage from 'components/pages/ManageSystemPage'

describe('ManageSystemPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<ManageSystemPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

