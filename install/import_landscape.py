import sys
import itertools
import csv
import yaml
from pprint import pprint

# input csv
isv_idx = 0
platform_vendor_idx = 1
product_name_idx = 2
open_source_idx = 3
part_of_odh_idx = 4
community_operator_idx = 5
certified_operator_idx = 6
ubi_implemented_idx = 7
homepage_url_idx = 8
repo_url_idx = 9
logo_idx = 10
twitter_idx = 11
crunchbase_idx = 12
component_projects_idx = 13
first_subcategory_idx = 14


def write_old_landscape_csv(yaml_data, landscape_csv):
    with open(landscape_csv, mode='w') as product_file:
        product_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        product_writer.writerow(
            ['ISVs', 'Platform vendor?', 'Product Name', 'Open Source', 'Part of ODH?', 'Homepage URL', 'Repository',
             'Logo', 'Twittter', 'Crunchbase'])
        for category in yaml_data.get('landscape'):
            if not category:
                continue
            for subcategory in category.get('subcategories'):
                if not subcategory:
                    continue
                for item in subcategory.get('items'):
                    if item:
                        isv = item.get('name')
                        name = item.get('name')
                        product_writer.writerow([
                            isv,
                            '',
                            name,
                            '',
                            '',
                            item.get('homepage_url'),
                            item.get('repo_url'),
                            item.get('logo'),
                            item.get('twitter'),
                            item.get('crunchbase')
                        ])


def save_landscape_as_csv(landscape_yaml, landscape_csv):
    with open(landscape_yaml, 'r') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            write_old_landscape_csv(yaml_data, landscape_csv)
        except yaml.YAMLError as exc:
            print(exc)


def init_landscape_dict(category_row, subcategory_row):
    category = None
    subcategory = None
    landscape = dict({'landscape': []})
    categories = []
    subcategories = []

    for idx, subcategory_name in enumerate(subcategory_row):
        if category_row[idx]:
            category = {
                'category': None,
                'name': category_row[idx],
                'subcategories': []
            }
            landscape.get('landscape').append(category)

        if category and subcategory_name:
            subcategory = {
                'subcategory': None,
                'name': subcategory_name,
                'items': []
            }
            category['subcategories'].append(subcategory)
        categories.append(category)
        subcategories.append(subcategory)

    # pprint(landscape)
    # pprint(categories)
    # pprint(subcategories)

    return landscape, categories, subcategories


def add_ecosystem_item(row, subcategories):
    isv = None
    for idx, field in enumerate(row):
        subcategory = subcategories[idx]
        if idx == 0:
            isv = field
        elif subcategory and field:
            product_names = field.split(',')
            for product in product_names:
                item = {
                    'item': None,
                    'name': f'{isv} {product}',
                    'homepage_url': None,
                    'repo_url': None,
                    'logo': 'no-data.svg',
                    'twitter': None,
                    'crunchbase': 'https://www.crunchbase.com/organization/no-data'
                }
                subcategory['items'].append(item)


def add_landscape_extras(landscape):
    category = {
        'category': None,
        'name': 'Open Data Hub Partner',
        'subcategories': [
            {
                'subcategory': None,
                'name': 'General',
                'items': []
            }
        ]
    }
    landscape.get('landscape').append(category)

    # category = {
    #     'category': None,
    #     'name': 'Hack',
    #     'subcategories': [
    #         {
    #             'subcategory': None,
    #             'name': 'Hack',
    #             'items': [
    #                 {
    #                     'item': None,
    #                     'name': 'No Crunchbase Data Available',
    #                     'homepage_url': 'https://www.no-data.com',
    #                     'logo': 'no-data.svg',
    #                     'crunchbase': 'https://www.crunchbase.com/organization/no-data'
    #                 }
    #             ]
    #         }
    #     ]
    # }
    # landscape.get('landscape').append(category)

    return landscape


def ecosystem_csv_to_yaml(ecosystem_csv, landscape_yaml):
    # output yaml
    landscape = None
    categories = None
    subcategories = None

    with open(ecosystem_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        category_row = []
        for row in csv_reader:
            line_count += 1
            if line_count == 7:
                category_row = row
            if line_count == 8:
                subcategory_row = row
                landscape, categories, subcategories = init_landscape_dict(category_row, subcategory_row)
            if line_count > 12:
                add_ecosystem_item(row, subcategories)
        add_landscape_extras(landscape)
        with open(landscape_yaml, 'w') as outfile:
            yaml.dump(landscape, outfile, default_flow_style=False, sort_keys=False)


def construct_header_1(input_row):
    header_row = ['', '', '', 'Product Information', '', '', '', '', '', '']
    for idx, column in enumerate(input_row):
        if idx >= first_subcategory_idx:
            header_row.append(column)

    return header_row


def construct_header_2(input_row):
    header_row = ['ISVs', 'Platform vendor?', 'Product Name', 'Open Source', 'Part of ODH?', 'Homepage URL', 'Repository',
                  'Logo', 'Twittter', 'Crunchbase']
    for idx, column in enumerate(input_row):
        if idx >= first_subcategory_idx:
            header_row.append(column)

    return header_row


def create_product_row(input_row, idx, product_name):
    isv = input_row[isv_idx]
    odh = 'TRUE' if input_row[part_of_odh_idx] == 'x' else 'FALSE'
    platform_vendor = 'TRUE' if input_row[platform_vendor_idx] == 'x' else 'FALSE'

    homepage_url = ''
    repo_url = ''
    logo = 'no-image.svg'
    twitter = ''
    crunchbase = 'https://www.crunchbase.com/organization/no-data'

    row = [isv, platform_vendor, product_name, '', odh, homepage_url, repo_url, logo, twitter, crunchbase]

    num_empty = idx - first_subcategory_idx
    for _ in itertools.repeat(None, num_empty):
        row.append('FALSE')

    return row


def expand_input_row(input_row):
    isv = input_row[0]
    product_rows = {}
    if not isv:
        return []

    for idx, column in enumerate(input_row):
        if idx < first_subcategory_idx:
            continue

        products = [product.strip() for product in column.split(',')]
        for product_name in products:
            if not product_name:
                continue
            product_row = product_rows.get(product_name)
            if not product_row:
                product_rows[product_name] = create_product_row(input_row, idx, product_name)

        for product_name, product_row in product_rows.items():
            if product_name in products:
                product_row.append('TRUE')
            else:
                product_row.append('FALSE')

    return product_rows.values()


def generate_initial_csv(ecosystem_csv, landscape_csv):
    with open(landscape_csv, mode='w') as output_csv:
        writer = csv.writer(output_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with open(ecosystem_csv, mode='r') as input_csv:
            csv_reader = csv.reader(input_csv)
            line_count = 0
            for input_row in csv_reader:
                line_count += 1
                if line_count == 7:
                    writer.writerow(construct_header_1(input_row))
                if line_count == 8:
                    writer.writerow(construct_header_2(input_row))
                if line_count > 12:
                    new_rows = expand_input_row(input_row)
                    for output_row in new_rows:
                        writer.writerow(output_row)


def create_landscape_item(isv, row, subcategory_name):
    product = row[product_name_idx].strip()
    open_source = row[open_source_idx].strip()
    odh = row[part_of_odh_idx]
    community = row[community_operator_idx]
    certified = row[certified_operator_idx]
    ubi = row[ubi_implemented_idx]
    homepage_url = row[homepage_url_idx].strip() or 'missing-homepage'
    repo_url = row[repo_url_idx].strip()
    logo = row[logo_idx].strip() or 'no-image.svg'
    twitter = row[twitter_idx].strip()
    crunchbase = row[crunchbase_idx].strip()
    components = row[component_projects_idx].strip()

    if not product or product.lower() == 'x' or product.lower() == isv.lower():
        name = f'{isv} ({subcategory_name})'
    elif isv.lower() in product.lower():
        name = f'{product} ({subcategory_name})'
    else:
        name = f'{isv} {product} ({subcategory_name})'

    item = {
        'item': None,
        'organization': isv,
        'name': name,
        'homepage_url': homepage_url,
        'open_source': open_source == 'full',
        'repo_url': repo_url,
        'logo': logo,
        'twitter': twitter,
        'crunchbase': crunchbase,
        'components': components
    }

    status = []

    if odh == 'TRUE':
        status.append('odh')
    if community == 'TRUE':
        status.append('community')
    if certified == 'TRUE':
        status.append('certified')
    if ubi == 'TRUE':
        status.append('ubi')

    if status:
        item['status'] = status

    if repo_url:
        item['allow_duplicate_repo'] = True

    return item


def process_landscape_row(isv, row, subcategories):
    for idx, column in enumerate(row):
        if idx < 10 or column == 'FALSE':
            continue
        subcategory = subcategories[idx]
        item = create_landscape_item(isv, row, subcategory.get('name'))
        subcategory['items'].append(item)


def remove_landscape_unneeded(landscape):
    landscape.get('landscape').pop(0)


def landscape_csv_to_yaml(landscape_csv, landscape_yaml):
    # output yaml
    landscape = None
    categories = None
    subcategories = None

    with open(landscape_csv, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        category_row = []
        subcategory_row = []
        isv = ''
        for row in csv_reader:
            line_count += 1
            if line_count == 1:
                category_row = row
            if line_count == 2:
                subcategory_row = row
                landscape, categories, subcategories = init_landscape_dict(category_row, subcategory_row)
            if line_count > 2:
                isv = row[0] or isv
                process_landscape_row(isv, row, subcategories)
        remove_landscape_unneeded(landscape)
        add_landscape_extras(landscape)
        with open(landscape_yaml, 'w') as outfile:
            yaml.dump(landscape, outfile, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    # save_landscape_as_csv('landscape.yml', 'original_landscape.csv')
    # generate_initial_csv('ecosystem.csv', 'initial_landscape.csv')
    # ecosystem_csv_to_yaml('ecosystem.csv', 'new_landscape.yml')
    landscape_csv_to_yaml(sys.argv[1], sys.argv[2])
