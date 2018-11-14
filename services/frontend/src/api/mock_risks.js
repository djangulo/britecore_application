// FIELD_TYPE_CHOICES = (
//   (0, _('text')),
//   (1, _('number')),
//   (2, _('date')),
//   (3, _('enum')),
// )
const dataTypes = {
  0: 'text',
  1: 'number',
  2: 'date',
  3: 'enum'
}

export const _risks = [
  {
    'id': 1,
    'name': 'Policy Risk',
    'fields': [
      {
        'id': 1,
        'name': 'first_name',
        'data_type': dataTypes[0],
      },
      {
        'id': 2,
        'name': 'last_name',
        'data_type': dataTypes[0],
      },
      {
        'id': 3,
        'name': 'birth_date',
        'data_type': dataTypes[2]
      }
    ]
  },
  {
    'id': 2,
    'name': 'Insurance Risk',
    'fields': [
      {
        'id': 1,
        'name': 'last_name',
        'data_type': 0,
      },
      {
        'id': 3,
        'name': 'birth_date',
        'data_type': dataTypes[2]
      }
    ]
  }
]