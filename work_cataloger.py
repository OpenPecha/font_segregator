from pathlib import Path
from openpecha.buda import api as buda_api

from openpecha.utils import dump_yaml

def catalog_work(work_datas):
    work_catalog = {}
    for work_data in work_datas:
        work_id = work_data.split(',')[0]
        img_grp_id = work_data.split(',')[1]
        if work_id not in work_catalog:
            work_catalog[work_id] = []
        work_catalog[work_id].append(img_grp_id)
    return work_catalog

def get_img_groups(work_id):
    """
    Get the image groups from the bdrc scan id
    """
    res = buda_api.get_buda_scan_info(work_id)
    if not res:
        print(f'BdcrScanNotFound Scan {work_id} not found')
    return res["image_groups"]


def catalog_work_from_work_id(work_ids):
    work_catalog = {}
    for work_id in work_ids:
        work_catalog[work_id] = get_img_groups(work_id)
        
    return work_catalog

if __name__ == "__main__":
    # work_datas = Path('./data/modernprints.txt').read_text().splitlines()
    # work_catalog = catalog_work(work_datas)
    # dump_yaml(work_catalog, Path('./data/work_catalog.yml'))
    work_ids = Path('./data/wooden_print.txt').read_text().splitlines()
    work_catalog = catalog_work_from_work_id(work_ids)
    dump_yaml(work_catalog, Path('./data/wooden_print_work_catalog.yml'))
