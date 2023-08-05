import ocldev.oclresourcelist


def test_get_resource():
    resources = ocldev.oclresourcelist.OclResourceList()
    resource = {'resource_type': 'Concept', 'id': 'A', 'name': 'Bob', 'owner_id': 'PEPFAR', 'source': 'PLM'}
    resources.append(resource)
    print resources[0]
    assert resource == resources[0]


def test_resource_iterator():
    resources = ocldev.oclresourcelist.OclResourceList()
    resource_a = {'resource_type': 'Concept', 'id': 'A', 'name': 'Adam', 'owner_id': 'PEPFAR', 'source': 'PLM'}
    resource_b = {'resource_type': 'Mapping', 'id': 'B', 'name': 'Bob', 'owner_id': 'PEPFAR', 'source': 'PLM'}
    resources.append(resource_a)
    resources.append(resource_b)
    count = 0
    for resource in resources:
        count += 1
        print resource
    assert count == len(resources)


def test_csv_to_json_conversion():
    csv_resources = ocldev.oclresourcelist.OclCsvResourceList()
    csv_resource_a = {
        'resource_type': 'Concept',
        'id': 'A',
        'name': 'Adam',
        'owner_id': 'PEPFAR',
        'source': 'PLM',
        'concept_class': 'Misc',
        'datatype': 'Numeric',
        'attr:MyAttribute': 'My custom value',
        'map_type[1]': 'Same As',
        'map_to_concept_url[1]': '/orgs/CIEL/sources/CIEL/concepts/1013/'
    }
    csv_resources.append(csv_resource_a)
    json_resources = csv_resources.convert_to_ocl_formatted_json()
    print json_resources.to_json()
    expected_json_output = [
        {
            'type': 'Concept',
            'owner': 'PEPFAR',
            'owner_type': 'Organization',
            'source': 'PLM',
            'id': 'A',
            'concept_class': 'Misc',
            'datatype': 'Numeric',
            'names': [{'locale': 'en', 'locale_preferred': True, 'name': 'Adam', 'name_type': 'Fully Specified'}],
            'extras': {'MyAttribute': 'My custom value'},
        },
        {
            'type': 'Mapping',
            'owner': 'PEPFAR',
            'owner_type': 'Organization',
            'source': 'PLM',
            'from_concept_url': '/orgs/PEPFAR/sources/PLM/concepts/A/',
            'map_type': 'Same As',
            'to_concept_url': '/orgs/CIEL/sources/CIEL/concepts/1013/',
        }
    ]
    assert expected_json_output == json_resources.to_json()

