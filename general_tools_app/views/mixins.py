import json
from django.http import HttpResponse

class JsonResponseBase(object):
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        
        return HttpResponse(data, **response_kwargs)

class AjaxableResponseMixin(JsonResponseBase):

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

class AjaxDeletionMixin(JsonResponseBase):
        
    def delete(self, request, *args, **kwargs):
        response = super(AjaxDeletionMixin, self).delete(request, *args, **kwargs)
        if request.is_ajax():
            return HttpResponse('')
        else:
            return response

