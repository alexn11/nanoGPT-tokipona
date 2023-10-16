
# source: linku.la data
nimi_ale = ['a', 'akesi', 'ala', 'alasa', 'ale', 'anpa', 'ante', 'anu', 'awen', 'e', 'en', 'esun', 'ijo', 'ike', 'ilo', 'insa', 'jaki', 'jan', 'jelo', 'jo', 'kala', 'kalama', 'kama', 'kasi', 'ken', 'kepeken', 'kili', 'kiwen', 'ko', 'kon', 'kule', 'kulupu', 'kute', 'la', 'lape', 'laso', 'lawa', 'len', 'lete', 'li', 'lili', 'linja', 'lipu', 'loje', 'lon', 'luka', 'lukin', 'lupa', 'ma', 'mama', 'mani', 'mi', 'moku', 'moli', 'monsi', 'mu', 'mun', 'musi', 'mute', 'nanpa', 'nasa', 'nasin', 'nena', 'ni', 'nimi', 'noka', 'o', 'olin', 'ona', 'open', 'pakala', 'pali', 'palisa', 'pan', 'pana', 'pi', 'pilin', 'pimeja', 'pini', 'pipi', 'poka', 'poki', 'pona', 'pu', 'sama', 'seli', 'selo', 'seme', 'sewi', 'sijelo', 'sike', 'sin', 'sina', 'sinpin', 'sitelen', 'sona', 'soweli', 'suli', 'suno', 'supa', 'suwi', 'tan', 'taso', 'tawa', 'telo', 'tenpo', 'toki', 'tomo', 'tu', 'unpa', 'uta', 'utala', 'walo', 'wan', 'waso', 'wawa', 'weka', 'wile', 'kijetesantakalu', 'kin', 'ku', 'leko', 'meli', 'mije', 'monsuta', 'n', 'namako', 'tonsi', 'epiku', 'kipisi', 'lanpan', 'meso', 'misikeke', 'oko', 'soko', 'ali', 'apeja', 'jasima', 'kiki', 'kokosila', 'linluwi', 'majuna', 'nimisin', 'oke', 'omekapo', 'powe', 'usawi', 'wuwojiti', 'yupekosi', 'isipin', 'kamalawala', 'kapesi', 'misa', 'pake', 'puwa', 'taki', 'te', 'to', 'unu', 'wa', 'aka', 'ako', 'alente', 'alu', 'awase', 'eki', 'eliki', 'enko', 'ete', 'ewe', 'i', 'iki', 'ipi', 'itomi', 'jaku', 'jalan', 'jami', 'jans', 'je', 'jonke', 'ju', 'jule', 'jume', 'kalamARR', 'kalijopilale', 'kan', 'kapa', 'ke', 'kepen', 'kese', 'ki', 'kisa', 'konsi', 'konwe', 'kosan', 'kulijo', 'kulu', 'kuntu', 'kutopoma', 'lijokuku', 'likujo', 'lo', 'loka', 'lokon', 'lu', 'melome', 'mijomi', 'molusa', 'mulapisu', 'nalanja', 'natu', 'neja', 'nele', 'nja', 'nu', 'ojuta', 'okepuma', 'oki', 'omekalike', 'omen', 'oni', 'owe', 'pa', 'pakola', 'pasila', 'pata', 'peta', 'peto', 'pika', 'Pingo', 'pipo', 'po', 'polinpin', 'pomotolo', 'poni', 'samu', 'san', 'sikomo', 'sipi', 'slape', 'soto', 'su', 'suke', 'sutopatikuna', 'teje', 'ten', 'tokana', 'toma', 'tuli', 'u', 'umesu', 'waleja', 'wasoweli', 'wawajete', 'we', 'we', 'wekama', 'wi', 'yutu']
digits = list('0123456789')
punctuations = list(',;:.!?"\'<>()[]{}-*+/\\|&#=^')

vowels = [ 'a', 'e', 'o', 'i', 'u', ]
consonnants = [
    'w', 'j',
    'm', 'n',
    's', 'l',
    'p', 't', 'k', 
]
initials = [ '', ] + consonnants
finals = vowels + [ v + 'n' for v in vowels ]

toki_pona_syllables = [
    i + f
    for i in initials
    for f in finals
]
forbidden_syllables = [
    'ji', 'jin', 'ti', 'tin', 'wu', 'wun', 'wo', 'won'
]
toki_pona_syllables = [
    s for s in toki_pona_syllables
    if(s not in forbidden_syllables)
]

toki_pona_letters = vowels + consonnants
non_toki_pona_letters = list('bcdfghqrvxyz')












