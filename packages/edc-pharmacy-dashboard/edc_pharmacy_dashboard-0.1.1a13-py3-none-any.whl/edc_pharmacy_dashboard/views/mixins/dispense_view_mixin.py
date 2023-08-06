import re

from edc_constants.constants import UUID_PATTERN


class DispenseViewMixin:
    @property
    def selected_items(self):
        if not self._selected_items:
            for pk in self.request.POST.getlist(self.form_action_selected_items_name):
                if re.match(UUID_PATTERN, str(pk)):
                    self._selected_items.append(pk)
        return self._selected_items

    @property
    def dispenses(self):
        return self.selected_items
