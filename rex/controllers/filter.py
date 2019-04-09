@app.template_filter()
def format_date(date): # date = datetime object.
    return date.strftime('%H:%M:%S')