from django.core.files.uploadhandler import (FileUploadHandler, 
                                            StopFutureHandlers, StopUpload)
from django.core.cache import cache
import time

class UploadLimitSizeHandler(FileUploadHandler):
    def handle_raw_input(self, input_data, META, content_length, boundary, encoding=None):
        if content_length > 10000000:
            if 'X-Progress-ID' in self.request.GET :
                self.progress_id = self.request.GET['X-Progress-ID']
            elif 'X-Progress-ID' in self.request.META:
                self.progress_id = self.request.META['X-Progress-ID']
        
            if self.progress_id:
                self.cache_key = "%s_%s" % (self.request.META['REMOTE_ADDR'], 
                                            self.progress_id )

                cache.set(self.cache_key, {
                    'failed': 'yes',
                })
            raise StopUpload(connection_reset=True)

    def receive_data_chunk(self, raw_data, start):
        # time.sleep(1)
        return raw_data
        
    def file_complete(self, file_size):
        pass
