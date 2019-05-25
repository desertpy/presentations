from configparser import ConfigParser

parser = ConfigParser()
found = parser.read('main.ini')

if not found:
    print('Configuration File Not found')
    parser.add_section('Section 1')
    parser.set('Section 1', 'option1', 'Value 1')
    parser.set('Section 1', 'option2', '300')

    parser.add_section('Section 2')
    parser.set('Section 2', 'option1', 'Value for Section 2 option 1')
    parser.set('Section 2', 'option2', 'Value for Section 2 option 2')
    with open('main.ini', 'w') as f:
        parser.write(f)
else:
    print(f'Configuration file exists {found}')
    for s in parser.sections():
        print(s)

    print('Access parser with a dictionary syntax')
    print(f"parser['Section 1']['option2'] = {parser['Section 1']['option2']}")

    # Update value with dictionary syntax
    parser['Section 2']['option2'] = 'Updated Value'

    with open('main.ini', 'w') as f:
        parser.write(f)