# SPDX-FileCopyrightText: 2022-present deepset GmbH <info@deepset.ai>
#
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Dict

from haystack.core.errors import DeserializationError, SerializationError
from haystack.core.serialization import generate_qualified_class_name, import_class_by_name


def serialize_class_instance(obj: Any) -> Dict[str, Any]:
    """
    Serializes an object that has a `to_dict` method into a dictionary.

    :param obj:
        The object to be serialized.
    :returns:
        A dictionary representation of the object.
    :raises SerializationError:
        If the object does not have a `to_dict` method.
    """
    if not hasattr(obj, "to_dict"):
        raise SerializationError(f"Object of class '{type(obj).__name__}' does not have a 'to_dict' method")

    output = obj.to_dict()
    return {"type": generate_qualified_class_name(type(obj)), "data": output}


def deserialize_class_instance(data: Dict[str, Any]) -> Any:
    """
    Deserializes an object from a dictionary representation generated by `auto_serialize_class_instance`.

    :param data:
        The dictionary to deserialize from.
    :returns:
        The deserialized object.
    :raises DeserializationError:
        If the serialization data is malformed, the class type cannot be imported, or the
        class does not have a `from_dict` method.
    """
    if "type" not in data:
        raise DeserializationError("Missing 'type' in serialization data")
    if "data" not in data:
        raise DeserializationError("Missing 'data' in serialization data")

    try:
        obj_class = import_class_by_name(data["type"])
    except ImportError as e:
        raise DeserializationError(f"Class '{data['type']}' not correctly imported") from e

    if not hasattr(obj_class, "from_dict"):
        raise DeserializationError(f"Class '{data['type']}' does not have a 'from_dict' method")

    return obj_class.from_dict(data["data"])
