Front End
========

::

  cd webapp && gulp mocha


Writing Tests
-------------

Dont's:
+++++++

When writing a test, use few words as possible to make the test make sense in english. Bad: ‘FooBar’ ‘it should exist’ - Good: ‘FooBar’ ‘exists’. The purpose for this is if the test messages will be more precise on the matter. “FooBar exists failed.”

Let’s write a basic test for an ES6 class.

file: FooBar.js

.. code-block:: javascript

    class FooBar {
      constructor(props) {
        this.instanceVariable = '010101'
      }
    }
    export default FooBar
    file: __tests__/FooBar.spec.js

    import FooBar from 'FooBar'
    import { expect } from 'chai'

    describe ('FooBar', () => {
      it ('exists', () => {
        expect (FooBar).to.exist
      })
      describe ('.constructor()', () => {
        it ('exists with 1 argument', () => {
          expect (FooBar.constructor).to.exist.and.have.lengthOf(1)
        })
      })
    })

This will check if there is a declaration of FooBar class and the second test is describing our static function constructor to have one argument and to exist. We place a dot in front of a property or function to indicate that it is a static function. Also, we add the parantheses to the function name to indicate it is a function.

Now let’s check for a instance function that returns a string.

In FooBar.js add a function to the class:


.. code-block:: javascript

    render() {
      return '1'
    }

Let’s test this works. We need to instantiate the object. In __tests__/FooBar.spec.js add a describe within the ‘FooBar’ describe

.. code-block:: javascript

    import FooBar from 'FooBar'
    import { expect } from 'chai'

    describe ('FooBar', () => {
      it ('exists', () => {
        expect (FooBar).to.exist
      })
      describe ('.constructor()', () => {
        it ('exists with 1 argument', () => {
          expect (FooBar.constructor).to.exist.and.have.lengthOf(1)
        })
      })
      describe ('#render()', () => {
        it ('returns the correct string', () => {
          const mockFooBar = new FooBar()
          expect (mockFooBar.render()).to.eq('1')
        })
      })
    })

We instantiate an object and now call this function to get the return value.

Let’s write a couple more simple tests on a React class.

file: someClass.js

.. code-block:: javascript

    import React from 'react'
    export default React.createClass {
      someFunction(param) {
        let returnValue = true
        if (!param) {
          returnValue = someOtherFunction()
        }
        return returnValue
      },
      someOtherFunction() {
        return null
      },
      render() {
        return 'empty'
      }
    }

file: someClass.spec.js

.. code-block:: javascript

    import React from 'react'
    import { expect } from 'chai'
    import { shallow } from 'enzyme'
    import sinon from 'sinon'

    import someClass from 'someClass'

    describe ('someClass', () => {
      describe('#someFunction()', () => {
        context ('argument given is true', () => {
          it ('returns true', () => {
            const wrapper = shallow(<someClass />)
            expect (wrapper.instance().someFunction(true)).to.be.true
          })
        })
      })
    })


We import the shallow function from enzyme, a test utility library, to help us mount our react class. This gives us access to a HUGE number of helper functions underneath. For example, wrapper.debug() will return the exact jsx returned from the render of the react class. See here for more documentation on enzyme.
We import sinon which will help us with callbacks on other functions for spying and stubbing functions to work for our needs.
We describe the class name, instance function name, and within a certain state, ‘context’, we insert a test case. If the given argument is true to the function someFunction the return value will be true.
The imported enzyme function we used to shallow render our react class, shallow, allows us to emulate the react behavior for a mounted class. We access the instance by calling with .instance() in order to gain access to .someFunction().
Now, lets add the other context which someFunction will call someOtherFunction:

.. code-block:: javascript

    describe ('someClass', () => {
      describe('#someFunction()', () => {
        context ('argument given is true', () => {
          it ('returns true', () => {
            const wrapper = shallow(<someClass />)
            expect (wrapper.instance().someFunction(true)).to.be.true
          })
        })
        context ('argument given is false', () => {
          it ('returns null', () => {
            const wrapper = shallow(<someClass />)
            expect (wrapper.instance().someFunction(false)).to.be.null
          })
        })
      })
    })


We utilize context to help with readability in the tests for anyone who may look through our tests. If it fails, it will display: “someClass #someFunction() argument given is false returns null” And indicate what is expected and what the actual value was.

If you noticed we were calling someOtherFunction within someFunction. This is so we can utilize sinon spy callback to check if this function is being called within our tests.

.. code-block:: javascript

    describe ('someClass', () => {
      describe('#someFunction()', () => {
        context ('argument given is true', () => {
          it ('returns true', () => {
            const wrapper = shallow(<someClass />)
            expect (wrapper.instance().someFunction(true)).to.be.true
          })
        })
        context ('argument given is false', () => {
          it ('returns null', () => {
            const wrapper = shallow(<someClass />)
            expect (wrapper.instance().someFunction(false)).to.be.null
          })
          it ('calls #someOtherFunction', () => {
            const wrapper = shallow(<someClass />)
            const spy = sinon.spy(someClass.prototype.__reactAutoBindMap, 'someOtherFunction')
            wrapper.instance().someFunction(false)
            spy.restore()
            expect(spy.calledOnce).to.be.true
          })
        })
      })
    })

We attach our spy to the someOtherFunction function by hooking into the prototype of react. We call someFunction with the false argument, we spy on someOtherFunction to see if it is called as a result of calling someFunction. We unwrap the someOtherFunction by calling spy.restore() to return it to normal state. See here for more documentation on sinon spies and stubs.
