from rest_framework.fields import ListField
import traceback


class StringArrayField(ListField):
    """
    String representation of an array field.
    """
    def to_representation(self, obj):
        try:
            obj = super().to_representation(obj)
            # convert list to string
            return ",".join([str(element) for element in obj])

        except Exception as exc:
            print(traceback.format_exc())

    def to_internal_value(self, data):
        try:
            data = data.split(",")  # convert string to list
            return super().to_internal_value(data)

        except Exception as exc:
            print(traceback.format_exc())
