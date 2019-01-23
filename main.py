#!/usr/bin/python

### import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.ViewingSetup import StereoViewingSetup
from lib.Scene import Scene
from lib.Inputs import Inputs
from lib.Navigation import NavigationManager

def start():


    ## create scenegraph
    scenegraph = avango.gua.nodes.SceneGraph(Name = "scenegraph")

    ## init scene
    scene = Scene(PARENT_NODE = scenegraph.Root.value)


    ## init viewing and interaction setups
    hostname = open('/etc/hostname', 'r').readline()
    hostname = hostname.strip(" \n")
    
    print("wokstation:", hostname)


    if hostname == "perseus": # Mitsubishi 3D-TV workstation
        _tracking_transmitter_offset = avango.gua.make_trans_mat(-0.98, -(0.58 + 0.975), 0.27 + 3.48) * avango.gua.make_rot_mat(90.0,0,1,0) # transformation into tracking coordinate system 

        viewingSetup = StereoViewingSetup(
            SCENEGRAPH = scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
            SCREEN_DIMENSIONS = avango.gua.Vec2(1.445, 0.81),
            #SCREEN_MATRIX = avango.gua.make_rot_mat(90.0,0,-1,0) * avango.gua.make_trans_mat(0.27 + 3.48, 0.975 + 0.58, 0.98), # screen offset matrix relative to navigation (tracking) coordinate system
            SCREEN_MATRIX = avango.gua.make_inverse_mat(_tracking_transmitter_offset), # screen offset matrix relative to navigation (tracking) coordinate system
            LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
            RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1920, 1080),
            STEREO_FLAG = True,
            STEREO_MODE = avango.gua.StereoMode.CHECKERBOARD,
            HEADTRACKING_FLAG = True,
            HEADTRACKING_STATION = "tracking-glasses-2", # wired 3D-TV glasses on Mitsubishi 3D-TV workstation
            )

        inputs = Inputs()
        inputs.init_projection_setup(
            POINTER_DEVICE_STATION = "device-pointer-2", # gyromouse pointer
            POINTER_TRACKING_STATION = "tracking-pointer-2", # gyromouse pointer
            KEYBOARD_STATION = "gua-device-keyboard",
        )
                        
    elif hostname == "andromeda": # ASUS 3D mirror display
        _tracking_transmitter_offset = avango.gua.make_rot_mat(12.46,1,0,0) * avango.gua.make_trans_mat(0.5, -(0.22 + 0.975), 0.39 + 3.48) * avango.gua.make_rot_mat(90.0,0,1,0) # transformation into tracking coordinate system 

        viewingSetup = StereoViewingSetup(
            SCENEGRAPH = scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(2560*2, 1440),
            SCREEN_DIMENSIONS = avango.gua.Vec2(0.595, 0.335),
            SCREEN_MATRIX = avango.gua.make_inverse_mat(_tracking_transmitter_offset), # screen offset matrix relative to navigation (tracking) coordinate system
            LEFT_SCREEN_POSITION = avango.gua.Vec2ui(0, 0),
            LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(2560, 1440),
            RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(2560, 1440),
            RIGHT_SCREEN_POSITION = avango.gua.Vec2ui(2560, 0),
            STEREO_FLAG = True,
            STEREO_MODE = avango.gua.StereoMode.SIDE_BY_SIDE,
            HEADTRACKING_FLAG = True,
            HEADTRACKING_STATION = "tracking-glasses-1", # ASUS 3D mirror display glasses
            )

        inputs = Inputs()
        inputs.init_projection_setup(
            POINTER_DEVICE_STATION = "device-pointer-1", # HAS pointer
            POINTER_TRACKING_STATION = "tracking-pointer-1", # HAS ppinter
            KEYBOARD_STATION = "gua-device-keyboard",
            )

    elif hostname == "athena": # small powerwall workstation
        viewingSetup = StereoViewingSetup(
            SCENEGRAPH = scenegraph,
            WINDOW_RESOLUTION = avango.gua.Vec2ui(1920*2, 1200),
            SCREEN_DIMENSIONS = avango.gua.Vec2(3.0, 2.0),
            SCREEN_MATRIX = avango.gua.make_trans_mat(0.0, 1.42, -1.6), # screen offset matrix relative to navigation (tracking) coordinate system
            LEFT_SCREEN_POSITION = avango.gua.Vec2ui(134, 1),
            LEFT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1770, 1175),
            RIGHT_SCREEN_POSITION = avango.gua.Vec2ui(1934, 0),
            RIGHT_SCREEN_RESOLUTION = avango.gua.Vec2ui(1765, 1165),
            STEREO_FLAG = True,
            STEREO_MODE = avango.gua.StereoMode.SIDE_BY_SIDE,
            HEADTRACKING_FLAG = True,
            HEADTRACKING_STATION = "tracking-glasses-3", # wired 3D-TV glasses on Samsung 3D-TV workstation
            )
           
        inputs = Inputs()
        inputs.init_projection_setup(
            POINTER_DEVICE_STATION = "device-pointer-3", # 2.4G pointer (green)
            POINTER_TRACKING_STATION = "tracking-pointer-3", # 2.4G pointer (green)
            KEYBOARD_STATION = "gua-device-keyboard",
        )
            

    else:
        print("No Viewing Setup available for this workstation")
        quit()


    ## init navigation techniques
    navigationManager = NavigationManager()
    navigationManager.my_constructor(
        SCENEGRAPH = scenegraph,
        VIEWING_SETUP = viewingSetup,
        INPUTS = inputs,
        )

    
    print_graph(scenegraph.Root.value)

    ## start application/render loop
    viewingSetup.run(locals(), globals())



### helper functions ###

## print the subgraph under a given node to the console
def print_graph(root_node):
  stack = [(root_node, 0)]
  while stack:
    node, level = stack.pop()
    print("│   " * level + "├── {0} <{1}>".format(
      node.Name.value, node.__class__.__name__))
    stack.extend(
      [(child, level + 1) for child in reversed(node.Children.value)])

## print all fields of a fieldcontainer to the console
def print_fields(node, print_values = False):
  for i in range(node.get_num_fields()):
    field = node.get_field(i)
    print("→ {0} <{1}>".format(field._get_name(), field.__class__.__name__))
    if print_values:
      print("  with value '{0}'".format(field.value))


if __name__ == '__main__':
  start()

