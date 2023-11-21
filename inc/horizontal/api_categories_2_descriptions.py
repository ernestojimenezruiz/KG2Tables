import config
from inc import api_classes, api_properties
import csv
from os.path import join, realpath, exists
from os import makedirs
from util.util_categories import get_categories_from_file, handle_duplicate_results
import config

# results paths
descriptions_file_path = join(config.HORIZONTAL_PATH, 'instances', 'descriptions')
if not exists(descriptions_file_path):
    makedirs(descriptions_file_path)


async def save_description_version(filename, res_strs):
    lines = []
    for Qxx, v in res_strs.items():
        lines += [[Qxx, vi['value']] for vi in v if 'description' in vi['prop']]

    with open(join(descriptions_file_path, filename + '.csv'), 'w', encoding='utf8', errors='ignore',
              newline='') as file:
        csvwriter = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['gt_R2I', 'description'])
        csvwriter.writerows(lines)


async def parse_categories():
    # open data/Categories.csv parse it to get categories list
    categories = await get_categories_from_file()

    # pass these categories to get subclasses
    res_instances = await api_classes.get_instances(categories)

    res_instances = await handle_duplicate_results(res_instances, table_type_path='')

    for k, v in res_instances.items():
        instances = [vi['child'] for vi in v if vi['child'].startswith('Q')]

        if instances:
            res_strs = await api_properties.get_strings_for_lst(instances)
            await save_description_version(k, res_strs)

    return res_instances