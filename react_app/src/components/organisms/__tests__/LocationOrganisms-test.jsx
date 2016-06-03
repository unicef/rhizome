import React from 'react'
import expect from 'expect'
import expectJSX from 'expect-jsx'
import TestUtils from 'react-addons-test-utils'
import ResourceTable from 'components/molecules/ResourceTable'
import LocationTable from 'components/organisms/locations/LocationTable'

expect.extend(expectJSX)

describe('LocationTable', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<LocationTable />)
  let output = renderer.getRenderOutput()

  it ('renders a ResourceTable', () => {
    expect(output.type).toEqual(ResourceTable)
  })
})
