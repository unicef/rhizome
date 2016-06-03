import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import UsersPage from 'components/pages/users/UsersPage'
import UserPage from 'components/pages/users/UserPage'
import UserEditPage from 'components/pages/users/UserEditPage'

describe('UsersPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<UsersPage />)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('UserPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<UserPage />)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => expect(output.type).toBe('div'))
})

describe('UserEditPage', () => {
  const renderer = TestUtils.createRenderer()
  renderer.render(<UserEditPage />)
  const output = renderer.getRenderOutput()

  it ('renders an div', () => expect(output.type).toBe('div'))
})
