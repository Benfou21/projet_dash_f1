def get_classement_hover_template(name):
    if name == 'Hamilton':
        hover_template = ('<b>%{customdata[0]}<br>' +
                      f'<b>{name}: </b>' + '%{customdata[5]} - %{customdata[7]}pts<br>' +
                      '<b>Championnat du monde<br>' +
                      f'<b>{name}: </b>' + '%{customdata[11]}e - %{customdata[9]}pts<br>' +
                      '<extra></extra>'
        )
    elif name == 'Verstappen':
        hover_template = ('<b>%{customdata[0]}<br>' +
                      f'<b>{name}: </b>' + '%{customdata[6]} - %{customdata[8]}pts<br>' +
                      '<b>Championnat du monde<br>' +
                      f'<b>{name}: </b>' + '%{customdata[12]}e - %{customdata[10]}pts<br>' +
                      '<extra></extra>'
        )
    else: hover_template = ''
    return hover_template