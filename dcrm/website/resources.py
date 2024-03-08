from .models import Quote_det,Quote_ovr
from import_export import resources


class Quote_ovrResource(resources.ModelResource):
    class meta:
        model =Quote_ovr


class Quote_detResource(resources.ModelResource):
    class meta:
        model =Quote_det
