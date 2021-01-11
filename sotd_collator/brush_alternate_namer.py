import copy
import re
from collections import OrderedDict
from functools import lru_cache, cached_property
from pprint import pprint

from sotd_collator.base_alternate_namer import BaseAlternateNamer


class BrushAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    bads = '(hmw|high.*mo|(2|3)band|shd|badger|silvertip|gelo|bulb|fan|finest|best|two\s*band)'
    boars = '(boar)'
    horses = '(horse)'
    syns = '(timber|tux|mew|silk|synt|synbad|2bed|captain|cashmere|faux.*horse|black.*(mag|wolf)|g4|boss)'

    apply_first = {
        'DG B1': ['B1(\s|$)'],
        'DG B2': ['B2'],
        'DG B3': ['B3'],
        'DG B4': ['B4'],
        'DG B5': ['B5'],
        'DG B6': ['B6'],
        'DG B7': ['B7'],
        'DG B8': ['B8'],
        'DG B9A+': ['B9A\+', 'b9.*alpha.*plus'],
        'DG B9A': ['B9A', 'b9.*alpha'],
        'DG B9B': ['B9B', 'b9.*bravo'],
        'DG B10': ['b10'],
        'Stirling Synthetic': ['stirl.*kong'],
        'r/wetshaving Semogue Brushbutt Boar': ['brushbutt'],
        'Omega Boar (model not specified)': ['^omega\s*boar$'],
        'Semogue Boar (model not specified)': ['^semogue\s*boar$'],
        'Hand Lather': ['^\s*hands*\s*$', 'hand.*lather'],
    }

    standard_makers = {
        'Alpha': {'patterns': ['alpha'], 'default': 'Synthetic'},
        'Anbbas': {'patterns': ['anbbas'], 'default': 'Synthetic'},
        'AP Shave Co': {'patterns': ['AP\s*shav'], 'default': 'Synthetic'},
        'Art of Shaving': {'patterns': ['^\s*aos', 'art.*of.*sha'], 'default': 'Badger'},
        'B&M': {'patterns': ['b\s*(&|a)\s*m', 'barrister'], 'default': 'Synthetic'},
        'Beaumont': {'patterns': ['bea.{1,3}mont'], 'default': 'Badger'},
        'Black Anvil': {'patterns': ['black.*anv'], 'default': 'Badger'},
        'Brad Sears': {'patterns': ['brad.*sears'], 'default': 'Badger'},
        'Bristle Brushwerks': {'patterns': ['huck', 'bristle.*brush'], 'default': 'Badger'},
        'Brushcraft': {'patterns': ['brushcraft'], 'default': 'Synthetic'},
        'Carnavis & Richardson': {'patterns': ['carn.*rich'], 'default': 'Synthetic'},
        'Catalin': {'patterns': ['catalin'], 'default': 'Badger'},
        'CaYuen': {'patterns': ['cayuen'], 'default': 'Synthetic'},
        'Craving Shaving': {'patterns': ['crav.*shav'], 'default': 'Synthetic'},
        'Cremo': {'patterns': ['cremo'], 'default': 'Horse'},
        'Crescent City Craftsman': {'patterns': ['cres.*city'], 'default': 'Synthetic'},
        'Declaration (Batch not Specified)': {'patterns': ['declaration'], 'default': 'Badger'},
        'DSCosmetics': {'patterns': ['DS\s*Cosmetic', 'DSC'], 'default': 'Synthetic'},
        'Dogwood': {'patterns': ['dogw', 'dogc*l', '^voa'], 'default': 'Badger'},
        'Doug Korn': {'patterns': ['doug\s*korn'], 'default': 'Badger'},
        'Dubl Duck': {'patterns': ['dubl.*duck'], 'default': 'Boar'},
        'Edwin Jagger': {'patterns': ['edwin.*jag'], 'default': 'Badger'},
        'El Druida': {'patterns': ['druida'], 'default': 'Badger'},
        'Elite': {'patterns': ['elite'], 'default': 'Badger'},
        'Erskine': {'patterns': ['erskine'], 'default': 'Boar'},
        'Ever Ready': {'patterns': ['ever.*read'], 'default': 'Badger'},
        'Executive Shaving': {'patterns': ['execut.*shav'], 'default': 'Synthetic'},
        'Fine': {'patterns': ['fine\s'], 'default': 'Synthetic'},
        'Firehouse Potter': {'patterns': ['fireh.*pott'], 'default': 'Synthetic'},
        'Fendrihan': {'patterns': ['fendri'], 'default': 'Badger'},
        'Frank Shaving': {'patterns': ['frank.*sha'], 'default': 'Synthetic'},
        'Geo F. Trumper': {'patterns': ['geo.*trumper'], 'default': 'Badger'},
        'Grizzly Bay': {'patterns': ['griz.*bay'], 'default': 'Badger'},
        'Haircut & Shave Co': {'patterns': ['haircut.*shave'], 'default': 'Badger'},
        'Heritage Collection': {'patterns': ['heritage'], 'default': 'Badger'},
        'L\'Occitane en Provence': {'patterns': ['oc*citane'], 'default': 'Synthetic'},
        'Lancaster Brushworks': {'patterns': ['lancaster'], 'default': 'Synthetic'},
        'Leonidam': {'patterns': ['leonidam', 'leo.*nem'], 'default': 'Badger'},
        'Liojuny Shaving': {'patterns': ['liojuny'], 'default': 'Synthetic'},
        'Lutin Brushworks': {'patterns': ['lutin'], 'default': 'Synthetic'},
        'Maggard': {'patterns': ['maggard'], 'default': 'Synthetic'},
        'Maseto': {'patterns': ['maseto'], 'default': 'Badger'},
        'Mojo': {'patterns': ['mojo'], 'default': 'Badger'},
        'Mondial': {'patterns': ['mondial'], 'default': 'Boar'},
        'Morris & Forndran': {'patterns': ['morris', 'm\s*&\s*f'], 'default': 'Badger'},
        'Mozingo': {'patterns': ['mozingo'], 'default': 'Badger'},
        'Muhle': {'patterns': ['muhle'], 'default': 'Badger'},
        'Mutiny': {'patterns': ['mutiny'], 'default': 'Synthetic'},
        'Noble Otter': {'patterns': ['noble', 'no\s*\d{2}mm'], 'default': 'Badger'},
        'NY Shave Co': {'patterns': ['ny\s.*shave.*co'], 'default': 'Badger'},
        'Omega EVO': {'patterns': ['omega.*evo', 'evo.*omega'], 'default': 'Synthetic'},
        'Oumo': {'patterns': ['oumo'], 'default': 'Badger'},
        'Oz Shaving': {'patterns': ['oz.*sha'], 'default': 'Synthetic'},
        'PAA': {'patterns': ['paa'], 'default': 'Synthetic'},
        'Paladin': {'patterns': ['paladin'], 'default': 'Badger'},
        'Parker': {'patterns': ['parker'], 'default': 'Badger'},
        'Plisson': {'patterns': ['plisson'], 'default': 'Badger'},
        'Prometheus Handcrafts': {'patterns': ['promethe'], 'default': 'Synthetic'},
        'Razorock': {'patterns': ['Razorr*ock', '(^|\s)rr\s', 'plissoft', 'razor rock'], 'default': 'Synthetic'},
        'Rubberset': {'patterns': ['rubberset'], 'default': 'Badger'},
        'Rudy Vey': {'patterns': ['rudy.*vey'], 'default': 'Badger'},
        'Rick Montalvo': {'patterns': ['montalv'], 'default': 'Synthetic'},
        'Sawdust Creation Studios': {'patterns': ['sawdust'], 'default': 'Synthetic'},
        'Semogue Owners Club': {'patterns': ['SOC', 'sem.*owner.*club'], 'default': 'Boar'},
        'Shavemac': {'patterns': ['shavemac'], 'default': 'Badger'},
        'Shore Shaving': {'patterns': ['shore.*shav'], 'default': 'Synthetic'},
        'Simpson': {'patterns': ['simpson', 'duke', 'chubby.*2'], 'default': 'Badger'},
        'Some Making Required': {'patterns': ['some.*maki'], 'default': 'Synthetic'},
        'Spiffo': {'patterns': ['spiffo'], 'default': 'Badger'},
        'Stirling': {'patterns': ['stirl'], 'default': 'Badger'},
        'Strike Gold Shave': {'patterns': ['strike.*gold'], 'default': 'Synthetic'},
        'Supply': {'patterns': ['supply'], 'default': 'Synthetic'},
        'Teton Shaves': {'patterns': ['teton'], 'default': 'Badger'},
        'The Bluebeard\'s Revenge': {'patterns': ['bluebeard.*rev'], 'default': 'Synthetic'},
        'The Holy Black': {'patterns': ['tgn', 'golden.*nib'], 'default': 'Synthetic'},
        'The Golden Nib': {'patterns': ['tgn', 'golden.*nib'], 'default': 'Boar'},
        'The Varlet': {'patterns': ['varlet'], 'default': 'Badger'},
        'Tony Forsyth': {'patterns': ['tony.*fors'], 'default': 'Badger'},
        'That Darn Rob': {'patterns': ['darn.*rob', 'tdr'], 'default': 'Badger'},
        'Thater': {'patterns': ['thater'], 'default': 'Badger'},
        'TOBS': {'patterns': ['tobs', 'taylor.*bond'], 'default': 'Badger'},
        'Turn-N-Shave': {'patterns': ['turn.{1,5}shave', 'tns'], 'default': 'Badger'},
        'Vie Long': {'patterns': ['vie.*long'], 'default': 'Horse'},
        'Viking': {'patterns': ['viking'], 'default': 'Badger'},
        'Vintage Blades': {'patterns': ['vintage.*blades'], 'default': 'Badger'},
        'Virginia Cheng': {'patterns': ['virginia.*cheng'], 'default': 'Badger'},
        'WCS': {'patterns': ['wcs', 'west.*coast'], 'default': 'Synthetic'},
        'Whipped Dog': {'patterns': ['whipped.*dog'], 'default': 'Badger'},
        'Wolf Whiskers': {'patterns': ['wolf.*whis'], 'default': 'Badger'},
        'Wild West Brushworks': {'patterns': ['wild.*west', 'wwb', 'ww.*brushw'], 'default': 'Synthetic'},
        'Yaqi': {'patterns': ['yaqu*i'], 'default': 'Synthetic'},
        'Zenith': {'patterns': ['zenith'], 'default': 'Boar'},
    }

    standard_fixup = {
            '{0} Badger': bads,
            '{0} Boar': boars,
            '{0} Synthetic': syns,
            '{0} Horse': horses,
            # default to maker default
            '{0} {1}': '',
    }

    @cached_property
    def _raw(self):
        raw = {}
        # for most makers just split them out into badger, boar and synthetic knots
        for maker, data in self.standard_makers.items():
            for regexp in data['patterns']:
                for maker_name_template, pattern in self.standard_fixup.items():
                    maker_name = maker_name_template.format(maker, data['default'])
                    if maker_name in raw:
                        raw[maker_name].append(regexp + '.*' + pattern)
                    else:
                        raw[maker_name] = [regexp + '.*' + pattern]
        return raw

    @lru_cache(maxsize=1024)
    def get_principal_name(self, name):
        # Standardise omega / semogues - dont want to list out every model number above,
        # but coerce them into a standard format
        name = name.lower().replace('semouge', 'semogue')

        omse_brand = re.search('(omega|semogue)', name, re.IGNORECASE)
        omse_model_num = re.search('[A-Za-z]*\d{3,}', name)
        if omse_brand and omse_model_num:
            return '{0} {1}'.format(
                omse_brand.group(1).title(),
                omse_model_num.group(0)
            )

        #initial regexs (Dec batches etc - apply first because they are short matches and otherwise would be applied last)
        for brush_name in sorted(self.apply_first.keys(), key=len, reverse=True):
            for pattern in self.apply_first[brush_name]:
                if re.search(pattern, name, re.IGNORECASE):
                    return brush_name

        # fall down to standard makers
        for alt_name_re in sorted(self._mapper.keys(), key=len, reverse=True):
            if re.search(alt_name_re, name, re.IGNORECASE):
                return self._mapper[alt_name_re]
        return None


if __name__ == '__main__':
    print(BrushAlternateNamer().get_principal_name(name='TOBS Pure Badger'))