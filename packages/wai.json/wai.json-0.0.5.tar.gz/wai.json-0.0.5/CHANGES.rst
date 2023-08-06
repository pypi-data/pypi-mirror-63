Changelog
=========

0.0.5 (2020-03-18)
-------------------

- Removed unnecessary validation from sub-components of objects which already validate themselves.

0.0.4 (2020-03-04)
-------------------

- Fixed bug in ArrayProxy where __iadd__ wasn't returning itself.
- Fixed default values for list methods of ArrayProxy.

0.0.3 (2020-02-26)
-------------------

- EnumProperty now returns its values as a frozen-set to avoid copy operation.
- Optional properties can now have default values for if they're not specified.
- Additional methods/options for introspecting/altering properties.

0.0.2 (2020-02-21)
-------------------

- Added the ability to create a JSONObject property directly from the class.
- Properties can now be reused between JSON objects, as long as the attribute
  name stays the same.
- ConstantProperty and EnumProperty can now report their values.
- StaticJSONValidator can now cache schema/validators for unhashable objects.
- Pretty serialisation.
- Can query the optionality of a property.
- Can specify initial values by attribute name.
- Can see if the class OR an instance has a property (instances include additional
  properties).
- Iterating over properties now only iterates over the names, and can be done on the
  class or an instance, as above.
- Sub-types can pass programmatic properties in __init_subclass__.

0.0.1 (2020-02-20)
-------------------

- Initial release
