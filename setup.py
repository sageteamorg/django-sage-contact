from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django_sage_contact",
    version="0.4.5",
    author="Sepehr Akbarzadeh",
    author_email="sepehr@sageteam.org",
    description="Django package to handle user contact information and contact form.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sageteamorg/django-sage-contact",
    project_urls={
        "Documentation": "https://django-sage-contact.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/sageteamorg/django-sage-contact",
        "Issues": "https://github.com/sageteamorg/django-sage-contact/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.11",
)
