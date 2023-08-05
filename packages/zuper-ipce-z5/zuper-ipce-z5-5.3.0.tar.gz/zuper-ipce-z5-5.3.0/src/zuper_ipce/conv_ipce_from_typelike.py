import copy
import dataclasses
import datetime
import warnings
from dataclasses import Field, is_dataclass, replace
from decimal import Decimal
from numbers import Number
from typing import (
    cast,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
)

import numpy as np

from zuper_ipce import IPCE
from zuper_typing import dataclass
from zuper_typing.aliases import TypeLike
from zuper_typing.annotations_tricks import (
    get_Callable_info,
    get_ClassVar_arg,
    get_Dict_name_K_V,
    get_fields_including_static,
    get_FixedTupleLike_args,
    get_FixedTupleLike_name,
    get_ForwardRef_arg,
    get_NewType_arg,
    get_NewType_name,
    get_Optional_arg,
    get_Sequence_arg,
    get_Set_name_V,
    get_Tuple_name,
    get_Type_arg,
    get_TypeVar_bound,
    get_TypeVar_name,
    get_Union_args,
    get_VarTuple_arg,
    is_Any,
    is_Callable,
    is_ClassVar,
    is_FixedTupleLike,
    is_ForwardRef,
    is_NewType,
    is_Optional,
    is_Sequence,
    is_TupleLike,
    is_Type,
    is_TypeLike,
    is_TypeVar,
    is_Union,
    is_VarTuple,
)
from zuper_typing.constants import BINDINGS_ATT, GENERIC_ATT2
from zuper_typing.exceptions import (
    ZAssertionError,
    ZNotImplementedError,
    ZTypeError,
    ZValueError,
)
from zuper_typing.my_dict import (
    get_DictLike_args,
    get_ListLike_arg,
    get_ListLike_name,
    get_SetLike_arg,
    is_DictLike,
    is_ListLike,
    is_SetLike,
)
from zuper_typing.my_intersection import get_Intersection_args, is_Intersection
from zuper_typing.recursive_tricks import get_name_without_brackets
from .constants import (
    ALL_OF,
    ANY_OF,
    ATT_PYTHON_NAME,
    CALLABLE_ORDERING,
    CALLABLE_RETURN,
    ID_ATT,
    IESO,
    IPCE_PASS_THROUGH,
    JSC_ADDITIONAL_PROPERTIES,
    JSC_ARRAY,
    JSC_BOOL,
    JSC_DEFINITIONS,
    JSC_DESCRIPTION,
    JSC_INTEGER,
    JSC_ITEMS,
    JSC_NULL,
    JSC_NUMBER,
    JSC_OBJECT,
    JSC_PROPERTIES,
    JSC_PROPERTY_NAMES,
    JSC_REQUIRED,
    JSC_STRING,
    JSC_TITLE,
    JSC_TITLE_CALLABLE,
    JSC_TITLE_DATETIME,
    JSC_TITLE_DECIMAL,
    JSC_TITLE_FLOAT,
    JSC_TITLE_NUMPY,
    JSC_TITLE_SLICE,
    JSC_TITLE_TYPE,
    JSC_TYPE,
    JSONSchema,
    ProcessingDict,
    REF_ATT,
    SCHEMA_ATT,
    SCHEMA_BYTES,
    SCHEMA_CID,
    SCHEMA_ID,
    X_CLASSATTS,
    X_CLASSVARS,
    X_ORDER,
    X_PYTHON_MODULE_ATT,
)
from .ipce_spec import assert_canonical_ipce, sorted_dict_cbor_ord
from .schema_caching import (
    get_ipce_from_typelike_cache,
    set_ipce_from_typelike_cache,
    TRE,
)
from .schema_utils import make_ref, make_url
from .structures import FakeValues


def ipce_from_typelike(
    T: TypeLike,
    *,
    globals0: Optional[dict] = None,
    processing: Optional[ProcessingDict] = None,
    ieso: Optional[IESO] = None,
) -> JSONSchema:
    if ieso is None:
        ieso = IESO(with_schema=True)
    if processing is None:
        processing = {}
    if globals0 is None:
        globals0 = {}
    c = IFTContext(globals0, processing, ())
    tr = ipce_from_typelike_tr(T, c, ieso=ieso)
    schema = tr.schema
    assert_canonical_ipce(schema)
    return schema


@dataclass
class IFTContext:
    globals_: dict
    processing: ProcessingDict
    context: Tuple[str, ...]


def ipce_from_typelike_tr(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    if not is_TypeLike(T):
        raise ValueError(T)

    if hasattr(T, "__name__"):
        if T.__name__ in c.processing:
            ref = c.processing[T.__name__]
            res = make_ref(ref)
            return TRE(res, {T.__name__: ref})

        if ieso.use_ipce_from_typelike_cache:
            try:
                return get_ipce_from_typelike_cache(T, c.processing)
            except KeyError:
                pass

    try:

        if T is type:
            res = cast(
                JSONSchema,
                {
                    REF_ATT: SCHEMA_ID,
                    JSC_TITLE: JSC_TITLE_TYPE
                    # JSC_DESCRIPTION: T.__doc__
                },
            )
            res = sorted_dict_cbor_ord(res)
            return TRE(res)

        if T is type(None):
            res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, JSC_TYPE: JSC_NULL})
            res = sorted_dict_cbor_ord(res)
            return TRE(res)

        if isinstance(T, type):
            for klass in T.mro():
                if klass.__name__.startswith("Generic"):
                    continue
                if klass is object:
                    continue

                globals2 = dict(c.globals_)
                globals2[get_name_without_brackets(klass.__name__)] = klass

                bindings = getattr(klass, BINDINGS_ATT, {})
                for k, v in bindings.items():
                    if hasattr(v, "__name__") and v.__name__ not in globals2:
                        globals2[v.__name__] = v
                    globals2[k.__name__] = v

                c = dataclasses.replace(c, globals_=globals2)

        tr: TRE = ipce_from_typelike_tr_(T, c=c, ieso=ieso)

        if ieso.use_ipce_from_typelike_cache:
            set_ipce_from_typelike_cache(T, tr.used, tr.schema)

        return tr
    except IPCE_PASS_THROUGH:  # pragma: no cover
        raise
    except ValueError as e:
        msg = "Cannot get schema for type @T"
        raise ZValueError(msg, T=T, T_type=type(T), c=c) from e
    except AssertionError as e:
        msg = "Cannot get schema for type @T"
        raise ZAssertionError(msg, T=T, T_type=type(T), c=c) from e
    except BaseException as e:
        msg = "Cannot get schema for @T"
        raise ZTypeError(msg, T=T, c=c) from e


def ipce_from_typelike_DictLike(T: Type[Dict], c: IFTContext, ieso: IESO) -> TRE:
    assert is_DictLike(T), T
    K, V = get_DictLike_args(T)
    res = cast(JSONSchema, {JSC_TYPE: JSC_OBJECT})
    res[JSC_TITLE] = get_Dict_name_K_V(K, V)
    if isinstance(K, type) and issubclass(K, str):
        res[JSC_PROPERTIES] = {SCHEMA_ATT: {}}  # XXX
        tr = ipce_from_typelike_tr(V, c=c, ieso=ieso)
        res[JSC_ADDITIONAL_PROPERTIES] = tr.schema
        res[SCHEMA_ATT] = SCHEMA_ID
        res = sorted_dict_cbor_ord(res)
        return TRE(res, tr.used)
    else:
        res[JSC_PROPERTIES] = {SCHEMA_ATT: {}}  # XXX
        props = FakeValues[K, V]
        tr = ipce_from_typelike_tr(props, c=c, ieso=ieso)
        # logger.warning(f'props IPCE:\n\n {yaml.dump(tr.schema)}')

        res[JSC_ADDITIONAL_PROPERTIES] = tr.schema
        res[SCHEMA_ATT] = SCHEMA_ID
        res = sorted_dict_cbor_ord(res)
        return TRE(res, tr.used)


def ipce_from_typelike_SetLike(T: Type[Set], c: IFTContext, ieso: IESO) -> TRE:
    assert is_SetLike(T), T
    V = get_SetLike_arg(T)
    res = cast(JSONSchema, {JSC_TYPE: JSC_OBJECT})
    res[JSC_TITLE] = get_Set_name_V(V)
    res[JSC_PROPERTY_NAMES] = SCHEMA_CID
    tr = ipce_from_typelike_tr(V, c=c, ieso=ieso)
    res[JSC_ADDITIONAL_PROPERTIES] = tr.schema
    res[SCHEMA_ATT] = SCHEMA_ID
    res = sorted_dict_cbor_ord(res)
    return TRE(res, tr.used)


def ipce_from_typelike_TupleLike(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    assert is_TupleLike(T), T

    used = {}

    def f(x: TypeLike) -> JSONSchema:
        tr = ipce_from_typelike_tr(x, c=c, ieso=ieso)
        used.update(tr.used)
        return tr.schema

    if is_VarTuple(T):
        T = cast(Type[Tuple], T)
        items = get_VarTuple_arg(T)
        res = cast(JSONSchema, {})
        res[SCHEMA_ATT] = SCHEMA_ID
        res[JSC_TYPE] = JSC_ARRAY
        res[JSC_ITEMS] = f(items)
        res[JSC_TITLE] = get_Tuple_name(T)
        res = sorted_dict_cbor_ord(res)
        return TRE(res, used)
    elif is_FixedTupleLike(T):
        T = cast(Type[Tuple], T)
        args = get_FixedTupleLike_args(T)
        res = cast(JSONSchema, {})
        res[SCHEMA_ATT] = SCHEMA_ID
        res[JSC_TYPE] = JSC_ARRAY
        res[JSC_ITEMS] = []
        res[JSC_TITLE] = get_FixedTupleLike_name(T)
        for a in args:
            res[JSC_ITEMS].append(f(a))
        res = sorted_dict_cbor_ord(res)
        return TRE(res, used)
    else:
        assert False


class KeepTrackSer:
    def __init__(self, c: IFTContext, ieso: IESO):
        self.c = c
        self.ieso = ieso
        self.used = {}

    def ipce_from_typelike(self, T: TypeLike) -> JSONSchema:
        tre = ipce_from_typelike_tr(T, c=self.c, ieso=self.ieso)
        self.used.update(tre.used)
        return tre.schema

    # def ipce_from_object(self, x: IPCE, st: TypeLike) -> IPCE:
    #     from zuper_ipce.conv_ipce_from_object import ipce_from_object_
    #     res = object_from_ipce_(x, st, ieds=self.ieds, iedo=self.iedo)
    #     return res

    def tre(self, x: IPCE) -> TRE:
        return TRE(x, self.used)


def ipce_from_typelike_NewType(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    _ = c, ieso
    name = get_NewType_name(T)
    T0 = get_NewType_arg(T)
    kt = KeepTrackSer(c, ieso)
    res = cast(JSONSchema, {})
    res[SCHEMA_ATT] = SCHEMA_ID
    res[JSC_TYPE] = "NewType"
    res["newtype"] = kt.ipce_from_typelike(T0)
    res[JSC_TITLE] = name
    res = sorted_dict_cbor_ord(res)
    return kt.tre(res)


def ipce_from_typelike_ListLike(T: Type[List], c: IFTContext, ieso: IESO) -> TRE:
    assert is_ListLike(T), T
    items = get_ListLike_arg(T)
    res = cast(JSONSchema, {})
    kt = KeepTrackSer(c, ieso)

    res[SCHEMA_ATT] = SCHEMA_ID
    res[JSC_TYPE] = JSC_ARRAY
    res[JSC_ITEMS] = kt.ipce_from_typelike(items)
    res[JSC_TITLE] = get_ListLike_name(T)
    res = sorted_dict_cbor_ord(res)
    return kt.tre(res)


def ipce_from_typelike_Callable(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    assert is_Callable(T), T
    cinfo = get_Callable_info(T)

    kt = KeepTrackSer(c, ieso)

    res = cast(
        JSONSchema,
        {
            JSC_TYPE: JSC_OBJECT,
            SCHEMA_ATT: SCHEMA_ID,
            JSC_TITLE: JSC_TITLE_CALLABLE,
            "special": "callable",
        },
    )

    p = res[JSC_DEFINITIONS] = {}

    for k, v in cinfo.parameters_by_name.items():
        p[k] = kt.ipce_from_typelike(v)
    p[CALLABLE_RETURN] = kt.ipce_from_typelike(cinfo.returns)
    res[CALLABLE_ORDERING] = list(cinfo.ordering)
    # print(res)
    res = sorted_dict_cbor_ord(res)
    return kt.tre(res)


def ipce_from_typelike_tr_(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    if T is None:
        msg = "None is not a type!"
        raise ZValueError(msg)

    # This can actually happen inside a Tuple (or Dict, etc.) even though
    # we have a special case for dataclass

    if is_ForwardRef(T):  # pragma: no cover
        msg = "It is not supported to have an ForwardRef here yet."
        raise ZValueError(msg, T=T)

    if isinstance(T, str):  # pragma: no cover
        msg = "It is not supported to have a string here."
        raise ZValueError(msg, T=T)

    if T is str:
        res = cast(JSONSchema, {JSC_TYPE: JSC_STRING, SCHEMA_ATT: SCHEMA_ID})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is bool:
        res = cast(JSONSchema, {JSC_TYPE: JSC_BOOL, SCHEMA_ATT: SCHEMA_ID})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is Number:
        res = cast(JSONSchema, {JSC_TYPE: JSC_NUMBER, SCHEMA_ATT: SCHEMA_ID})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is float:
        res = cast(
            JSONSchema,
            {JSC_TYPE: JSC_NUMBER, SCHEMA_ATT: SCHEMA_ID, JSC_TITLE: JSC_TITLE_FLOAT},
        )
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is int:
        res = cast(JSONSchema, {JSC_TYPE: JSC_INTEGER, SCHEMA_ATT: SCHEMA_ID})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is slice:
        return ipce_from_typelike_slice(ieso=ieso)

    if T is Decimal:
        res = cast(
            JSONSchema,
            {JSC_TYPE: JSC_STRING, JSC_TITLE: JSC_TITLE_DECIMAL, SCHEMA_ATT: SCHEMA_ID},
        )
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is datetime.datetime:
        res = cast(
            JSONSchema,
            {
                JSC_TYPE: JSC_STRING,
                JSC_TITLE: JSC_TITLE_DATETIME,
                SCHEMA_ATT: SCHEMA_ID,
            },
        )
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is bytes:
        res = SCHEMA_BYTES
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if T is object:
        res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, JSC_TITLE: "object"})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    # we cannot use isinstance on typing.Any
    if is_Any(T):  # XXX not possible...
        res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, JSC_TITLE: "Any"})
        res = sorted_dict_cbor_ord(res)
        return TRE(res)

    if is_Union(T):
        return ipce_from_typelike_Union(T, c=c, ieso=ieso)

    if is_Optional(T):
        return ipce_from_typelike_Optional(T, c=c, ieso=ieso)

    if is_DictLike(T):
        T = cast(Type[Dict], T)
        return ipce_from_typelike_DictLike(T, c=c, ieso=ieso)

    if is_SetLike(T):
        T = cast(Type[Set], T)
        return ipce_from_typelike_SetLike(T, c=c, ieso=ieso)

    if is_Intersection(T):
        return ipce_from_typelike_Intersection(T, c=c, ieso=ieso)

    if is_Callable(T):
        return ipce_from_typelike_Callable(T, c=c, ieso=ieso)

    if is_NewType(T):
        return ipce_from_typelike_NewType(T, c=c, ieso=ieso)

    if is_Sequence(T):
        msg = "Translating Sequence into List"
        warnings.warn(msg)
        T = cast(Type[Sequence], T)
        # raise ValueError(msg)
        V = get_Sequence_arg(T)
        T = List[V]
        return ipce_from_typelike_ListLike(T, c=c, ieso=ieso)

    if is_ListLike(T):
        T = cast(Type[List], T)
        return ipce_from_typelike_ListLike(T, c=c, ieso=ieso)

    if is_TupleLike(T):
        # noinspection PyTypeChecker
        return ipce_from_typelike_TupleLike(T, c=c, ieso=ieso)

    if is_Type(T):
        TT = get_Type_arg(T)
        r = ipce_from_typelike_tr(TT, c, ieso=ieso)
        res = cast(
            JSONSchema,
            {SCHEMA_ATT: SCHEMA_ID, JSC_TYPE: "subtype", "subtype": r.schema},
        )
        res = sorted_dict_cbor_ord(res)
        return TRE(res, r.used)
        # raise NotImplementedError(T)

    assert isinstance(T, type), (T, type(T), is_Optional(T), is_Union(T))

    if is_dataclass(T):
        return ipce_from_typelike_dataclass(T, c=c, ieso=ieso)

    if T is np.ndarray:
        return ipce_from_typelike_ndarray()

    msg = "Cannot interpret the type @T"
    raise ZValueError(msg, T=T, c=c)


def ipce_from_typelike_ndarray() -> TRE:
    res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID})
    res[JSC_TYPE] = JSC_OBJECT
    res[JSC_TITLE] = JSC_TITLE_NUMPY
    properties = {"shape": {}, "dtype": {}, "data": SCHEMA_BYTES}  # TODO  # TODO
    properties = sorted_dict_cbor_ord(properties)
    res[JSC_PROPERTIES] = properties
    res = sorted_dict_cbor_ord(res)
    return TRE(res)


def ipce_from_typelike_slice(ieso: IESO) -> TRE:
    res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID})
    res[JSC_TYPE] = JSC_OBJECT
    res[JSC_TITLE] = JSC_TITLE_SLICE
    c = IFTContext({}, {}, ())
    tr = ipce_from_typelike_tr(Optional[int], c=c, ieso=ieso)
    properties = {
        "start": tr.schema,  # TODO
        "stop": tr.schema,  # TODO
        "step": tr.schema,
    }
    res[JSC_PROPERTIES] = sorted_dict_cbor_ord(properties)
    res = sorted_dict_cbor_ord(res)
    return TRE(res, tr.used)


def ipce_from_typelike_Intersection(T: TypeLike, c: IFTContext, ieso: IESO):
    args = get_Intersection_args(T)
    kt = KeepTrackSer(c, ieso)

    options = [kt.ipce_from_typelike(t) for t in args]
    res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, ALL_OF: options})
    res = sorted_dict_cbor_ord(res)
    return kt.tre(res)


def get_mentioned_names(T: TypeLike, context=()) -> Iterator[str]:
    if T in context:
        return
    c2 = context + (T,)
    if is_dataclass(T):
        if context:
            yield T.__name__
        annotations = getattr(T, "__annotations__", {})
        for v in annotations.values():
            yield from get_mentioned_names(v, c2)
    elif is_Type(T):
        v = get_Type_arg(T)
        yield from get_mentioned_names(v, c2)
    elif is_TypeVar(T):
        yield get_TypeVar_name(T)

    elif is_FixedTupleLike(T):
        for t in get_FixedTupleLike_args(T):
            yield from get_mentioned_names(t, c2)
    elif is_VarTuple(T):
        t = get_VarTuple_arg(T)
        yield from get_mentioned_names(t, c2)
    elif is_ListLike(T):
        T = cast(Type[List], T)
        t = get_ListLike_arg(T)
        yield from get_mentioned_names(t, c2)

    elif is_DictLike(T):
        T = cast(Type[Dict], T)
        K, V = get_DictLike_args(T)
        yield from get_mentioned_names(K, c2)
        yield from get_mentioned_names(V, c2)
    elif is_SetLike(T):
        T = cast(Type[Set], T)
        t = get_SetLike_arg(T)
        yield from get_mentioned_names(t, c2)

    elif is_ForwardRef(T):
        return get_ForwardRef_arg(T)

    elif is_Optional(T):

        t = get_Optional_arg(T)
        yield from get_mentioned_names(t, c2)

    elif is_Union(T):
        for t in get_Union_args(T):
            yield from get_mentioned_names(t, c2)
    else:
        pass


def ipce_from_typelike_dataclass(T: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    assert is_dataclass(T), T

    # noinspection PyDataclass
    c = replace(
        c,
        globals_=dict(c.globals_),
        processing=dict(c.processing),
        context=c.context + (T.__name__,),
    )

    used = {}

    def ftl(x: TypeLike) -> JSONSchema:
        if not is_TypeLike(x):
            raise ValueError(x)
        tr = ipce_from_typelike_tr(x, c=c, ieso=ieso)
        used.update(tr.used)
        return tr.schema

    def fob(x: object) -> IPCE:
        return ipce_from_object(x, globals_=c.globals_, ieso=ieso)

    def f(x: object) -> IPCE:
        if is_TypeLike(x):
            x = cast(TypeLike, x)
            return ftl(x)
        else:
            return fob(x)

    res = cast(JSONSchema, {})

    mentioned = set(get_mentioned_names(T, ()))
    relevant = [x for x in c.context if x in mentioned and x != T.__name__]
    relevant.append(T.__qualname__)
    url_name = "_".join(relevant)
    my_ref = make_url(url_name)
    res[ID_ATT] = my_ref
    res[JSC_TITLE] = T.__name__
    c.processing[T.__name__] = my_ref

    res[ATT_PYTHON_NAME] = T.__qualname__
    res[X_PYTHON_MODULE_ATT] = T.__module__

    res[SCHEMA_ATT] = SCHEMA_ID

    res[JSC_TYPE] = JSC_OBJECT

    if hasattr(T, "__doc__") and T.__doc__:
        res[JSC_DESCRIPTION] = T.__doc__

    if hasattr(T, GENERIC_ATT2):
        definitions = {}
        types2 = getattr(T, GENERIC_ATT2)
        for t2 in types2:
            if not isinstance(t2, TypeVar):
                continue

            url = make_url(f"{T.__qualname__}/{t2.__name__}")

            c.processing[f"{t2.__name__}"] = url
            # noinspection PyTypeHints
            t2_name = get_TypeVar_name(t2)
            c.globals_[t2_name] = t2

            bound = get_TypeVar_bound(t2)
            # bound = t2.__bound__ or object
            schema = ftl(bound)
            schema = copy.copy(schema)
            schema[ID_ATT] = url
            schema = sorted_dict_cbor_ord(schema)
            definitions[t2.__name__] = schema

            c.globals_[t2.__name__] = t2

        if definitions:
            res[JSC_DEFINITIONS] = sorted_dict_cbor_ord(definitions)

    properties = {}
    classvars = {}
    classatts = {}

    required = []
    all_fields: Dict[str, Field] = get_fields_including_static(T)

    from .conv_ipce_from_object import ipce_from_object

    original_order = list(all_fields)
    ordered = sorted(all_fields)

    for name in ordered:
        afield = all_fields[name]

        t = afield.type

        try:
            if isinstance(t, str):  # pragma: no cover
                # t = eval_just_string(t, c.globals_)
                msg = "Before serialization, need to have all text references substituted."
                msg += f"\n found reference {t!r} in class {T}."
                raise Exception(msg)

            if is_ClassVar(t):
                tt = get_ClassVar_arg(t)
                # logger.info(f'ClassVar found : {tt}')
                if False and is_Type(tt):
                    u = get_Type_arg(tt)
                    if is_TypeVar(u):
                        tn = get_TypeVar_name(u)
                        if tn in c.processing:
                            ref = c.processing[tn]
                            schema = make_ref(ref)
                            classvars[name] = schema
                            used.update({tn: ref})
                            classatts[name] = ftl(type)
                        else:  # pragma: no cover
                            msg = "Unknown typevar @tn in class @T"
                            raise ZNotImplementedError(msg, tn=tn, T=T, c=c)
                    else:
                        classvars[name] = ftl(u)
                        try:
                            the_att = get_T_attribute(T, name)
                        except AttributeError:
                            pass
                        else:
                            classatts[name] = f(the_att)

                else:
                    classvars[name] = ftl(tt)
                    try:
                        the_att = get_T_attribute(T, name)
                    except AttributeError:
                        pass
                    else:
                        classatts[name] = f(the_att)

            else:  # not classvar
                schema = ftl(t)

                try:
                    default = get_field_default(afield)
                except KeyError:
                    required.append(name)
                else:
                    schema = make_schema_with_default(schema, default, c, ieso)
                properties[name] = schema

        except IPCE_PASS_THROUGH:  # pragma: no cover
            raise
        except BaseException as e:
            msg = "Cannot write schema for attribute @name -> @t of type @T."
            raise ZTypeError(msg, name=name, t=t, T=T) from e

    if required:  # empty is error
        res[JSC_REQUIRED] = sorted(required)
    if classvars:
        res[X_CLASSVARS] = classvars
    if classatts:
        res[X_CLASSATTS] = classatts

    assert len(classvars) >= len(classatts), (classvars, classatts)

    if properties:
        res[JSC_PROPERTIES] = sorted_dict_cbor_ord(properties)

    res[X_ORDER] = original_order
    if sorted_dict_cbor_ord:
        res = sorted_dict_cbor_ord(res)

    if T.__name__ in used:
        used.pop(T.__name__)
    return TRE(res, used)


def get_T_attribute(T: TypeLike, n: str) -> object:
    if hasattr(T, n):
        # special case
        the_att2 = getattr(T, n)
        if isinstance(the_att2, Field):
            # actually attribute not there
            raise AttributeError()
        else:
            return the_att2
    else:
        raise AttributeError()


def make_schema_with_default(
    schema: JSONSchema, default: object, c: IFTContext, ieso: IESO
) -> JSONSchema:
    from zuper_ipce import ipce_from_object

    options = [schema]
    s_u_one = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, ANY_OF: options})

    ipce_default = ipce_from_object(default, globals_=c.globals_, ieso=ieso)
    s_u_one["default"] = ipce_default
    s_u_one = sorted_dict_cbor_ord(s_u_one)
    return s_u_one


from dataclasses import MISSING


def get_field_default(f: Field) -> object:
    if f.default != MISSING:
        return f.default
    elif f.default_factory != MISSING:
        return f.default_factory()
    else:
        raise KeyError("no default")


def ipce_from_typelike_Union(t: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    types = get_Union_args(t)
    used = {}

    def f(x: TypeLike) -> JSONSchema:
        tr = ipce_from_typelike_tr(x, c=c, ieso=ieso)
        used.update(tr.used)
        return tr.schema

    options = [f(t) for t in types]
    res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, ANY_OF: options})
    res = sorted_dict_cbor_ord(res)
    return TRE(res, used)


def ipce_from_typelike_Optional(t: TypeLike, c: IFTContext, ieso: IESO) -> TRE:
    types = [get_Optional_arg(t), type(None)]
    kt = KeepTrackSer(c, ieso)

    options = [kt.ipce_from_typelike(t) for t in types]
    res = cast(JSONSchema, {SCHEMA_ATT: SCHEMA_ID, ANY_OF: options})
    res = sorted_dict_cbor_ord(res)
    return kt.tre(res)


#
# def ipce_from_typelike_generic(T: Type, globals_: GlobalsDict, processing_: ProcessingDict) -> JSONSchema:
#     assert hasattr(T, GENERIC_ATT2)
#
#     types2 = getattr(T, GENERIC_ATT2)
#     processing2 = dict(processing_)
#     globals2 = dict(globals_)
#
#     res = cast(JSONSchema, {})
#     res[SCHEMA_ATT] = SCHEMA_ID
#
#     res[JSC_TITLE] = T.__name__
#     # res[ATT_PYTHON_NAME] = T.__qualname__
#     res[X_PYTHON_MODULE_ATT] = T.__module__
#
#     res[ID_ATT] = make_url(T.__name__)
#
#     res[JSC_TYPE] = JSC_OBJECT
#
#     processing2[f'{T.__name__}'] = make_ref(res[ID_ATT])
#
#     # print(f'T: {T.__name__} ')
#     definitions = {}
#
#     if hasattr(T, '__doc__') and T.__doc__:
#         res[JSC_DESCRIPTION] = T.__doc__
#     globals_ = dict(globals_)
#     for t2 in types2:
#         if not isinstance(t2, TypeVar):
#             continue
#
#         url = make_url(f'{T.__name__}/{t2.__name__}')
#
#         # processing2[f'~{name}'] = {'$ref': url}
#         processing2[f'{t2.__name__}'] = make_ref(url)
#         # noinspection PyTypeHints
#         globals2[t2.__name__] = t2
#
#         bound = t2.__bound__ or Any
#         schema = ipce_from_typelike(bound, globals2, processing2)
#         schema = copy.copy(schema)
#         schema[ID_ATT] = url
#
#         definitions[t2.__name__] = schema
#
#         globals_[t2.__name__] = t2
#
#     if definitions:
#         res[JSC_DEFINITIONS] = definitions
#     properties = {}
#     required = []
#
#     # names = list(T.__annotations__)
#     # ordered = sorted(names)
#     original_order = []
#     for name, t in T.__annotations__.items():
#         t = replace_typevars(t, bindings={}, symbols=globals_, rl=None)
#         if is_ClassVar(t):
#             continue
#         try:
#             result = eval_field(t, globals2, processing2)
#         except PASS_THROUGH:
#             raise
#         except BaseException as e:
#             msg = f'Cannot evaluate field "{name}" of class {T} annotated as {t}'
#             raise Exception(msg) from e
#         assert isinstance(result, Result), result
#         properties[name] = result.schema
#         original_order.append(name)
#         if not result.optional:
#             required.append(name)
#     if required:
#         res[JSC_REQUIRED] = sorted(required)
#
#     sorted_vars = sorted(original_order)
#     res[JSC_PROPERTIES] = {k: properties[k] for k in sorted_vars}
#     res['order'] = original_order
#     res = sorted_dict_with_cbor_ordering(res)
#     return res

# @dataclasses.dataclass
# class Result:
#     tre: TRE
#     optional: Optional[bool] = False
#
#     def __post_init__(self):
#         assert isinstance(self.tre, TRE), self
#     #
#     # def __init__(self, tr: TRE, optional: bool = None):
#     #     self.schema = schema
#     #     self.optional = optional

#
# def eval_field(t, globals_: GlobalsDict, processing: ProcessingDict) -> Result:
#     debug_info2 = lambda: dict(globals_=globals_, processing=processing)
#
#     c = IFTContext(globals_=globals_, processing=processing, context=())
#     if isinstance(t, str):
#         te = eval_type_string(t, globals_, processing)
#         return te
#
#     if is_Type(t):
#         res = cast(JSONSchema, make_ref(SCHEMA_ID))
#         return Result(TRE(res))
#
#     if is_TupleLike(t):
#         tr = ipce_from_typelike_TupleLike(t, c)
#         return Result(tr)
#
#     if is_ListLike(t):
#         tr = ipce_from_typelike_ListLike(t, c)
#         return Result(tr)
#
#     if is_DictLike(t):
#         tr = ipce_from_typelike_dict(t, c)
#         return Result(tr)
#
#     if is_SetLike(t):
#         tr = ipce_from_typelike_SetLike(t, c)
#         return Result(tr)
#
#     if is_ForwardRef(t):
#         tn = get_ForwardRef_arg(t)
#         return eval_type_string(tn, globals_, processing)
#
#     if is_Optional(t):
#         tt = get_Optional_arg(t)
#         result = eval_field(tt, globals_, processing)
#         return Result(result.tre, optional=True)
#
#     if is_Union(t):
#         return Result(ipce_from_typelike_Union(t, c))
#
#     if is_Any(t):
#         res = cast(JSONSchema, {'$schema': 'http://json-schema.org/draft-07/schema#'})
#         return Result(TRE(res))
#
#     if isinstance(t, TypeVar):
#         l = t.__name__
#         if l in processing:
#             ref = processing[l]
#             schema = make_ref(ref)
#             return Result(TRE(schema, {l: ref}))
#         # I am not sure why this is different in Python 3.6
#         if PYTHON_36 and (l in globals_):  # pragma: no cover
#             T = globals_[l]
#             tr = ipce_from_typelike_tr(T, c)
#             return Result(tr)
#
#         m = f'Could not resolve the TypeVar {t}'
#         msg = pretty_dict(m, debug_info2())
#         raise CannotResolveTypeVar(msg)
#
#     if isinstance(t, type):
#         # catch recursion here
#         if t.__name__ in processing:
#             return eval_field(t.__name__, globals_, processing)
#         else:
#             tr = ipce_from_typelike_tr(t, c)
#             return Result(tr)
#
#     msg = f'Could not deal with {t}'
#     msg += f'\nglobals: {globals_}'
#     msg += f'\nprocessing: {processing}'
#     raise NotImplementedError(msg)

#
# def eval_type_string(t: str, globals_: GlobalsDict, processing: ProcessingDict) -> Result:
#     check_isinstance(t, str)
#     globals2 = dict(globals_)
#     debug_info = lambda: dict(t=t, globals2=pretty_dict("", globals2), processing=pretty_dict("", processing))
#
#     if t in processing:
#         url = make_url(t)
#         schema: JSONSchema = make_ref(url)
#         return Result(TRE(schema, {t: url}))  # XXX not sure
#
#     elif t in globals2:
#         return eval_field(globals2[t], globals2, processing)
#     else:
#         try:
#             res = eval_just_string(t, globals2)
#             return eval_field(res, globals2, processing)
#         except NotImplementedError as e:  # pragma: no cover
#             m = 'While evaluating string'
#             msg = pretty_dict(m, debug_info())
#             raise NotImplementedError(msg) from e
#         except PASS_THROUGH:
#             raise
#         except BaseException as e:  # pragma: no cover
#             m = 'Could not evaluate type string'
#             msg = pretty_dict(m, debug_info())
#             raise ValueError(msg) from e
#
#
# def eval_just_string(t: str, globals_):
#     from typing import Optional
#     eval_locals = {
#           'Optional': Optional, 'List': List,
#           'Dict':     Dict, 'Union': Union, 'Set': typing.Set, 'Any': Any
#           }
#     # TODO: put more above?
#     # do not pollute environment
#     if t in globals_:
#         return globals_[t]
#     eval_globals = dict(globals_)
#     try:
#         res = eval(t, eval_globals, eval_locals)
#         return res
#     except PASS_THROUGH:
#         raise
#     except BaseException as e:
#         m = f'Error while evaluating the string {t!r} using eval().'
#         msg = pretty_dict(m, dict(eval_locals=eval_locals, eval_globals=eval_globals))
#         raise type(e)(msg) from e
