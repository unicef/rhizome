// InterfaceMixin takes a list of string "interfaces"
// and adds a static called implementsInterface to the component that simply checks if an interface is in the list
// This way, a parent component can pass particular props only to children which implement the relevant interface
// by checking child.type.implementsInterface('SomeInterface')
// usage:
// mixins: [InterfaceMixin('SomeInterface')] // or...
// mixins: [InterfaceMixin(['SomeInterface', 'AnotherInterface'])]

let InterfaceMixin = function () {
  for (var _len = arguments.length, interfaces = Array(_len), _key = 0; _key < _len; _key++) {
    interfaces[_key] = arguments[_key]
  }

  return {
    statics: {
      implementsInterface: function implementsInterface (name) {
        return interfaces.indexOf(name) >= 0
      }
    }
  }
}

export default InterfaceMixin
