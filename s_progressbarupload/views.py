from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError, Http404

import sys

def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    # print >> sys.stderr, "..upload progress view.."
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']

    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        
        if data:
            import json
            response = HttpResponse(json.dumps(data), content_type="application/json")
            if data.get('success') or data.get('failed'):
                cache.delete(cache_key)
            return response
        else:
            raise Http404
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

