"""
PillowScreenX is a powerful screenshot capturing tool
that leverages the power of the Pillow library to provide high-quality screenshot captures.
With PillowScreenX, you can take full screenshots or capture specific regions
of your screen with ease. The module also provides options to store your screenshots
in a zip file or in a separate folder. Whether you need to capture screenshots for documentation,
debugging, or any other purpose, PillowScreenX is the ideal solution.
"""
import inspect
import os
import re
import time
from configparser import ConfigParser
from PIL import ImageGrab

config = ConfigParser()
config.read('config.ini')
CONFIG_DATA = {ea_section: config._sections.get(ea_section)  for ea_section in config.sections()}

# Default output folder
CONFIG_DATA.get('path').update({'output_folder': time.strftime("%Y%m%d_%H%M%S")})
USE_CASE_OUTPUT_FOLDER = CONFIG_DATA.get('path').get('output_folder')

class PillowScreenX:
    """
    PillowScreenX is a powerful screenshot capturing tool
    that leverages the power of the Pillow library to provide high-quality screenshot captures.
    """
    @classmethod
    def screenshot(cls, name: str = None, wait_time: float = 0.0) -> str:
        """
        Take the screenshot of the current page

        Args:
            name (str, optional): The name of the screenshot. Defaults to None.
        """
        # wait time before taking screenshot
        time.sleep(wait_time)

        calling_frame = inspect.stack()[1]
        current_file = calling_frame.filename

        # Get the current file name in which this code is present
        file_name = os.path.basename(current_file)[:-3]

        # Get the current working directory
        file_location = os.path.dirname(os.path.abspath(current_file))

        use_case_name = os.path.basename(file_location)
        category_name = os.path.basename(os.path.dirname(file_location))

        # Get only folders in {file_location} directory
        old_folders_in_current_dir = [f for f in os.listdir(file_location) \
                                        if os.path.isdir(os.path.join(file_location, f))]

        # delete the folders and its contents in {old_folders_in_current_dir} list
        for folder in old_folders_in_current_dir:
            # check folder name is in YYYYMMDD_HH format using regex
            if folder != USE_CASE_OUTPUT_FOLDER and re.match(r'\d{8}_\d{2}', folder):
                for file in os.listdir(f'{file_location}/{folder}'):
                    os.remove(f'{file_location}/{folder}/{file}')
                os.rmdir(f'{file_location}/{folder}')

        # folder_count = 0
        # if os.path.exists(f'{file_location}/{current_output_dir}'):
        #     folder_count = len([f for f in os.listdir(file_location) \
        #         if f.startswith(current_output_dir)]) + 1

        # if folder_count == 0:
        #     output_directory = f'{file_location}/{USE_CASE_OUTPUT_FOLDER}'
        # else:
        #     output_directory = f'{file_location}/{USE_CASE_OUTPUT_FOLDER}_({folder_count})'

        output_directory = f'{file_location}\{USE_CASE_OUTPUT_FOLDER}'
        # Create a folder named USE_CASE_FOLDER in the same directory as this file
        # If it doesn't already exist
        if not os.path.exists(f'{output_directory}'):
            os.makedirs(f'{output_directory}')

        if name is None:
            test_case_name = f'{file_name}'
        else:
            test_case_name = name

        # Save the screenshot to the USE_CASE_FOLDER folder
        use_case_output = f'{output_directory}\{test_case_name}.png'

        # if the file already exists, then add incrementing number to the file name
        if os.path.exists(use_case_output):
            # get the count of same file name
            file_count = len([f for f in os.listdir(f'{output_directory}') \
                        if f.startswith(file_name)]) + 1

            use_case_output = f'{output_directory}\{test_case_name}_({file_count}).png'

        # Print the screenshot path
        print(f'{category_name} | {use_case_name} | {file_name}\nScreenshot is saved at: {use_case_output}\n')

        return use_case_output

