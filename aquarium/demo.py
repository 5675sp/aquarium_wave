from h2o_wave import site, ui
page = site['/demo']
sample_markdown = '''
Here's a [link to an image](https://upload.wikimedia.org/wikipedia/en/c/cb/Flyingcircus_2.jpg).
'''
page['example'] = ui.form_card(
    box='1 1 4 10',
    items=[ui.text(sample_markdown)]
)
page.save()