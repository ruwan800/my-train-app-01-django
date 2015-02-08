from advanced.render import renderJSON, renderForm
from comment.models import Comment, saveComment
from advanced.user import getUser
from comment.forms import CommentForm
from reference.models import getReferenceByObject

def allComments(request):
    comments = Comment.objects.filter(user=getUser(request))
    return renderJSON(request, [{'ref':x.ref, 'dt':str(x.dt), 'text':x.text[:60]} for x in comments])

def view(request,ref):
    c = Comment.objects.get(ref=ref)
    return renderJSON(request, {'user':c.user.name, 'ref':getReferenceByObject(c.user), 'text':c.text, 'dt':str(c.dt)})

def write(request):
    if request.method == 'POST':
        msg = request.POST.get("text", None)
        target = request.POST.get("ref", "")
        formatted = [ x.partition(':')[::2] for x in target.split('_')]
        saveComment(request, msg, formatted)
        return renderJSON(request, {'success':True})
    else:
        return renderForm(request, None, CommentForm())