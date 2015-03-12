from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mixins import JsonResponseBase

class HTTPGetFormMixin(object):
    form_class = None
    _form = None
    
    def len_query_string(self):
        return len(self.request.GET)
        
    def get_form_kwargs(self):
        return {}
    
    def get_form_class(self):
        return self.form_class
    
    def get_form(self, form_class):
        if self._form:
            return self._form
        
        if self.len_query_string():
            self._form = form_class(self.request.GET, **self.get_form_kwargs())
        else:
            self._form = form_class(**self.get_form_kwargs())
        
        return self._form


class HTTPGetFormView(HTTPGetFormMixin, TemplateView, JsonResponseBase):
    http_method_names = ['get', 'options', 'trace', 'head']
    success_url = None
    
    def get_success_url(self):
        return self.success_url
    
    def form_valid(self, form):
        if self.request.is_ajax():
            reponse_d = {'valid': 1}
            return self.render_to_json_response(reponse_d, status=200)
        else:
            return HttpResponseRedirect(self.get_success_url())
        
    def form_invalid(self, form):
        if self.request.is_ajax():
            # status code need improvement
            return self.render_to_json_response(form.errors, status=200)
        else:
            return super(HTTPGetFormView, self).get(self.request, *self.args, **self.kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HTTPGetFormView, self).get_context_data(**kwargs)
        context['form'] = self._form
        return context
    
    def get(self, request, *args, **kwargs):
        self.get_form(self.get_form_class())
        
        if self._form.is_valid():
            return self.form_valid(self._form)
        else:
            return self.form_invalid(self._form)


class ListWithFormView(HTTPGetFormMixin, ListView):
    """
    Note this view doesn't validate the form. It only populates the form
    and display the queryset.
    
    """
    form = None
    
    def get_form(self, form_class):
        return self.form

    def dispatch(self, request, *args, **kwargs):
        self.get_form(self.get_form_class())
        return super(ListWithFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.get_form(self.get_form_class())
        context = super(ListWithFormView, self).get_context_data(**kwargs)
        
        if context.get('page_obj') and context['page_obj'].has_next():
            query_dict_next = self.request.GET.copy()
            query_dict_next['page'] = context['page_obj'].next_page_number()
            context['next_page_query'] = query_dict_next.urlencode()
        
        if context.get('page_obj') and context['page_obj'].has_previous():
            query_dict_pre = self.request.GET.copy()
            query_dict_pre['page'] = context['page_obj'].previous_page_number()
            context['pre_page_query'] = query_dict_pre.urlencode()
        
        return context
    
    def get_queryset(self):
        """This method may be overidden in child classes."""
        return self.form.get_file_list()
    
    
    
