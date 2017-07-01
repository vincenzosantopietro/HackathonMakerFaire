from values import office_contacts


def office_full_contact_formatter(office_name):
    speech = 'Telefono: ' + office_contacts[office_name]['tel'] + ' - opzione ' + str(office_contacts[office_name]['option']) + '\n'
    speech += 'FAX: ' + office_contacts[office_name]['fax'] + '\n'
    speech += 'Email: ' + office_contacts[office_name]['email'] + '\n'
    speech += 'PEC: ' + ' '.join(office_contacts[office_name]['pec']) + '\n'
    speech += 'Apertura: \n' + office_contacts[office_name]['work_days'].capitalize() + '\n'
    speech += '' + office_contacts[office_name]['work_hours'].capitalize()

    return speech


def office_work_hour_contact_formatter(office_name):
    speech = 'E\' aperta \n'
    speech += office_contacts[office_name]['work_days'] + '\n'
    speech += office_contacts[office_name]['work_hours']

    return speech


def office_email_contact_formatter(office_name):
    speech = 'Email: ' + office_contacts[office_name]['email'] + '\n'
    speech += 'PEC: ' + ' '.join(office_contacts[office_name]['pec'])

    return speech


def office_tel_contact_formatter(office_name):
    speech = 'Telefono: ' + office_contacts[office_name]['tel'] + ' - opzione ' + str(office_contacts[office_name]['option']) + '\n'
    speech += 'FAX: ' + office_contacts[office_name]['fax'] + '\n'

    return speech



