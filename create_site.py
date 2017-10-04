import json
import os
import markdown
from jinja2 import Environment, FileSystemLoader
from livereload import Server


def get_articles_data():
    if not os.path.exists('config.json'):
        return None
    with open('config.json', 'r', encoding='utf-8') as file_handler:
        return json.load(file_handler)['articles']


def get_abs_path():
    return os.getcwd()


def change_slashes(dirname):
    return dirname.replace('\\', '/')


def get_filepath(dirname, relative_path):
    return '{}/articles/{}'.format(dirname, relative_path)


def convert_md_to_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as md_data:
        html_data = markdown.markdown(md_data.read(),
                extensions=['markdown.extensions.codehilite'])
    return html_data


def apply_template(data_for_rendering, title):
    env = Environment(loader=FileSystemLoader('templates', encoding='utf-8'))
    template = env.get_template('page_template.html')
    rendered_html = template.render(content=data_for_rendering, title=title)
    return rendered_html


def change_extension(filepath):
    filename_w_o_ext = os.path.splitext(filepath)[0]
    file_new_extension = '{}.html'.format(filename_w_o_ext)
    return file_new_extension


def save_html(saved_data, filepath):
    with open(filepath, 'w') as page:
        page.write(saved_data)


def format_path():
    abs_path = get_abs_path()
    format_path = change_slashes(abs_path)
    return format_path


def create_site():
    articles_data = get_articles_data()
    abs_path = format_path()
    for article in articles_data:
        filepath = get_filepath(abs_path, article['source'])
        html_from_md = convert_md_to_html(filepath)
        format_html = apply_template(html_from_md, article['title'])
        filepath_with_new_extension = change_extension(filepath)
        save_html(format_html, filepath_with_new_extension)


if __name__ == '__main__':
    create_site()
    '''
    server = Server()
    server.watch('templates/*.html', create_site)
    articles_data = get_articles_data()
    for article in articles_data:
        abs_path = format_path()
        filepath = get_filepath(abs_path, article['source'])
        server.watch(filepath, create_site)
    server.serve()
    '''