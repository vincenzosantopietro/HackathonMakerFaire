# This Python file uses the following encoding: utf-8

SORESA_NEWS_INTENT_NAME='SoresaNews'
SORESA_WELCOME_INTENT_NAME='Welcome'

# Segreteria
SORESA_ORARI_SEGRETERIA_INTENT_NAME='Contatti_Orari_Segreteria'
SORESA_INFORMAZIONI_SEGRETERIA_INTENT_NAME='Contatti_Informazioni_Segreteria'
SORESA_TELEFONO_SEGRTERIA_INTENT_NAME='Contatti_Telefono_Segreteria'
SORESA_EMAIL_SEGRTERIA_INTENT_NAME='Contatti_Email_Segreteria'

# Ufficio ordini
SORESA_ORARI_UFFICIO_ORDINI_INTENT_NAME='Contatti_Orari_UfficioOrdini'
SORESA_INFORMAZIONI_UFFICIO_ORDINI_INTENT_NAME='Contatti_Informazioni_UfficioOrdini'
SORESA_TELEFONO_UFFICIO_ORDINI_INTENT_NAME='Contatti_Telefono_UfficioOrdini'
SORESA_EMAIL_UFFICIO_ORDINI_INTENT_NAME='Contatti_Email_UfficioOrdini'

SORESA_BANDI_INTENT_NAME='Bandi'
SORESA_CONSIGLIOAMMINISTRAZIONE_INTENT_NAME='ConsiglioAmministrazione'
SORESA_COLLEGIOSINDACALE_INTENT_NAME='CollegioSindacale'
SORESA_CONVENZIONI_INTENT_NAME='ConvenzioniPA'
SORESA_BANDI_INTENT_NAME='Bandi'
SORESA_CHISIAMO_NAME='ChiSiamo'


consiglio_amministrazione = ['Dott. Giovanni Porcelli - Presidente con funzioni di amministratore delegato',
                            'Avv. Giulia Abbate - consigliere',
                            'Avv. Luigi Giuliano - consigliere']

collegio_sindacale = ['Dott. Fabio Migliardi - presidente',
                        'Dott. Giovanni De Rosa - componente',
                        'Dott.ssa Dora Ruggiero - componente']

office_contacts = {
    'segreteria': {
        'tel': '081 2128174',
        'fax': '081 7500012',
        'email': 'segreteria@soresa.it',
        'pec': ['soresa@pec.soresa.it'],
        'option': 4,
        'work_days': 'dal lunedì al venerdì',
        'work_hours': 'dalle 08.00 alle 13.00 e dalle 13.45 alle 16.45'
    },

    'ufficioordini': {
        'tel': '081 2128174',
        'fax': '081 6040337',
        'email': 'segreteria@soresa.it',
        'pec': ['ordinisoresa@pec.soresa.it', 'flussifinanziari@pec.soresa.it'],
        'option': 2,
        'work_days': 'dal lunedì al venerdì',
        'work_hours': 'dalle 08.00 alle 13.00 e dalle 13.45 alle 16.45'
    },

    'gestionedebitoria': {
        'tel': '081 2128174',
        'fax': '081 7500012',
        'email': 'servizio.creditori@soresa.it',
        'pec': ['servizio.creditori@pec.soresa.it', 'servizio.aziendesanitarie@pec.soresa.it'],
        'option': 1,
        'work_days': 'dal lunedì al venerdì',
        'work_hours': 'dalle 08.00 alle 13.00 e dalle 13.45 alle 16.45'
    },

    'ufficioacquisti': {
        'tel': '081 2128174',
        'fax': '081 7500012',
        'email': 'acquisti.centralizzazione@soresa.it',
        'pec': ['ufficiogare@pec.soresa.it'],
        'option': 4,
        'work_days': 'dal lunedì al venerdì',
        'work_hours': 'dalle 08.00 alle 13.00 e dalle 13.45 alle 16.45'
    },

    'ufficiolegale': {
        'pec': ['arealegale@pec.soresa.it']
    },

    'accreditamentoistituzionale': {
        'pec': ['accreditamento@pec.soresa.it']
    }
}

position = {
    'longitude': '14.2799888',
    'latitude': '40.8586875'
}
