import inspect, shutil
from add_mesh_rocks import utils
from xml.dom import minidom

basePath = inspect.getfile(inspect.currentframe())[0:-len("settings.py")]
path = basePath + "add_mesh_rocks.xml"

try:
    source = minidom.parse(path)
    print("Rock generator settings file found:\n" + path)
except:
    print("Rock generator settings file not found.  Creating settings file.")
    shutil.copy(basePath + "factory.xml", path)
    source = minidom.parse(path)

xmlDefault = source.getElementsByTagName('default')[0]
xmlPresets = source.getElementsByTagName('preset')
default = []
presets = []

#----- Gets and Sets -----#

def getDefault():
    global default    
    return default

def getPresetLists():
    global presets
    return presets

def getPreset(ID = 0):
    global presets
    return presets[ID]

#---------- Core ----------#

def parse():
    global xmlDefault
    global xmlPresets
    global default
    global presets

    # Parse default values
    default = parseNode(xmlDefault)

    # Parse preset values
    for setting in xmlPresets:
        presets.append(parseNode(setting))
    
    return '{FINISHED}'

# Takes a node and parses it for data.  Relies on that setting.xml has
#   a valid format as specified by the DTD.
# For some reason minidom places an empty child node for every other node.
def parseNode(setting, title = True):
    loc = 1
    
    if title:
        # Preset name (xmlPreset.childNodes[1]):
        title = setting.childNodes[loc].childNodes[0].data
        loc += 2
        
    # Preset size values (xmlPreset.childNodes[3]):
    scaleX = [float(setting.childNodes[loc].childNodes[1].childNodes[3].childNodes[0].data),
              float(setting.childNodes[loc].childNodes[1].childNodes[5].childNodes[0].data)]
    scaleY = [float(setting.childNodes[loc].childNodes[3].childNodes[3].childNodes[0].data),
              float(setting.childNodes[loc].childNodes[3].childNodes[5].childNodes[0].data)]
    scaleZ = [float(setting.childNodes[loc].childNodes[5].childNodes[3].childNodes[0].data),
              float(setting.childNodes[loc].childNodes[5].childNodes[5].childNodes[0].data)]
    skewX = float(setting.childNodes[loc].childNodes[7].childNodes[3].childNodes[0].data)
    skewY = float(setting.childNodes[loc].childNodes[9].childNodes[3].childNodes[0].data)
    skewZ = float(setting.childNodes[loc].childNodes[11].childNodes[3].childNodes[0].data)
    if setting.childNodes[loc].childNodes[13].childNodes[0].data == 'False':
        use_scale_dis = False
    else:
        use_scale_dis = True
    scale_fac = utils.toList(setting.childNodes[loc].childNodes[15].childNodes[0].data)
    loc += 2
    
    # Presst shape values (xmlPreset.childNodes[5]):
    deform = float(setting.childNodes[loc].childNodes[1].childNodes[0].data)
    rough = float(setting.childNodes[loc].childNodes[3].childNodes[0].data)
    detail = int(setting.childNodes[loc].childNodes[5].childNodes[0].data)
    display_detail = int(setting.childNodes[loc].childNodes[7].childNodes[0].data)
    smooth_fac = float(setting.childNodes[loc].childNodes[9].childNodes[0].data)
    smooth_it = int(setting.childNodes[loc].childNodes[11].childNodes[0].data)
    loc += 2
    
    # Preset material values (xmlPreset.childNodes[7]):
    if setting.childNodes[loc].childNodes[1].childNodes[0].data == 'False':
        mat_enable = False
    else:
        mat_enable = True
    mat_color = utils.toList(setting.childNodes[loc].childNodes[3].childNodes[0].data)
    mat_bright = float(setting.childNodes[loc].childNodes[5].childNodes[0].data)
    mat_rough = float(setting.childNodes[loc].childNodes[7].childNodes[0].data)
    mat_spec = float(setting.childNodes[loc].childNodes[9].childNodes[0].data)
    mat_hard = int(setting.childNodes[loc].childNodes[11].childNodes[0].data)
    mat_mossy = float(setting.childNodes[loc].childNodes[13].childNodes[0].data)
    loc += 2

    # Preset random values (xmlPreset.childNodes[9]):
    if setting.childNodes[loc].childNodes[1].childNodes[0].data == 'False':
        use_random_seed = False
    else:
        use_random_seed = True
    user_seed = int(setting.childNodes[loc].childNodes[3].childNodes[0].data)

    if title:
        parsed = [title, scaleX, scaleY, scaleZ, skewX, skewY, skewZ, use_scale_dis, scale_fac,
                  deform, rough, detail, display_detail, smooth_fac, smooth_it,
                  mat_enable, mat_color, mat_bright, mat_rough, mat_spec, mat_hard,
                  mat_mossy, use_random_seed, user_seed]
    else:
        parsed = [scaleX, scaleY, scaleZ, skewX, skewY, skewZ, use_scale_dis, scale_fac,
                  deform, rough, detail, display_detail, smooth_fac, smooth_it,
                  mat_enable, mat_color, mat_bright, mat_rough, mat_spec, mat_hard,
                  mat_mossy, use_random_seed, user_seed]

    return parsed

def save():
    return '{FINISHED}'

def _print():
    for i in presets:
        print(i)
    return '{FINISHED}'
