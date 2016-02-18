function InterfaceMixin () {
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
