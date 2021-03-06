import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer


class KarvePlateExtractor(BaseNameExtractor):
    """
    From a given comment, if it's a Karve CB then extract the plate used if possible
    """

    oc_re = re.compile(r'\sOC[\s$)]', re.IGNORECASE)
    plate_re = re.compile(r'[\s(\-]([A-G](?<=A)*)(?:$|\s|-plate|\))', re.IGNORECASE)

    @cached_property
    def alternative_namer(self):
        return RazorAlternateNamer()

    @cached_property
    def detect_regexps(self):
        razor_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(r'^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)'.format(razor_name_re),
                       re.MULTILINE | re.IGNORECASE),  # TTS and similar
            re.compile(r'\*Razor\*:.*\*\*([{0}]+)\*\*'.format(razor_name_re), re.MULTILINE | re.IGNORECASE),  # sgrddy
            re.compile(r'^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]'.format(razor_name_re),
                       re.MULTILINE | re.IGNORECASE),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant

        ]


    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        extracted_name = None

        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            # catch case where some jerk writes ❧ Razor and Blade Notes or similar
            # at some point this can be genericised in to a block words / phrases list to catch razorock too
            if res and 'and blade note' in res.group(1).lower():
                continue

            # catch case where we match against razorock
            if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == 'ock'):
                extracted_name = res.group(1)

        if not extracted_name or not self.alternative_namer.get_principal_name(extracted_name) == 'Karve CB':
            return None

        # extract plate from name
        try:
            plate = self.plate_re.search(extracted_name).group(1)
        except AttributeError:
            return None

        # determine OC / SB
        sb_oc = 'OC' if self.oc_re.search(extracted_name) else 'SB'

        return '{0} {1}'.format(plate, sb_oc)


