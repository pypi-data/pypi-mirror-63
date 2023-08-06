from setuptools import setup, find_packages
setup(
    name="amway_eap_migration",
    version="0.1",
    packages=['amway_eap_migration'],
    

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=["docutils>=0.3", "boto3>=1.10.45", "psycopg2==2.8.4"],

    # metadata to display on PyPI
    author="Jeff Allard",
    author_email="me@example.com",
    description="This is an Example Package",
  

    # could also include long_description, download_url, etc.
)