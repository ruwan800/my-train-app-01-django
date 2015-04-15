from django.views.decorators.http import require_http_methods

WHERE_FIELDS = "where_fields"
WHERE_CONDITIONS = "where_conditions"
WHERE_ARGS = "where_args"


def get_where(request, field):
    where_fields = get_post_list_value(request, WHERE_FIELDS)
    where_conditions = get_post_list_value(request, WHERE_CONDITIONS)
    where_args = get_post_list_value(request, WHERE_ARGS)
    if field in where_fields:
        index = where_fields.index(field)
        return prepare_single_condition(where_fields[index], where_conditions[index], where_args[index])
    return None


def get(model, request, *args):
    field_map = get_field_map(*args)
    where_condition = where(request, field_map)
    sort_by_value = sort_by(request, field_map)
    lim = limit(request)
    q0 = model.objects.filter(**where_condition)
    if sort_by_value:
        q0 = q0.order_by(sort_by_value)
    if 0 < lim:
        q0 = q0[:lim]
    return q0


def add(model, request, *args):
    columns = get_post_value_list(model, request, *args)
    q = model(**columns)
    q.save()
    return q


def edit(model, request, *args):
    field_map = get_field_map(*args)
    where_condition = where(request, field_map)
    q0 = model.objects.filter(**where_condition)
    q = q0[0]
    columns = get_post_value_list(model, request, *args)
    for key in columns.keys():
        q.key = columns[key]
    q.save()
    return q


def delete(model, request, *args):
    field_map = get_field_map(*args)
    where_condition = where(request, field_map)
    q = model.objects.filter(**where_condition)
    q.delete()
    return []


def get_field_map(*args):
    field_map = {}
    if len(args):
        field_map.update(args[0])
    return field_map
    
# def prepareResult(request, model, fieldmap, result):
#     fieldset = fields(request, fieldmap, model)
#     realfieldset = fields(request, {}, model)
#     output = []
#     for i in result:
#         item = {}
#         for j in range(len(fieldset)):
#             item[realfieldset[j]] = str(getattr(i, fieldset[j]))
#         output.append(item)
#     return output


def get_mapped_post_keys(field_map, values):
    for pos in range(len(values)):
        if values[pos] in field_map.keys():
            values[pos] = field_map[values[pos]]
    return values


def get_mapped_model_keys(field_map, values):
    for pos in range(len(values)):
        for key, val in field_map.items():
            if values[pos] == val:
                values[pos] = key
    return values


@require_http_methods(["POST"])
def get_post_list_value(request, key, *args):
    values = request.POST.getlist(key, [])
    if not len(values) and 1 < len(args):
            values = get_model_fields(args[1])
    if len(args):
        values = get_mapped_model_keys(args[0], values)
    return values


@require_http_methods(["POST"])
def get_post_value(request, key, *args):
    value = request.POST.get(key, None)
    if len(args):
        value = get_mapped_model_keys(args[0], [value])[:1]
    return value


def get_post_value_list(model, request, *args):
    columns = {}
    model_fields = get_model_fields(model)
    post_fields = get_model_fields(model, *args)
    for i in range(len(model_fields)):
        value = get_post_value(request, post_fields[i])
        if value:
            columns[model_fields[i]] = value
    return columns


def fields(request, *args):
    return get_post_list_value(request, "fields", *args)


def where(request, field_map):
    where_fields = get_post_list_value(request, "where_fields", field_map)
    where_conditions = get_post_list_value(request, "where_conditions")
    where_args = get_post_list_value(request, "where_args")
    condition = {}
    for i in range(len(where_fields)):
        element = prepare_single_condition(where_fields[i], where_conditions[i], where_args[i])
        condition.update(element)
    return condition


def sort_by(request, *args):
    sort = get_post_value(request, "sortby")
    if not sort:
        return None
    elif "DESC" in sort:
        value = get_mapped_model_keys(args[0], [sort.split()[0]])[:1]
        return "-{}".format(value)
    else:
        return get_mapped_model_keys(args[0], [sort])[:1]


def limit(request):
    limit_value = get_post_value(request, "limit")
    if not limit_value:
        limit_value = -1
    return limit_value


def prepare_single_condition(field, condition, value):
    if condition == "eq":
        return {"{}__eq".format(field): value}
    if condition == "lt":
        return {"{}__lt".format(field): value}
    if condition == "lte":
        return {"{}__lte".format(field): value}
    if condition == "gt":
        return {"{}__gt".format(field): value}
    if condition == "gte":
        return {"{}__gte".format(field): value}
    if condition == "ne":
        return {}  # TODO implement this


def get_model_fields(model, *args):
    model_fields = [x.name for x in model._meta.fields]   # TODO modify this
    if len(args):
        model_fields = get_mapped_post_keys(args[0], model_fields)
    return model_fields
