from django.views.decorators.http import require_http_methods

def get(model, request, *args):
    fieldmap = getFieldMap(*args)
    where_condition = where(request, fieldmap)
    sort_by = sortby(request, fieldmap)
    lim = limit(request)
    Q0 = model.objects.filter(**where_condition)
    if sort_by:
        Q0 = Q0.order_by(sort_by)
    if 0 < lim:
        Q0 = Q0[:lim]
    return prepareResult(request, model, fieldmap, Q0)

def add(model, request, *args):
    fieldmap = getFieldMap(*args)
    columns = getPostValueList(model, request, *args)
    Q = model(**columns)
    Q.save()
    return prepareResult(request, model, fieldmap, [Q])[0]

def edit(model, request, *args):
    fieldmap = getFieldMap(*args)
    where_condition = where(request, fieldmap)
    Q0 = model.objects.filter(**where_condition)
    Q = Q0[0]
    columns = getPostValueList(model, request, *args)
    for key in columns.keys():
        Q.key = columns[key]
    Q.save()
    return prepareResult(request, model, fieldmap, [Q])[0]

def delete(model, request, *args):
    fieldmap = getFieldMap(*args)
    where_condition = where(request, fieldmap)
    Q = model.objects.filter(**where_condition)
    Q.delete()
    return []

def getFieldMap(*args):
    fieldmap = {}
    if len(args):
        fieldmap.update(args[0])
    return fieldmap
    
def prepareResult(request, model, fieldmap, result):
    fieldset = fields(request, fieldmap, model)
    realfieldset = fields(request, {}, model)
    output = []
    for i in result:
        item = {}
        for j in range(len(fieldset)):
            item[realfieldset[j]] = str(getattr(i, fieldset[j]))
        output.append(item)
    return output

def getMappedPostKeys(fieldmap, values):
    for pos in range(len(values)):
        if values[pos] in fieldmap.keys():
            values[pos] = fieldmap[values[pos]]
    return values
        
def getMappedModelKeys(fieldmap, values):
    for pos in range(len(values)):
        for key, val in fieldmap.items():
            if values[pos] == val:
                values[pos] = key
    return values
        
#@require_http_methods(["POST"])
def getPostListValue(request, key, *args):
    values=request.POST.getlist(key, [])
    if not len(values) and 1 < len(args):
            values = getModelFields(args[1])
    if len(args):
        values = getMappedModelKeys(args[0], values)
    return values

#@require_http_methods(["POST"])
def getPostValue(request, key, *args):
    value=request.POST.get(key, None)
    if len(args):
        value = getMappedModelKeys(args[0], [value])[:1]
    return value

def getPostValueList(model, request, *args):
    columns = {}
    modelfields = getModelFields(model)
    postfields = getModelFields(model, *args)
    for i in range(len(modelfields)):
        value = getPostValue(request, postfields[i])
        if value:
            columns[modelfields[i]] = value
    return columns

def fields(request, *args):
    return getPostListValue(request, "fields", *args)

def where(request, fieldmap):
    where_fields=getPostListValue(request, "where_fields", fieldmap)
    where_conditions=getPostListValue(request, "where_conditions")
    where_args=getPostListValue(request, "where_args")
    condition = {}
    for i in range(len(where_fields)):
        element = prepareSingleCondition(where_fields[i], where_conditions[i], where_args[i])
        condition.update(element)
    return condition

def sortby(request, *args):
    sort = getPostValue(request, "sortby")
    if not sort:
        return None
    elif "DESC" in sort:
        value = getMappedModelKeys(args[0], [sort.split()[0]])[:1]
        return "-{}".format(value)
    else:
        return getMappedModelKeys(args[0], [sort])[:1]

def limit(request):
    limit = getPostValue(request, "limit")
    if not limit:
        limit = -1
    return limit

def prepareSingleCondition(field, condition, value):
    if condition == "eq":
        return {"{}__eq".format(field):value}
    if condition == "lt":
        return {"{}__lt".format(field):value}
    if condition == "lte":
        return {"{}__lte".format(field):value}
    if condition == "gt":
        return {"{}__gt".format(field):value}
    if condition == "gte":
        return {"{}__gte".format(field):value}
    if condition == "ne":
        return {}#TODO implement this

def getModelFields(model, *args):
    fields = [ x.name for x in model._meta.fields ]   #TODO modify this
    if len(args):
        fields = getMappedPostKeys(args[0], fields)
    return fields
    