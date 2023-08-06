import json
import math
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

from tululu_offline.download_files import download_template
from tululu_offline.get_args import get_args


def render_website() -> None:  # noqa: WPS210
    """Renders the template.html in index.html and saves a new file."""
    args = get_args()
    json_path = args.json_path
    dest_folder = args.dest_folder
    number_of_books_per_page = args.number_of_books_per_page

    path_to_file_with_books = json_path if json_path else f'{dest_folder}/books.json'
    with open(path_to_file_with_books, 'r') as file_object:
        books_json = file_object.read()
    books_list = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=['jinja2.ext.loopcontrols'],
    )

    template_path = download_template()
    template = env.get_template(template_path)

    pages_folder_path = 'pages'
    os.makedirs(pages_folder_path, exist_ok=True)

    count_of_books = len(books_list)
    number_of_pages = math.ceil(count_of_books / number_of_books_per_page)
    current_page = 0

    chunks = [
        books_list[index_number:index_number + number_of_books_per_page]
        for index_number in range(0, count_of_books, number_of_books_per_page)
    ]

    for chunk in chunks:
        current_page = current_page + 1
        rendered_page = template.render(
            books=chunk,
            current_page=current_page,
            number_of_pages=int(number_of_pages),
        )

        path_to_index_file = f'{pages_folder_path}/index{current_page}.html'
        with open(path_to_index_file, 'w', encoding='utf8') as index_file:
            index_file.write(rendered_page)


def main() -> None:  # noqa: WPS210
    """Entry point."""
    server = Server()
    server.watch('template.html', render_website)
    server.serve(root='.')


if __name__ == '__main__':
    main()
