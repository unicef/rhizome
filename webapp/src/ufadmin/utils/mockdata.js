module.exports = {
  schemas: {
    users: {
      '$schema': 'http:// json-schema.org/draft-04/schema#',
      title: 'Users',
      type: 'array',

      'defaultSortField': 'last_name',
      'defaultSortDirection': 'asc',
      'primaryKey': 'id',

      items: {
        title: 'User',
        type: 'object',

        properties: {
          date_joined: {
            title: 'date_joined',
            default: '2015-05-15 02:09:53.567367+00:00',
            maxLength: null,
            editable: true,
            type: 'string',
            format: 'date-time',
            display: {
              weightForm: 3,
              on_table: true,
              weightTable: 3
            }
          },
          email: {
            title: 'email',
            default: '',
            maxLength: 75,
            editable: true,
            type: 'string',
            display: {
              weightForm: 5,
              on_table: true,
              weightTable: 5
            }
          },
          first_name: {
            default: '',
            maxLength: 30,
            title: 'first_name',
            editable: true,
            type: 'string',
            display: {
              weightForm: 6,
              on_table: true,
              weightTable: 6
            }
          },
          groups: {
            maxLength: null,
            title: 'groups',
            editable: true,
            type: 'list',
            display: {
              weightForm: 7,
              on_table: true,
              weightTable: 7
            },
            items: {
              enum: [ // oneOf matches one of multiple schemas, enum matches one of values
                {
                  title: 'UNICEF HQ',
                  value: 1
                }
              ]
            }
          },
          id: {
            default: 'None',
            maxLength: null,
            title: 'id',
            editable: true,
            type: 'number',
            display: {
              weightForm: 9,
              on_table: true,
              weightTable: 9
            }
          },
          is_active: {
            default: 'True',
            maxLength: null,
            title: 'is_active',
            editable: true,
            type: 'boolean',
            display: {
              weightForm: 11,
              on_table: true,
              weightTable: 11
            }
          },
          is_staff: {
            default: 'False',
            maxLength: null,
            title: 'is_staff',
            editable: true,
            type: 'boolean',
            display: {
              weightForm: 12,
              on_table: true,
              weightTable: 12
            }
          },
          is_superuser: {
            default: 'False',
            maxLength: null,
            title: 'is_superuser',
            editable: true,
            type: 'boolean',
            display: {
              weightForm: 13,
              on_table: true,
              weightTable: 13
            }
          },
          last_login: {
            default: '2015-05-15 02:09:53.567582+00:00',
            maxLength: null,
            title: 'last_login',
            editable: true,
            type: 'string',
            format: 'date-time',
            display: {
              weightForm: 14,
              on_table: true,
              weightTable: 14
            }
          },
          last_name: {
            default: '',
            maxLength: 30,
            title: 'last_name',
            editable: true,
            type: 'string',
            display: {
              weightForm: 15,
              on_table: true,
              weightTable: 15
            }
          },
          password: {
            default: '',
            maxLength: 128,
            title: 'password',
            editable: true,
            type: 'string',
            display: {
              weightForm: 17,
              on_table: true,
              weightTable: 17
            }
          },
          user_permissions: {
            default: '',
            maxLength: null,
            title: 'user_permissions',
            editable: true,
            type: 'list',
            display: {
              weightForm: 21,
              on_table: true,
              weightTable: 21
            }
          },
          username: {
            default: '',
            maxLength: 30,
            title: 'username',
            editable: true,
            type: 'string',
            display: {
              weightForm: 22,
              on_table: true,
              weightTable: 22
            }
          }
        }
      }
    }
  }
}
