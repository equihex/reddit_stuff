import re
from collections import OrderedDict
from functools import lru_cache

class AlternateRazorNames(object):
    """
    Amalgamate names
    """

    @property
    def all_razor_names(self):
        unique = set()
        for stub, variants in self._raw.items():
            unique.add(stub)
            unique.update(variants)

        return list(unique)

    @property
    @lru_cache(maxsize=1)
    def _mapper(self):
        output = {}
        for main_name, alternate_names in self._raw.items():
            for alternate_name in alternate_names:
                output[alternate_name] = main_name
        return output

    @lru_cache(maxsize=1024)
    def get_principal_name(self, name):
        for alt_name_re in sorted(self._mapper.keys(), key=len, reverse=True):
            if re.search(alt_name_re, name, re.IGNORECASE):
                return self._mapper[alt_name_re]
        return None


    _raw = OrderedDict({
        'Asylum Evolution': ['asylum.*evo'],
        'ATT H1': ['ATT.*h-*1*', 'tie.*h-*1*', '(atlas|bamboo|calypso|colossus|kronos).*h1*'],
        'ATT H2': ['ATT.*h-*2', 'tie.*h-*2', '(atlas|bamboo|calypso|colossus|kronos).*h2'],
        'ATT M1': ['ATT.*m-*1*', 'tie.*m-*1*', '(atlas|bamboo|calypso|colossus|kronos).*m1*'],
        'ATT M2': ['ATT.*m-*2', 'tie.*m-*2', '(atlas|bamboo|calypso|colossus|kronos).*m2'],
        'ATT R1': ['ATT.*r-*1*', 'tie.*r-*1*', '(atlas|bamboo|calypso|colossus|kronos).*r1*'],
        'ATT R2': ['ATT.*r-*2', 'tie.*r-*2', '(atlas|bamboo|calypso|colossus|kronos).*r2'],
        'ATT S1': ['ATT.*s-*1*', 'tie.*s-*1*', '(atlas|bamboo|calypso|colossus|kronos).*s1*'],
        'ATT S2': ['ATT.*s-*2', 'tie.*s-*2', '(atlas|bamboo|calypso|colossus|kronos).*s2'],
        'ATT SE1': ['ATT.*se-*1*', 'tie.*se-*1*', '(atlas|bamboo|calypso|colossus|kronos).*se1*'],
        'Baili BR1xx': ['(baili|BR).*(1|2)\d{2}'],
        'Bevel Razor': ['bevel'],
        'Blackland Blackbird': ['black\s*bird', 'bb\s*(sb|oc)', 'brassbird'],
        'Blackland Dart': ['(^|\s)dart'],
        'Blackland Sabre': ['sabre'],
        'Blackland Vector': ['vector'],
        'Boker Straight': ['Boker'],
        'Broman Razor': ['broman'],
        'Carbon Cx': ['carbon.*cx'],
        'Charcoal Goods Lvl 1': ['char.*l.*(1|one)', 'cg.*l.*1'],
        'Charcoal Goods Lvl 2': ['char.*l.*(2|two)', 'cg.*l.*2'],
        'Charcoal Goods Lvl 3': ['char.*l.*(3|three)', 'cg.*l.*(3|three)'],
        'Charcoal Goods Lithe Head': ['lithe'],
        'Cobra': ['cobra.*(clas|razor)', 'classic.*cobra', '^cobra$'],
        'Colonial General': ['col.*gener', 'general', 'colonial.*ac'],
        'Colonial Silversmith': ['silversmith'],
        'Crescent City Closed Comb 79': ['cres.*city.*79'],
        'Dorco ST-301': ['ST-*301'],
        'Dorco PL-602': ['pl-*602'],
        'Dovo Straight': ['dovo'],
        'Edwin Jagger DE89': ['DE\s*89', 'kelvin', 'edwi', '(de|ej)\s*8\d',],
        'Edwin Jagger 3one6': ['3.*one.*6'],
        'Ever Ready': ['ever.*ready', 'er\s*19', 'er.*streamline', '^streamline$'],
        'Fatip Grande': ['fa.*grande'],
        'Fatip Gentile': ['fa.*gentile', 'test.*genti.*'],
        'Fatip Picollo': ['fa.*picc*oll*o'],
        'Feather AS-D2': ['Feather.*as.*2', 'as-*d2'],
        'Feather Popular': ['Feather.*popular'],
        'Feather DX': ['Feather.*dx', 'feather.*artist.*club'],
        'Feather SS': ['feather.*ss'],
        'Fine Marvel': ['fine.*marvel'],
        'Fine Superlight Slant': ['superlight.*slant', 'fine.*slant'],
        'Filarmonica Straight': ['Filar*monica'],
        'Futur Clone': ['futur.*clone', 'Ming.*Shi.*(2000|adj)', 'qshave'],
        'GEM': ['GEM'],
        'Gillette Aristocrat': ['Aristocrat', 'Artisocrat'],
        'Gillette Diplomat': ['Diplomat'],
        'Gillette Fatboy': ['Fatboy', 'fat\s*boy'],
        'Gillette Goodwill': ['Gil.*et.*goodwill'],
        'Gillette Guard': ['Gil.*et.*guard'],
        'Gillette Heritage': ['Gil.*et.*heritage'],
        'Gillette Knack': ['Gil.*et.*knack'],
        'Gillette Milord': ['milord'],
        # gill.*new so that new.*improved is longer and gets evaluated first!
        'Gillette NEW': [
            'gil.*new',
            'bostonian',
            'new.*(s|l)c',
            'new.*(short|long).*comb',
            '(british|english).*new',
            'tuckaway',
            'new.*luxe',
            'rfb.*new',
            'new.*rfb',
            'gil.*et.*rfb',
            'bottom.*new',
            'big boy',
        ],
        'Gillette New Improved': ['new.*improved'],
        'Gillette Old Type': [
            'old.*type',
            'pocket.*ed',
            '(single|double).*ring',
            'big.*fellow',
            'gil.*et.*bulldog',
        ],
        'Gillette President': ['President'],
        'Gillette Senator': ['senator'],
        'Gillette Sheraton': ['sheraton'],
        'Gillette Slim': ['Gil.*Slim', 'slim.*adjust', '\d\d.*slim', 'slim.*\d', '^slim$'],
        'Gillette Super Adjustable': ['Black.*Beauty', 'Super.*adjust', 'gil.*et.*bb', 'super.*109'],
        'Gillette Superspeed': [
            'Super.*speed',
            '(red|black|blue|flare).*tip',
            'gillette.*tto(\W|$)',
            'gil.*ss',
            '\d\ds*\s*ss',
            'TV special',
            'gil.*rocket',
            'rocket.*hd',
        ],
        'Gillette Toggle': ['Toggle'],
        'Gillette Tech': ['Tech'],
        'Handlebar Shaving Company Dali': ['handlebar.*dali'],
        'Homelike START': ['Homelike.*start'],
        'iKon 101': ['ikon.*101'],
        'iKon 102': ['ikon.*102'],
        'iKon 103': ['ikon.*103'],
        'iKon B1': ['ikon.*b1'],
        'iKon SBS': ['ikon.*sbs'],
        'iKon X3': ['ikon.*x3'],
        'Karve CB': ['Karve', 'christopher.*brad'],
        'Kai Captain Kamisori': ['Kai.*captain.*kami'],
        'Koraat Straight': ['Koraat'],
        'Lady Gillette': ['lady.*gil.*et', 'gil.*et.*lady'],
        'LASSCo BBS-1': ['BBS-*1'],
        'Lord L6': ['lord.*l6'],
        'Maggard Slant': ['mag.*ard.*slant', 'mr.*slant'],
        'Maggard V2': ['maggard.*V2', 'maggard.*(oc|open)', 'mr.*v2'],
        'Maggard V3M': ['maggard.*V3M', 'V3M'],
        'Maggard V3A': ['Maggard.*V3A', 'V3A'],
        'Maggard V3': [
            'Maggard.*V3',
            'Maggard.*M3',
            'V3',
            'MR\d{1,2}'#assume folks who ordered a full maggard razor and listed it as such went with V3
        ],
        'Merkur 15C': ['15c'],
        'Merkur 23C': ['23c'],
        'Merkur 24C': ['24c'],
        'Merkur 33C': ['33c'],
        'Merkur 34C': ['34c'],
        'Merkur 37C': ['37c'],
        'Merkur 38C': ['38c'],
        'Merkur 39C': ['39c'],
        'Merkur 41C': ['41c'],
        'Merkur 43C': ['43c'],
        'Merkur 45': ['merkur.*45'],
        'Merkur Futur': ['futur'],
        'Merkur Mergress': ['mergress', 'digress'],
        'Merkur Progress': ['progress'],
        'Merkur Vision': ['vision'],
        'Mongoose': ['goose'],
        'Muhle R41': ['R41'],
        'Muhle R89': ['R10\d', 'R89', 'muhle.*89'],
        'Muhle Rocca': ['rocca'],
        'Noble Otter DE': ['NOC(1|2)', 'NO(1|2)C'],
        'Oberon Safety Razor': ['Oberon'],
        'Occams Razor Enoch': ['enoch'],
        'OneBlade Core': ['oneblade.*core'],
        'OneBlade Genesis': ['oneblade.*genesis'],
        'OneBlade Hybrid': ['oneblade.*hybrid'],
        'Other Shavette': ['shavette'],
        'Other Straight Razor': [
            'hollow',
            '\d\/\d',
            'frameback',
            'kamisori',
            'straig',
            'joseph\s*(elliot|allen)',
            'fred.*Reynolds',
            'gold.*dollar',
            'wedge',
            'french.*point',
            'dubl.*duck',
            '&\s+son',
            'engels',
            'Wostenholm',
            'suzumasa',
            'wester.*brothers',
            'green.*lizard',
            'Cattaraugus',
            'Heljstrand',
            'friedr.*herd',
            'friodur',
            'Henckels',
            'henkels',
            'torrey',
            'tornblom',
            'Issard',
        ],
        'PAA Alpha Ecliptic': ['alpha.*ecli'],
        'PAA Bakelite Slant': ['(phoenix|paa).*bake.*slant'],
        'PAA DOC': ['(phoenix|paa).*doc', '(phoenix|paa).*double.*comb'],
        'Paradigm 17-4': ['parad.*17'],
        'Paradigm SE': ['parad.*se'],
        'Paradigm Ti': ['parad.*ti'],
        'Paradigm Ti II': ['parad.*ii'],
        'Parker 24C': ['parker.*24C'],
        'Parker 29L': ['29L'],
        'Parker 60R': ['60R'],
        'Parker 66R': ['66R'],
        'Parker 87R': ['87R'],
        'Parker 90R': ['90R'],
        'Parker 96R': ['96R'],
        'Parker 98R': ['98R'],
        'Parker 99R': ['99R'],
        'Parker 111W': ['111W'],
        'Parker SRX': ['parker.*srx'],
        'Parker Variant': ['variant'],
        'Pearl L-55': ['Pearl L-55'],
        'PILS': ['pils.*10', '^pils$'],
        'Portland Razor Co. Straight': ['portland.*razor'],
        'QShave Parthenon': ['parthenon'],
        'Ralf Aust Straight': ['ralf.*aust'],
        'Raw Shaving RS-10': ['rs-*10'],
        'Razorine': ['razorine'],
        'Razorock Baby Smooth': ['ba*by.*smooth'],
        'Razorock Game Changer .84': ['game.*changer.*84', 'gc.*84', 'game.*changer'],
        'Razorock Game Changer .68': ['game.*changer.*68', 'gc.*68'],
        'Razorock German 37 Slant': ['r.*r.*german.*37', 'r.*r.*slant.*37', 'r.*r.*37.*slant'],
        'Razorock Hawk (v1 or v2)': ['hawk', 'hawk*.*v'],
        'Razorock Lupo': ['Lupp*o'],
        'Razorock Mamba': ['mamba'],
        'Razorock MJ-90': ['mj-*90'],
        'Razorock SLOC': ['r*.r*.*sloc'],
        'Razorock Stealth Slant': ['r*.r*.*stealth.*slant'],
        'Razorock Teck II': ['r.*r.*teck'],
        'Razorock Wunderbar Slant': ['wunderbar'],
        'Rex Ambassador': ['rex.*ambassador', 'ambassador.*rex', 'rex.*\d'],
        'Rex Envoy': ['envoy'],
        'Rockwell 2C': ['Rockwell.*2C', '2C'],
        'Rockwell 6C': ['Rockwell.*6C', 'Rockwell', '6c'],
        'Rockwell 6S': ['Rockwell.*6S', '6s'],
        'Rocnel Elite 2019': ['Roc.*elite.*2019','2019.*Roc.*elite'],
        'Rolls Razor': ['rolls.*razor'],
        'Schick Hydromagic': ['hydro[\-\s]*magic'],
        'Schick Injector': ['Schick.*Injector', 'schick.*type', 'golden.*500', 'schick.*grip', 'schick.*\w\d'],
        'Schick Krona': ['krona'],
        'Standard Razor': ['standard.*razor', '^standard$', 'standard.*(black|raw)', '(raw|black).*standard'],
        'Stirling Slant': ['stirling.*slant'],
        'Stirling DE3P7S': ['DE3P7S'],
        'Supply SE': ['sup.*ly.*inject', 'sup.*ly.*2', 'supply.*se'],
        'Tatara Nodachi': ['nodachi'],
        # matusumi is a common mispelling apparently
        'Tatara Masamune': ['masamune', 'Matusumi', 'tatara'],
        'Timeless (Unspecified)': ['Timeless'],
        'Timeless .68': ['Timeless.*68', 't(i|l).*68'],
        'Timeless .95': ['Timeless.*95', '95.*timeless'],
        'Timeless Bronze': ['Timeless.*bronze'],
        'The Holy Black SR-71': ['sr-*71'],
        'Tradere': ['tradere'],
        'Van Der Hagen Razor': ['Van Der Haa*gen', 'vdh'],
        'Wade & Butcher Straight': ['wade.*butcher', 'w&b'],
        'Weck Sextoblade': ['Sextoblade'],
        'WCS 77': ['77-*S', 'WCS.*77'],
        'WCS 78': ['78-*BL', '78M', 'WCS.*78'],
        'WCS 84': ['84-*R*B', 'WCS.*84'],
        'WCS 88': ['88-*S', 'WCS.*88'],
        'WCS/Charcoal Goods - El Capitan': ['el\s*capitan'],
        'WCS/Charcoal Goods - Hyperion': ['hyperion'],
        'WCS/Charcoal Goods - Hollywood Palm': ['hollywood.*palm'],
        'Weber ARC': ['weber.*arc'],
        'Weber DLC': ['weber.*dlc'],
        'Weber PH': ['weber.*ph'],
        'Wilkinson Sword Classic': ['wilk.*sword.*clas'],
        'Wolfman Guerilla': ['guerr*ill*a', 'wolf.*uag', '^uag$', '^uag', 'uag$', 'uag\s*razor'],
        'Wolfman WR1': [
            'Wolfman.*WR-*1', # this will be evaluated first, as will the wr2 variant, so we will be as specfici as possible
            'Wolfman',# assume if not specified that it is a WR1
            'WR-*1', # catch the case where eg ntownuser just lists wr1 / wr2
        ],
        'Wolfman WR2': [
            'Wolfman.*WR-*2',
            'WR-*2'
        ],
        'Yates 921': ['921-*\w', 'yates.*921'],
        'Yaqi Slant': ['yaqi.*slant'],


    })


if __name__ == '__main__':
    arn = AlternateRazorNames()
    print(arn.all_razor_names)