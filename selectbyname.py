bl_info = {  
 "name": "Batch Selection by Name",  
 "author": "Bastian Ilso (bastianilso)",  
 "version": (0, 1),  
 "blender": (2, 7, 8),  
 "location": "3D View -> Select -> Select by Name",  
 "description": "Adds a Select by Name option to Select Menu and the Shift+G menu.",
 "tracker_url": "https://github.com/bastianilso/blender-enhanced-group-select",  
 "category": "Object"}

import bpy
import string

addon_keymaps = []

class SelectByName(bpy.types.Operator):
    """Select Objects with Similar Name"""
    bl_idname = "object.select_by_name"
    bl_label = "Select by Name"

    def execute(self, context):
        if not bpy.context.active_object:
            return {'FINISHED'}

        name = bpy.context.active_object.name
        name = ''.join(name.split("."))
        name = ''.join([i for i in name if not i.isdigit()])

        for ob in bpy.context.scene.objects:
            obname = ''.join(ob.name.split("."))
            obname = ''.join([i for i in obname if not i.isdigit()])
            if name == obname:
                print(obname)
                ob.select = True
        
        return {'FINISHED'}

class SelectGroupedEnhancedMenu(bpy.types.Menu):
    bl_label = "Select Grouped (Enhanced)"
    bl_idname = "view3d.mymenu"

    def draw(self, context):
        layout = self.layout

        layout.operator_enum("object.select_grouped", "type")
        layout.operator("object.select_by_name")
        
        
def menu_func_select(self, context):    
    self.layout.operator(SelectByName.bl_idname, text="Select by Name")
        
        
def register():
    bpy.utils.register_class(SelectGroupedEnhancedMenu)
    bpy.utils.register_class(SelectByName)
    bpy.types.VIEW3D_MT_select_object.append(menu_func_select)    

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'G', 'PRESS', shift = True)
        kmi.properties.name = "view3d.mymenu"

def unregister():
    bpy.utils.unregister_class(SelectGroupedEnhancedMenu)
    bpy.utils.register_class(SelectByName)
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
