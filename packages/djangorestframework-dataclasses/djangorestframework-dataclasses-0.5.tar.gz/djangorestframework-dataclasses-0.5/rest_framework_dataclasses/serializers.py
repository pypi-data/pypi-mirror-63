import copy
import dataclasses
import datetime
import decimal
import uuid
from collections import OrderedDict
from typing import List, Type, Dict, Any, Tuple, Mapping

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.utils.functional import cached_property
import rest_framework.fields
import rest_framework.serializers
from rest_framework.relations import PrimaryKeyRelatedField, HyperlinkedRelatedField
from rest_framework.utils.field_mapping import get_relation_kwargs

from rest_framework_dataclasses import field_utils, typing_utils
from rest_framework_dataclasses.field_utils import DataclassDefinition, get_dataclass_definition, TypeInfo


# Define some types to make type hinting more readable
SerializerField = rest_framework.fields.Field
KWArgs = Dict[str, Any]
SerializerFieldDefinition = Tuple[Type[SerializerField], KWArgs]


# noinspection PyMethodMayBeStatic
class DataclassSerializer(rest_framework.serializers.Serializer):
    """
    A `DataclassSerializer` is just a regular `Serializer`, except that:

    * A set of default fields are automatically populated.
    * A set of default validators are automatically populated.
    * Default `.create()` and `.update()` implementations are provided.

    The process of automatically determining a set of serializer fields based on the dataclass fields is slightly
    complex, but you almost certainly don't need to dig into the implementation.

    If the `DataclassSerializer` class *doesn't* generate the set of fields that you need you should either declare the
    extra/differing fields explicitly on the serializer class, or simply use a `Serializer` class.

    Note that this implementation is heavily based on that of ModelSerializer in the rest_framework source code.
    """

    # The mapping of field types to serializer fields
    serializer_field_mapping = {
        int:                rest_framework.fields.IntegerField,
        float:              rest_framework.fields.FloatField,
        bool:               rest_framework.fields.BooleanField,
        str:                rest_framework.fields.CharField,
        decimal.Decimal:    rest_framework.fields.DecimalField,
        datetime.date:      rest_framework.fields.DateField,
        datetime.datetime:  rest_framework.fields.DateTimeField,
        datetime.time:      rest_framework.fields.TimeField,
        datetime.timedelta: rest_framework.fields.DurationField,
        uuid.UUID:          rest_framework.fields.UUIDField,
    }
    serializer_related_field = PrimaryKeyRelatedField

    # Override constructor to allow "anonymous" usage by passing the dataclass type and extra kwargs as a constructor
    # parameter instead of via a Meta class.
    def __init__(self, *args, **kwargs):
        self.dataclass = kwargs.pop('dataclass', None)
        self.extra_kwargs = kwargs.pop('extra_kwargs', None)
        super(DataclassSerializer, self).__init__(*args, **kwargs)

    # Parse and validate the configuration to a more usable format

    @cached_property
    def dataclass_definition(self) -> DataclassDefinition:
        # Determine the dataclass that we should operate on.
        if self.dataclass:
            assert not hasattr(self, 'Meta'), (
                "Class '{serializer_class}' may not have `Meta` attribute when instantiated with `dataclass` parameter."
                .format(serializer_class=self.__class__.__name__)
            )

            dataclass_type = self.dataclass
        else:
            assert hasattr(self, 'Meta'), (
                "Class '{serializer_class}' missing `Meta` attribute."
                .format(serializer_class=self.__class__.__name__)
            )
            assert hasattr(self.Meta, 'dataclass'), (
                "Class '{serializer_class}' missing `Meta.dataclass` attribute."
                .format(serializer_class=self.__class__.__name__)
            )

            dataclass_type = self.Meta.dataclass

        # Make sure we're dealing with an actual dataclass.
        if not dataclasses.is_dataclass(dataclass_type):
            raise ValueError(
                "Class '{serializer_class}' can only be used to serialize dataclasses."
                .format(serializer_class=self.__class__.__name__)
            )

        return get_dataclass_definition(dataclass_type)

    # Default `create` and `update` behavior...

    def instantiate_data_dictionaries(self, validated_data, instance=None):
        """
        Instantiate the values in a deserialized data dictionaries to their respective classes (for now only nested
        dataclasses).
        """
        # I'm not sure this is actually the best way to deserialize into nested dataclasses. The cleanest way seems to
        # be overriding to_internal_value(), but the top-level serializer must return a dictionary from that method. We
        # could split nested dataclasses off into a separate DataclassField (which could in general clean-up the code a
        # bit), but that breaks specifying nested serializers using a single class. Let's use this ugly hack until I can
        # think of something better.

        ret = {}
        for attr, value in validated_data.items():
            field = self.fields[attr]

            if value is None:
                # If the value is None, we don't care about mapping it to the correct dataclass type.
                pass
            elif isinstance(field, DataclassSerializer):
                value = (field.update(getattr(instance, attr), value)
                         if instance and getattr(instance, attr) else field.create(value))
            elif (isinstance(field, rest_framework.fields.ListField) and
                  isinstance(field.child, DataclassSerializer) or
                  isinstance(field, rest_framework.serializers.ListSerializer) and
                  isinstance(field.child, DataclassSerializer)):
                value = [field.child.create(item) if item else None for item in value]
            elif isinstance(field, rest_framework.fields.DictField) and isinstance(field.child, DataclassSerializer):
                value = {key: field.child.create(item) if item else None for key, item in value.items()}

            ret[attr] = value

        return ret

    def create(self, validated_data):
        dataclass_type = self.dataclass_definition.dataclass_type
        return dataclass_type(**self.instantiate_data_dictionaries(validated_data))

    def update(self, instance, validated_data):
        for attr, value in self.instantiate_data_dictionaries(validated_data, instance).items():
            setattr(instance, attr, value)
        return instance

    # Determine the fields to apply...

    def get_fields(self) -> Dict[str, SerializerField]:
        """
        Return the dict of field names -> field instances that should be used for `self.fields` when instantiating the
        serializer.
        """
        declared_fields = copy.deepcopy(self._declared_fields)

        # Determine all fields that should be included on the serializer.
        field_names = self.get_field_names()

        # Determine any extra field arguments that should be included.
        extra_kwargs = self.get_extra_kwargs()

        # Determine the fields that should be included on the serializer.
        fields = OrderedDict()

        for field_name in field_names:
            # If the field is explicitly declared on the class then use that.
            if field_name in declared_fields:
                assert field_name not in extra_kwargs, (
                    "Cannot both declare the field '{field_name}' and include it in '{serializer_class}' "
                    "`extra_kwargs` or `read_only_fields` option. Move all options to the field declaration."
                    .format(field_name=field_name, serializer_class=self.__class__.__name__)
                )

                fields[field_name] = declared_fields[field_name]
                continue

            extra_field_kwargs = extra_kwargs.get(field_name, {})
            fields[field_name] = self.create_field(field_name, extra_field_kwargs)

        return fields

    # Methods for determining the set of field names to include...

    def get_field_names(self) -> List[str]:
        """
        Returns the list of all field names that should be created when instantiating this serializer class. This is
        based on the default set of fields, but also takes into account the `Meta.fields` or `Meta.exclude` options
        if they have been specified.
        """
        # Retrieve metadata about the declared fields.
        declared_fields = self._declared_fields

        # Read configuration from Meta class.
        meta = getattr(self, 'Meta', None)
        fields = getattr(meta, 'fields', None)
        exclude = getattr(meta, 'exclude', None)

        if fields and fields != rest_framework.serializers.ALL_FIELDS and not isinstance(fields, (list, tuple)):
            raise TypeError(
                "The `fields` option must be a list or tuple or '__all__'. Got '{type}'."
                .format(type=type(fields).__name__)
            )

        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                "The `exclude` option must be a list or tuple. Got '{type}'."
                .format(type=type(exclude).__name__)
            )

        assert not (fields and exclude), (
            "Cannot set both `fields` and `exclude` options on serializer '{serializer_class}'."
            .format(serializer_class=self.__class__.__name__)
        )

        # If fields is not specified, or is the magic all fields option, make it a list consisting of the all fields
        # placeholder for now.
        if fields is None or fields == rest_framework.serializers.ALL_FIELDS:
            fields = [rest_framework.serializers.ALL_FIELDS]

        if rest_framework.serializers.ALL_FIELDS not in fields:
            # If fields are explicitly specified, and it is not the all fields magic option, ensure that all included
            # fields are valid.
            for field_name in fields:
                assert field_name in self.dataclass_definition.fields or field_name in declared_fields, (
                    "The field '{field_name}' was included on serializer {serializer_class} in the `fields` option, "
                    "but does not match any dataclass field."
                    .format(field_name=field_name, serializer_class=self.__class__.__name__)
                )

            # Also ensure that all declared fields are included. Do not require any fields that are declared in a parent
            # class, in order to allow serializer subclasses to only include a subset of fields.
            required_field_names = set(declared_fields)
            for cls in self.__class__.__bases__:
                required_field_names -= set(getattr(cls, '_declared_fields', []))

            for field_name in required_field_names:
                assert field_name in fields, (
                    "The field '{field_name}' was declared on serializer '{serializer_class}', but has not been "
                    "included in the `fields` option."
                    .format(field_name=field_name, serializer_class=self.__class__.__name__)
                )
            return fields

        # The field list now includes the magic all fields option, so replace it with the default field names.
        fields = list(fields)
        fields.remove(rest_framework.serializers.ALL_FIELDS)
        fields.extend(self.get_default_field_names(declared_fields))

        if exclude is not None:
            # If `Meta.exclude` is included, then remove those fields.
            for field_name in exclude:
                assert field_name not in declared_fields, (
                    "Cannot both declare the field '{field_name}' and include it in '{serializer_class}' `exclude` "
                    "option. Remove the field or, if inherited from a parent serializer, disable with "
                    "`{field_name} = None`."
                    .format(field_name=field_name, serializer_class=self.__class__.__name__)
                )

                assert field_name in fields, (
                    "The field '{field_name}' was included on serializer {serializer_class} in the `exclude` option, "
                    "but does not match any dataclass field."
                    .format(field_name=field_name, serializer_class=self.__class__.__name__)
                )

                fields.remove(field_name)

        return fields

    def get_default_field_names(self, declared_fields: Mapping[str, SerializerField]) \
            -> List[str]:
        """
        Return the default list of field names that will be used if the `Meta.fields` option is not specified.
        """
        return (
            list(declared_fields) +
            list(self.dataclass_definition.fields)
        )

    # Methods for constructing serializer fields...

    def create_field(self, field_name: str, extra_kwargs: KWArgs) -> SerializerField:
        # Get the source field (this can be useful to represent a single dataclass field in multiple ways in the
        # serialization state).
        source = extra_kwargs.get('source', '*')
        if source == '*':
            source = field_name

        # Determine the serializer field class and keyword arguments.
        if source in self.dataclass_definition.fields:
            type_info = field_utils.get_type_info(self.dataclass_definition.field_types[source])
            field_class, field_kwargs = self.build_typed_field(source, type_info, extra_kwargs)
        elif hasattr(self.dataclass_definition.dataclass_type, source):
            field_class, field_kwargs = self.build_property_field(source)
        else:
            field_class, field_kwargs = self.build_unknown_field(source)

        # Include any extra kwargs defined through `Meta.extra_kwargs`
        field_kwargs = self.include_extra_kwargs(field_kwargs, extra_kwargs)

        # Create the serializer field instance.
        return field_class(**field_kwargs)

    def build_typed_field(self, field_name: str, type_info: TypeInfo,
                          extra_kwargs: KWArgs) -> SerializerFieldDefinition:
        """
        Create a serializer field for a typed dataclass field.
        """
        if type_info.is_mapping or type_info.is_many:
            field_class, field_kwargs = self.build_composite_field(field_name, type_info, extra_kwargs)
        elif dataclasses.is_dataclass(type_info.base_type):
            field_class, field_kwargs = self.build_nested_field(field_name, type_info)
        elif isinstance(type_info.base_type, type) and issubclass(type_info.base_type, Model):
            field_class, field_kwargs = self.build_relational_field(field_name, type_info)
        elif typing_utils.is_literal_type(type_info.base_type):
            field_class, field_kwargs = self.build_literal_field(field_name, type_info)
        else:
            field_class, field_kwargs = self.build_standard_field(field_name, type_info)

        if type_info.is_optional:
            field_kwargs['required'] = False
            field_kwargs['allow_null'] = True

        return field_class, field_kwargs

    def build_composite_field(self, field_name: str, type_info: TypeInfo,
                              extra_kwargs: KWArgs) -> SerializerFieldDefinition:
        """
        Create a composite (mapping or list) field.
        """
        # Recurse to build the child field (i.e. the field of every instance). We pass the extra kwargs that are
        # specified for the child field through, so these can be used to recursively specify kwargs for child fields.
        extra_child_field_kwargs = extra_kwargs.get('child_kwargs', {})
        base_type_info = field_utils.get_type_info(type_info.base_type)
        child_field_class, child_field_kwargs = self.build_typed_field(field_name, base_type_info,
                                                                       extra_child_field_kwargs)

        # Include the extra kwargs specified for the child field before instantiating it.
        child_field_kwargs = self.include_extra_kwargs(child_field_kwargs, extra_child_field_kwargs)

        # Create child field and initialize parent field kwargs
        child_field = child_field_class(**child_field_kwargs)
        field_kwargs = {'child': child_field}

        if type_info.is_mapping:
            field_class = rest_framework.fields.DictField
        else:
            field_class = rest_framework.fields.ListField

        return field_class, field_kwargs

    def build_standard_field(self, field_name: str, type_info: TypeInfo) -> SerializerFieldDefinition:
        """
        Create regular dataclass fields.
        """
        try:
            field_class = field_utils.lookup_type_in_mapping(self.serializer_field_mapping, type_info.base_type)
            field_kwargs = {}

            return field_class, field_kwargs
        except KeyError:
            # When resolving the type hint fails, raise a nice descriptive error based on the outermost type of the
            # field (this makes solving deep recursive errors much easier).
            field_type = self.dataclass_definition.field_types[field_name]
            raise NotImplementedError(
                "Automatic serializer field deduction not supported for field '{field}' on '{dataclass}' "
                "of type '{type}'."
                .format(dataclass=self.dataclass_definition.dataclass_type.__name__, field=field_name, type=field_type)
            )

    def build_relational_field(self, field_name: str, type_info: TypeInfo) -> SerializerFieldDefinition:
        """
        Create fields for models.
        """
        relation_info = field_utils.get_relation_info(self.dataclass_definition, type_info)
        field_class = self.serializer_related_field
        field_kwargs = get_relation_kwargs(field_name, relation_info)

        # `view_name` is only valid for hyperlinked relationships.
        if not issubclass(field_class, HyperlinkedRelatedField):
            field_kwargs.pop('view_name', None)

        return field_class, field_kwargs

    def build_literal_field(self, field_name: str, type_info: TypeInfo) -> SerializerFieldDefinition:
        """
        Create ChoiceField from a Literal[...] type.
        """
        field_class = rest_framework.fields.ChoiceField
        choices = typing_utils.get_literal_choices(type_info.base_type)
        field_kwargs = {
            'choices': [val for val in choices if val not in (None, '')],
            'allow_blank': '' in choices,
        }

        return field_class, field_kwargs

    def build_nested_field(self, field_name: str, type_info: TypeInfo) -> SerializerFieldDefinition:
        """
        Create fields for dataclasses.
        """
        field_class = DataclassSerializer
        field_kwargs = {'dataclass': type_info.base_type,
                        'many': type_info.is_many}

        return field_class, field_kwargs

    def build_property_field(self, field_name: str) -> SerializerFieldDefinition:
        """
        Create a read only field for dataclass methods and properties.
        """
        field_class = rest_framework.fields.ReadOnlyField
        field_kwargs = {}

        return field_class, field_kwargs

    def build_unknown_field(self, field_name: str) -> SerializerFieldDefinition:
        """
        Raise an error on any unknown fields.
        """
        raise ImproperlyConfigured(
            "Field name '{field_name}' is not valid for dataclass '{class_name}'."
            .format(field_name=field_name, class_name=self.dataclass_definition.dataclass_type.__name__)
        )

    # Methods for determining additional keyword arguments to apply...

    def include_extra_kwargs(self, kwargs: KWArgs, extra_kwargs: KWArgs) -> KWArgs:
        """
        Include any `extra_kwargs` that have been included for this field, possibly removing any incompatible existing
        keyword arguments.
        """
        # If the field is made read only, drop write-only related arguments.
        if extra_kwargs.get('read_only', False):
            for attr in [
                'required', 'default', 'allow_blank', 'allow_null',
                'min_length', 'max_length', 'min_value', 'max_value',
                'validators', 'queryset'
            ]:
                kwargs.pop(attr, None)

        # If `default` is specified, `required` may not be specified. If the field is not explicitly specified as not
        # required (the behaviour of `default`), remove that specification.
        if extra_kwargs.get('default') and kwargs.get('required') is False:
            kwargs.pop('required')

        if extra_kwargs.get('read_only', kwargs.get('read_only', False)):
            extra_kwargs.pop('required', None)  # Read only fields should always omit the 'required' argument.

        if 'child_kwargs' in extra_kwargs:
            extra_kwargs.pop('child_kwargs', None)  # Always drop the child_kwargs field, as it's applied manually

        kwargs.update(extra_kwargs)

        return kwargs

    def get_extra_kwargs(self) -> KWArgs:
        """
        Return a dictionary mapping field names to a dictionary of additional keyword arguments.
        """
        meta = getattr(self, 'Meta', None)
        extra_kwargs = copy.deepcopy(getattr(meta, 'extra_kwargs', None)) if meta is not None else None
        if extra_kwargs is None:
            extra_kwargs = self.extra_kwargs or {}

        read_only_fields = getattr(meta, 'read_only_fields', None)
        if read_only_fields is not None:
            if not isinstance(read_only_fields, (list, tuple)):
                raise TypeError(
                    "The `read_only_fields` option must be a list or tuple. Got '{type}'."
                    .format(type=type(read_only_fields).__name__)
                )
            for field_name in read_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs['read_only'] = True
                extra_kwargs[field_name] = kwargs

        else:
            # Guard against the possible misspelling `readonly_fields` (used
            # by the Django admin and others).
            assert not hasattr(meta, 'readonly_fields'), (
                "Serializer '{serializer_class}' has field `readonly_fields`; the correct spelling for the option is "
                "`read_only_fields`."
                .format(serializer_class=self.__class__.__name__)
            )

        return extra_kwargs


class HyperlinkedDataclassSerializer(DataclassSerializer):
    serializer_related_field = HyperlinkedRelatedField

    def build_nested_field(self, field_name: str, type_info: TypeInfo) -> SerializerFieldDefinition:
        """
        Create fields for dataclasses.
        """
        field_class = HyperlinkedDataclassSerializer
        field_kwargs = {'dataclass': type_info.base_type,
                        'many': type_info.is_many,
                        'allow_null': type_info.is_optional}

        return field_class, field_kwargs
