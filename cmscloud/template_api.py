from django.utils.safestring import mark_safe


class Registry(object):
    def __init__(self):
        self.head = []
        self.tail = []
        
    def add_to_head(self, content):
        self.head.append(content)
    
    def add_to_tail(self, content):
        self.tail.append(content)
        
    def render_head(self):
        return self._render(self.head)
        
    def render_tail(self):
        return self._render(self.tail)

    def _render(self, data):
        return mark_safe('\n'.join(data))
    
    def template_processor(self, request):
        return {'TEMPLATE_API_REGISTRY': self}

registry = Registry()
template_processor = registry.template_processor
