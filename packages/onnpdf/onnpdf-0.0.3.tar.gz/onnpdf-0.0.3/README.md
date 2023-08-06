# OzNetNerd PDF

Convenience Python module for creating templated PDF documents using `Jinja2` and `WeasyPrint`.

## Installation

```
pip3 install onnpdf
```

## Usage

Pass a dictionary into `onnpdf`, and it will:

1. Perform a "find and replace" operation (as well as other Jinja2 operations defined in your template)
2. Convert the template into a PDF document

Example dictionary as seen in [code snippets](examples/Demo%20Guide):

```
kv_pairs = {
    'title': 'OzNetNerd.com Demo PDF',
    'author': 'Will Robinson',
    'job_title': 'DevOps Specialist',
    'company': 'OzNetNerd.com',
    'email': 'will@oznetnerd.com',
    'phone': '+61 00 000 000',
    'website': 'https://oznetnerd.com'
}
```

## Example Document

The above produces [this PDF document.](examples/Demo%20Guide/outputs/demo.pdf)

## Example Use Case

Automate the creation of personalised lab guides for users. 

This enables lab admins to easily provide users with unique usernames, passwords, DNS entries, etc.

# Contact

* Blog: [oznetnerd.com](https://oznetnerd.com)
* Email: will@oznetnerd.com