# Save the category of site tululu.org offline

<p align="center">
    <img width="500"
         src="http://omsklib.ru/files/news/2017/predvarit-zakaz/166513214-1.jpg"
         alt="Books library restyle" />
</p>

## Description
[![Maintainability](https://api.codeclimate.com/v1/badges/c8ec73b47d297795daae/maintainability)](https://codeclimate.com/github/velivir/tululu-offline/maintainability)
[![Build Status](https://travis-ci.com/velivir/tululu-offline.svg?branch=master)](https://travis-ci.com/velivir/tululu-offline)
[![Coverage Status](https://coveralls.io/repos/github/velivir/tululu-offline/badge.png?branch=master)](https://coveralls.io/github/velivir/tululu-offline?branch=master)
![Platform](https://img.shields.io/badge/platform-linux-brightgreen)
![Python_versions](https://img.shields.io/badge/Python-3.7%7C3.8-brightgreen)
![GitHub](https://img.shields.io/github/license/velivir/books-library-restyle)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


The program downloads from tululu.org books in text format and their covers. The following information is also downloaded to the json file:
- title
- author
- image path
- book path
- comments
- genres

After downloading the necessary data, the offline version of the site will be generated (you can see an example [here](https://velivir.github.io/tululu-offline/pages/index1.html))


## How to install

Install using [pip](https://pypi.org/project/tululu-offline/):
  ```bash
  pip install tululu-offline
  ```


## How to use
  ```bash
  tululu-offline [OPTIONS]
  ```


## Options
- [category_url] - the category url [tululu.org](http://tululu.org)
- [--start_page] - which page to start downloading
- [--end_page] - on which page to finish downloading
- [--dest_folder] - path to the directory with parsing results: pictures, books, JSON.
- [--skip_txt] - do not download books
- [--skip_imgs] - do not download images
- [--json_path] - specify your path to *.json file with results
- [--number_of_books_per_page] - number of books per page


## Example run
Run the script with the necessary parameters. For example:
```bash
tululu-offline http://tululu.org/l55/ --start_page 1 --end_page 3 --skip_txt true --skip_imgs true --number_of_books_per_page 15
```

The first page of the library will be available at ```pages/index1.html```


## License

Tululu-offline is licensed under the MIT License. See [LICENSE](https://github.com/velivir/tululu-offline/blob/master/LICENSE) for more information.


## Project goal
The code is written for educational purposes in an online course for web developers [dvmn.org](https://dvmn.org).
