from pprint import pprint
spieler = ['Mi', 'Rheilo']
trans = {
    'Mi' : 'Mi_',
    'Rheilo': 'Rheîlo'
}
for s in spieler:
    if s in trans:
        spieler[spieler.index(s)] = trans[s]

pprint(spieler)
