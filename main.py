# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

from nvflare.lighter.impl.template import TemplateBuilder
from nvflare.lighter.spec import Provisioner
from nvflare.lighter.spec import Participant
from nvflare.lighter.spec import Study
from nvflare.lighter.provision import main as provisionMain
import yaml


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    '''workspace = os.getcwd()
    ctx = {"workspace": workspace}  # study is more static information while ctx is dynamic
    workspace = ctx.get("workspace")
    wip_dir = os.path.join(workspace, "wip")
    state_dir = os.path.join(workspace, "state")
    resources_dir = os.path.join(workspace, "resources")
    template_file = os.path.join(workspace, "master_template.yml")
    ctx.update(dict(wip_dir=wip_dir, state_dir=state_dir, resources_dir=resources_dir,template_file=template_file))
    #dirs = [workspace, resources_dir, wip_dir, state_dir]
    for item in ctx.keys():
        print(str(item) + ': ' + str(ctx[item]))
    
    VulnNVF = TemplateBuilder()
    VulnNVF.initialize(ctx)

    vulnProvisioner = Provisioner(workspace,[VulnNVF])

    Participant1 = Participant('admin','admin@NVFlare.Testing','NVFlareTesting')
    Study1 = Study('study1','This is a NVFlare test.',[Participant1])

    print("vulnProvisioner.ctx: " + str(vulnProvisioner.ctx))
    '''
    #vulnProvisioner.provision(Study1)
    #try:
    #    provisionMain()
    #except:
    #    print("Something else went wrong")


    #data = b"""!!python/object/apply:subprocess.Popen
    #- calc"""

    deserialized_data = yaml.load(open('Normal_project.yml','r'),yaml.Loader)  # deserializing data
    #deserialized_data = yaml.load(data, yaml.Loader)  # deserializing data
    #deserialized_data = yaml.safe_load(data)


    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
