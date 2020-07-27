def timeStr(duration_ms, colon=True):
    ''' Convert ms to 'MM:SS' or 'HH h MM min '''
    seconds = int(duration_ms / 1000)
    if colon:
        hours = int(int(seconds / 60) / 60)
        hoursSrt = ''
        if hours:
            hoursSrt = f'{hours:02}:'

        return f'{hoursSrt}{int(seconds / 60):02}:{int(seconds % 60):02}'

    else:
        minutes = int(seconds / 60)
        hours = int(minutes / 60)

        return f'{hours} h {int(minutes % 60)} min'


def delSpecCh(str):
    for ch in list('\\/:*?"<>|+%'):
        str = str.replace(ch, '')
    return ' '.join(str.split())
