import pathlib
from setuptools import setup, find_packages
from importlib.metadata import entry_points

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# The text of the README file
REQUIRE = (HERE / "requirements.txt").read_text()

# Replace 'your_script_name' with the actual name of your script (without .py)
script_name = 'kavi'

setup(
    name=script_name,
    version='0.0.1',  # You can change this to a more specific version number
    packages=find_packages(),
    package_data={
    "": ["config.json"]  # Include config.json in the package
    },
    py_modules=[script_name],
    # Add any additional dependencies your script requires in the list below
    install_requires = REQUIRE,
    entry_points={
        "console_scripts":[
            "kavi=kavi:main",
        ]
    }
)