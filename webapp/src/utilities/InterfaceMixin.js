// THIS IS TECHNICAL DEBT THAT WE INHERITED FROM A MASSIVELY MIS MANAGED
// FRONT END TEAM.  THE CURRENT TEAM DOES NOT KNOW WHAT THIS DOES AND
// WE NEED TO REMOVE THIS ASAP //

// THIS IS TECHINCAL DEBT //

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
