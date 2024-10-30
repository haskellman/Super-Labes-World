CHARACTERS_DATA = {
	'char_1': {
		'dialog': {
			'default': ['voce entendeu?'], 
			'visited': ['Parabens poh voce é brabo', 'potato']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'player': {
		'dialog': {
            'default': ['Sim', 'Não'],
            },
		},
    'vitor': {
		'dialog': {
            'default': ['então você conseguiu chegar até aqui!', 'meus parabéns!', 'mas daqui você não passa!', 'sou conhecido como javaboy', 'para conseguir a minha chave você terá que me vencer em uma batalha!', 'você aceita o desafio?'],
			'visited': ['parabéns!', 'você conseguiu mostrar domínio teórico em java', 'tome! leve isso!']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'monalessa': {
		'dialog': {
            'default': ['então você conseguiu a chave do vitor!', 'nada mal', 'vamos ver se você é bom em gerencia de projetos!!!'],
			'visited': ['meus parabéns!', 'você acertou x questões', 'vamos! pegue isso você vai precisar!']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'patricia': {
		'dialog': {
            'default': ['seja bem vindo!', 'então voce conseguiu as outras duas chaves', 'isso não significa nada se você não conseguir a minha!', 'aqui acaba para você! muahahaha'],
			'visited': ['uauu', 'voce conseguiu superar o meu desafio', 'você merece isso!', 'com isso você tem todas as chaves!', 'agora que desafio de verdade', 'você pode entrar no sigAmaes', 'boa sorte!']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'mae': {
		'dialog': {
            'default': ['to cansada de lavar louça nessa casa!'],
			'visited': ['']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'pai': {
		'dialog': {
            'default': ['o que será que eu leio hoje??'],
			'visited': ['to cansada de lavar louça nessa casa!']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    'luaninha': {
		'dialog': {
            'default': ['seja bem vindo ao labgrad', 'aqui voce pode usar os computadores a vontade para estudar', 'mas tem uma regra muito importante rs','faça silencio!'],
			'visited': ['seja bem vindo ao labgrad', 'aqui voce pode usar os computadores a vontade para estudar', 'mas tem uma regra muito importante rs','faça silencio!']},
		'directions': ['down'],
		'look_around': True,
		'visited': False,
		},
    }

ITEMS_DATA = {
    '0': {
        'name': 'chave do vitor',
        'description':'chave do vitor, é a prova de que voce conseguiu a aprovação do javaboy para entrar no sigamaes',
    },
    '1': {
		'name': 'chave da monalessa',
        'description':'chave da mona, é a prova de que voce conseguiu a aprovação da monalessa para entrar no sigamaes',
    },
    '2': {
		'name': 'chave da patrícia',
        'description':'chave da patrícia, é a prova de que voce conseguiu a aprovação da patricia para entrar no sigamaes',
    },
    '4': {
		'name': 'cafe',
        'description':'Uma xícara de café forte e revigorante, feito com grãos de alta qualidade.' \
        'Possui um aroma intenso chocolate amargo.  \n + 100 speed',
    },
}

COMPUTER_DATA = {
    '0': {
        'title': 'Java',
        'description':'Aqui você pode aprender e testar seus conhecimentos em Java',
        'url': 'https://www.google.com',
        'color': 'gray',
	},
    '1': {
        'title': 'Github',
        'description':'O melhor site para aprender git e versionamento de código',
        'url': 'https://www.google.com',
        'color': 'white',
	},
        
}