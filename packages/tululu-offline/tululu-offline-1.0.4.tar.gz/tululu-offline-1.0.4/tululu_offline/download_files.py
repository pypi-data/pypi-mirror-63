import os
from typing import List, Optional

import requests
from pathvalidate import sanitize_filename  # type: ignore


def download_file(path_to_file: str, file_url: str) -> None:
    """Downloads file."""
    block_size = 1024
    response = requests.get(file_url, allow_redirects=False)
    response.raise_for_status()
    with open(path_to_file, 'wb') as file_object:
        for chunk in response.iter_content(block_size):
            file_object.write(chunk)


def download_txt(
    url: str, filename: str, dest_folder: str, folder='books',
) -> Optional[str]:
    """Downloads a book in text format."""
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    books_folder_path = os.path.join(dest_folder, folder)
    os.makedirs(books_folder_path, exist_ok=True)
    if 'text/plain' in response.headers['Content-Type']:
        normalized_filename = sanitize_filename(filename)
        book_path = os.path.join(
            books_folder_path,
            f'{normalized_filename}.txt',
        )

        with open(book_path, 'w') as file_object:
            file_object.write(response.text)
        return book_path
    return None


def download_image(
    url: str, filename: str, dest_folder: str, folder='images',
) -> str:
    """Downloads image of book."""
    image_folder_path = os.path.join(dest_folder, folder)
    os.makedirs(image_folder_path, exist_ok=True)
    normalized_filename = sanitize_filename(filename)
    path_to_image = os.path.join(
        image_folder_path,
        normalized_filename,
    )
    download_file(path_to_image, url)
    return path_to_image


def download_template() -> str:
    """Downloads template file to root dir."""
    template_url = 'https://raw.githubusercontent.com/velivir/tululu-offline/master/template.html'
    path_to_template = 'template.html'
    download_file(path_to_template, template_url)
    return path_to_template


def download_js_files() -> List[str]:
    """Downloads Javascript files for website."""
    js_files_urls = [
        'https://code.jquery.com/jquery-3.4.1.slim.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
    ]
    path_to_files = []
    js_file_folder = 'static/js'
    os.makedirs(js_file_folder, exist_ok=True)

    for file_url in js_files_urls:
        path_to_file = os.path.join(
            js_file_folder,
            file_url.split('/')[-1],
        )
        download_file(path_to_file, file_url)
        if os.path.exists(path_to_file):
            path_to_files.append(path_to_file)
    return path_to_files


def download_bootstrap_css() -> Optional[str]:
    """Downloads bootstrap css file."""
    bootstrap_css_url = 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
    css_file_folder = 'static/css'
    os.makedirs(css_file_folder, exist_ok=True)
    path_to_file = os.path.join(
        css_file_folder,
        bootstrap_css_url.split('/')[-1],
    )
    download_file(
        path_to_file,
        bootstrap_css_url,
    )
    if os.path.exists(path_to_file):
        return path_to_file
    return None
