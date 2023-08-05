"""handle relationship between django model and graphene type. """

import typing
from functools import lru_cache

import django.db.models as djm

if typing.TYPE_CHECKING:
    import django.contrib.contenttypes.models as ctm

REGISTRY: typing.Dict[typing.Type[djm.Model], str] = {}


@lru_cache()
def get_models(v: str) -> typing.List[typing.Type[djm.Model]]:
    """Get models for typename.

    Args:
        v (str): typename

    Returns:
        typing.List[djm.Model]: list of models that registered for this typename.
    """

    ret = []
    for model, typename in REGISTRY.items():
        if typename == v:
            ret.append(model)
    return ret


def get_model(typename: str) -> typing.Type[djm.Model]:
    """Get django model for typename.

    Args:
        typename (str): Graphql typename.

    Raises:
        ValueError: When not exact one matched model for given typename.

    Returns:
        typing.Type[djm.Model]: Model registered for given typename.
    """

    models = get_models(typename)
    if len(models) != 1:
        raise ValueError(
            f"Can not determinate model from typename: typename={typename}")
    return models[0]


@lru_cache()
def get_typename(model: typing.Type[djm.Model]) -> str:
    """Get typename for model, support inheritance.

    Args:
        model (typing.Type[djm.Model]): Model.

    Raises:
        ValueError: When model is not registered.

    Returns:
        str: Typename for this model.
    """

    if model in REGISTRY:
        return REGISTRY[model]

    for k, v in REGISTRY.items():
        if issubclass(model, k):
            return v

    raise ValueError(
        f'No typename has not registed for: {repr(model)}')


def get_content_type(typename: str) -> 'ctm.ContentType':
    """Get django.contrib.contenttype for typename.

    Args:
        typename (str): Graphql typename.

    Raises:
        ValueError: When not exact one matched model for given typename.

    Returns:
        ctm.ContentType: ContentType object for given typename.
    """
    # pylint: disable=import-outside-toplevel

    import django.contrib.contenttypes.models as ctm
    model = get_model(typename)
    return ctm.ContentType.objects.get_for_model(model)
