import os
import nbformat as nbf

def create_notebook(output_path: str, 
                    platform: str,
                    device_name: str, 
                    device_version: str, 
                    from_date: str, 
                    to_date: str, 
                    current_release_link: str, 
                    previous_release_link: str,
                    current_release_server: str,
                    previous_release_server: str,
                    data_folder_path: str):
    """
    Generates notebook

    Args:
        output_path (str): Location where the generated notebook should be stored
        platform (str): Name of the platform, value should be iOS or Android
        device_name (str): Name of the device used to generate the EPT data
        device_version (str): OS and OS version of the device used to generate the EPT data
        from_date (str): Report start date
        to_date (str): Report end date
        current_release_link (str): Hockey app link for current release
        previous_release_link (str): Hockey app link for previous release
        current_release_server (str): Current release number for server
        previous_release_server (str): Previous release number for server
        data_folder_path (str): Path of the folder which contains splunk csv data files

    """
    if not os.path.isdir(output_path):
        print ("Unable to create notebook. %s path doesnot exists or is not a directory/folder." %output_path)
        return
    nb = nbf.v4.new_notebook()
    
    main_code_cell = """\
get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")

# Install the PyDrive wrapper & import libraries.
# This only needs to be done once per notebook.
!pip install -U -q PyDrive emoji
import emoji
import utils.utils
import utils.hockey_utils as hockeyutils
import pandas as pd
from utils.graph_utils import GraphUtils
from hockeyapp.api import Hockeyapp
from main.generate_metrics import MetricGenerator
from IPython.display import display, Markdown

current_info = hockeyutils.get_app_version('{current_release_link}')
previous_info = hockeyutils.get_app_version('{previous_release_link}')

current_version = current_info['version']
previous_version = previous_info['version']
current_build = current_info['build']
previous_build = previous_info['build']

last_release = '{{previous_version}}({{previous_build}})'.format(**vars())
this_release = '{{current_version}}({{current_build}})'.format(**vars())
last_server = pd.to_numeric('{previous_release_server}')
current_server = pd.to_numeric('{current_release_server}')

display(Markdown(\"""
# **The Salesforce {device_version} Release Freeze {{current_version}} Release Sign off Notebook**
### Device : {device_name} OS: {device_version}
### Data from : {from_date} to {to_date}
- [Link to Hockey App for {{current_version}}]({current_release_link})
- [Link to Hockey App for {{previous_version}}]({previous_release_link})
\n[Link](https://gus.lightning.force.com/lightning/r/ADM_Release__c/a01B0000003rGPlIAM/view) to the sign off record.
\nApp Version: {{current_version}} Build {{current_build}}\""".format(**vars())))

graph_utils = GraphUtils(last_release, this_release)
metric_gen = MetricGenerator("{platform}", last_release, this_release)

raw_data = metric_gen.load_data_from_folder('{data_folder_path}')
objecthome_raw = raw_data["OH"]
bootstrap_raw = raw_data["Bootstrap"]
feeds_raw = raw_data["MainFeed"]
coldstart_raw = raw_data["ColdStart"]
appstartup_raw = raw_data["AppStart"]
rh_cold = raw_data["RH_Cold"]
rh_warm = raw_data["RH_Warm"]

display(Markdown("# Aura Bootstrap"))
if "{platform}" == "iOS":
    metric_gen.generate_bootstrap_metric(bootstrap_raw, 10000, 10, 3500)
else:
    metric_gen.generate_bootstrap_metric(bootstrap_raw, 10000, 10, 3750)

""".format(platform=platform, device_name=device_name, device_version=device_version, from_date=from_date, to_date=to_date, current_release_link=current_release_link, previous_release_link=previous_release_link, current_release_server=current_release_server, previous_release_server=previous_release_server, data_folder_path=data_folder_path)
    
    objhome_code_cell = """\
display(Markdown("# Object Home"))
if "{platform}" == "iOS":
    metric_gen.generate_object_home_metric(objecthome_raw, 20000, 20, 800)
else:
    metric_gen.generate_object_home_metric(objecthome_raw, 20000, 20, 400)
    """.format(platform=platform)
    
    rhcold_code_cell = """\
display(Markdown("# RH Cold"))
metric_gen.generate_rh_cold_metric(rh_cold, 5000, 5)
    """

    rhwarm_code_cell = """\
display(Markdown("# RH Warm"))
metric_gen.generate_rh_warm_metric(rh_warm, 5000, 5)
    """
    
    mainfeed_code_cell = """\
display(Markdown("# Native Main Feed"))
metric_gen.generate_mainfeed_metric(feeds_raw, 10000, 10, 2500)
    """
    
    coldstart_code_cell = """\
display(Markdown("# Cold Start"))
metric_gen.generate_cold_start_metric(coldstart_raw, 20000, 20, 2500)
    """
    
    appstart_code_cell = """\
display(Markdown("# App Startup"))
if "{platform}" == "iOS":
    metric_gen.generate_app_start_metric(appstartup_raw, 20000, 20, 3500)
else:
    metric_gen.generate_app_start_metric(appstartup_raw, 20000, 20, 3750)
    """
    nb['cells']  = [nbf.v4.new_code_cell(main_code_cell),
                    nbf.v4.new_code_cell(objhome_code_cell),
                    nbf.v4.new_code_cell(rhcold_code_cell),
                    nbf.v4.new_code_cell(rhwarm_code_cell),
                    nbf.v4.new_code_cell(mainfeed_code_cell),
                    nbf.v4.new_code_cell(coldstart_code_cell),
                    nbf.v4.new_code_cell(appstart_code_cell)]

    fname = '/Notebook.ipynb'

    try:
        with open(output_path + fname, 'w') as f:
            nbf.write(nb, f)
    except Exception as e:
        print("create_notebook():: Error occured while generating notebook: ", e)