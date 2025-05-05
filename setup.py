from cx_Freeze import setup, Executable

# Define the list of dependencies to be included
includes = ["os", "json", "requests", "selenium", "datetime", "time", "apscheduler"]

# Create an executable
executables = [
    Executable(
        "client.py",  # Replace with the actual name of your Python script
        base=None,  # Replace with your desired base, e.g., "Console" for a console application
        # Replace with your desired executable name
    )
]

# Define options for freezing
options = {
    "build_exe": {
        "includes": includes,
        "packages": ["selenium.webdriver.common.by"],
    }
}

# Setup for cx_Freeze
setup(
    name="main",
    version="1.0",
    description="Your Application Description",
    options=options,
    executables=executables,
)
