#!/usr/bin/python3

import os
import shutil
import subprocess

from typing import NamedTuple

from pathlib import Path

GOOGLE_CHROME_PATH = ('/Applications/Google\ Chrome.app/Contents/MacOS/'
    'Google\ Chrome')


# Can't make album, text around printed area :()
def export_svg_pdf(svg_path: Path, pdf_output_path: Path):
    subprocess.check_call([f'{GOOGLE_CHROME_PATH} --headless --print-to-pdf='
        f'{pdf_output_path} --window-size=1480,1048 {svg_path}'], shell=True)
    # os.rename('screenshot.png', png_output_path)


# Works ok now
def export_svg_png(svg_path: Path, png_output_path: Path):
    subprocess.check_call([
        f'{GOOGLE_CHROME_PATH} --headless --screenshot '
        f'--window-size=1480,1048 {svg_path}',
        ], shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
    )
    os.rename('screenshot.png', png_output_path)


def generate_cert(
    *, name: str, svg_template_path: Path, svg_output_path: Path, 
    pdf_output_path: Path, png_output_path: Path,
    ):
    subprocess.check_call([f'sed "s/PLACE_NAME_HERE/{name}/" ' 
        f'{svg_template_path} > {svg_output_path}'], shell=True)

    export_svg_png(svg_path=svg_output_path, png_output_path=png_output_path)


class GenerateCertTask(NamedTuple):
    list_file_path: Path
    template_file_path: Path
    output_slug: str


def generate_list(task: GenerateCertTask, generated_path: Path):
    print(f'Make list {task.output_slug}')
    items = []
    with open(task.list_file_path) as f:
        for line in f:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            items.append(stripped_line)

    output_path = generated_path / task.output_slug

    output_path_png = generated_path / (task.output_slug + '-png')
    output_path_png.mkdir(parents=True)

    output_path_svg = generated_path / (task.output_slug + '-svg')
    output_path_svg.mkdir(parents=True)

    for counter, name in enumerate(items, start=1):
        make_base_name = name.replace(' ', '_').lower()
        print(f'  {counter:02}/{len(items):02} Bake {make_base_name}')
        generate_cert(
            name=name, 
            svg_template_path=task.template_file_path,
            svg_output_path=output_path_svg / f'{make_base_name}.svg', 
            pdf_output_path=output_path / f'{make_base_name}.pdf',
            png_output_path=output_path_png / f'{make_base_name}.png',
        )


def generate_certs():
    lists_path = Path('lists')
    templates_path = Path('templates')
    generated_path = Path('_generated')

    tasks = [
        GenerateCertTask(
            output_slug='en-full', 
            list_file_path=lists_path / 'cert-en-full.txt', template_file_path=templates_path / 'en_bold.svg',
        ),
        GenerateCertTask(
            output_slug='en-self', 
            list_file_path=lists_path / 'cert-en-self.txt', template_file_path=templates_path / 'en_bold.svg',
        ),
        GenerateCertTask(
            output_slug='ru-full', 
            list_file_path=lists_path / 'cert-ru-full.txt', template_file_path=templates_path / 'ru_bold.svg',
        ),
        GenerateCertTask(
            output_slug='ru-self', 
            list_file_path=lists_path / 'cert-ru-self.txt', template_file_path=templates_path / 'ru_bold.svg',
        ),
    ]

    shutil.rmtree(generated_path, ignore_errors=True)
    generated_path.mkdir(parents=True)
    for task in tasks:
        generate_list(task, generated_path=generated_path)
        

if __name__ == '__main__':
    generate_certs()
