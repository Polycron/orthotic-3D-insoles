
# Disclaimer: I had no Idea what I was doing. I just coded this script to not have to do it all by hand in Meshlab
# Don't expect anything fancy really, but it "works" somehow. If it makes sense in a anatomical way is up to the debate!
# The Output file is meant to be part of an orthotic insole, it is meant to be 3D printed in a suitable material.

import pymeshlab  # Meshlab
import polyscope  # 3D GUI         or import "as MeshSet"? I have no Idea


MeshSet = pymeshlab.MeshSet()  # class containing all meshes
Percentage = pymeshlab.Percentage # something for percentage values at some point (no idea)
polyscope.set_up_dir("neg_z_up")  # set "upwards" direction in polyscope
polyscope.init()


# Begin declaration of functions

def LoadMesh():                                             # Load Mesh
    Dateiname = input("Geben sie den Namen der Datei ein:/Input Filename:")
    MeshSet.load_new_mesh(Dateiname)
    #polyscope.set_autocenter_structures(True)
    MeshSet.compute_matrix_from_scaling_or_normalization(scalecenter=1, uniformflag=1, axisx=skalierungsfaktor)
    MeshSet.meshing_decimation_quadric_edge_collapse(targetfacenum=75000)
    #MeshSet.set_current_mesh(0)
    #MeshSet.meshing_decimation_clustering(threshold=Percentage(0.5))
    return


def ShowInPolyscope():                                     #show what has happened in Polyscope (3D GUI)
    MeshSet.current_mesh()
    MeshSet.show_polyscope()
    return


def RotateToFitOnXYPlane():                                #Rotate the Scan of the foot
    MeshSet.set_current_mesh(0)
    MeshSet.compute_selection_from_mesh_border()
    #MeshSet.compute_matrix_by_principal_axis()
    #ShowInPolyscope()
    MeshSet.compute_matrix_by_fitting_to_plane(targetplane='XY plane', rotaxis='Z axis', toorigin=True)
    ShowInPolyscope()
    #MeshSet.compute_matrix_by_fitting_to_plane(targetplane='XY plane', rotaxis='X axis', toorigin=True)
    #ShowInPolyscope()
    #MeshSet.compute_matrix_by_principal_axis()
    #ShowInPolyscope()
    #MeshSet.compute_matrix_from_rotation(rotaxis=2, rotcenter=1, angle=90)
    #ShowInPolyscope()
    return


def CreatePlaneOnBorder():                                  #Creates A Plane that covers the whole scan
    MeshSet.compute_selection_from_mesh_border()
    MeshSet.generate_plane_fitting_to_selection(extent=1.2, subdiv=60, orientation=1)
    return


def ColorizeMesh0():                                        #colorizes the Mesh according to the euclidean distance to the Plane
    MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=1, radius=laenge/4)
    return


def MoveSelectedFacesToAnotherLayer():                      #For editing certain parts of the mesh
    MeshSet.generate_from_selected_faces(deleteoriginal=True)
    return


def SaveCurrentMesh():                                      #For creating a printable file format
    MeshSet.save_current_mesh(file_name="Output.stl", save_textures=True)
    return


#Begin Inputs
print("Geben sie die gemessene Länge in mm ein:/Input the Length")
laenge = float(input())

while laenge > 400 or laenge < 200:
    print("Geben sie einen Wert zwischen 200 und 400mm ein:/Input a value between 200 and 400mm:")
    laenge = float(input())
else:
    print("Input:", laenge, "mm laenge")

    print("Geben sie die gemessene Fußlänge aus Meshlab ein:/Input the length of the foot in Meshlab:")
    laengemeshlab = float(input())
    print("Input:", laengemeshlab, "Meshlab units")

    skalierungsfaktor = laenge / laengemeshlab

    print("Skalierungsfaktor berechnet/Factor for scaling calculated")

    print("geben sie links oder rechts ein/input left or right foot")

'''
lire = str(input())
while lire != "links" or lire !="L" or lire != "l" or lire !="rechts" or lire !="R" or lire != "r": #bullshit i guess
    print("Eingabe ungültig.")
    lire = str(input())

else:
'''

lire = str(input())
if lire == "links" or lire == "L" or lire == "l":
    print("sie haben ", lire, " eingegeben.")
    angle1 = float(-39)
    angle2 = float(-2.5)
    angle21 = float(2.5)
    #angle21 = float(-8.5) #0 für Torsionsschnitt, 7.5 normal
    angle3 = float(17.5)

elif lire == "rechts" or lire == "R" or lire == "r":
    print("sie haben ", lire, " eingegeben.")
    angle1 = float(-39)
    angle2 = float(2.5)
    angle21 = float(-2.5)
    #angle21 = float(8.5) #0 für Torsionsschnitt, -7.5 normal
    angle3 = float(-17.5)


# Berechnungen der Höhen für das Ebenenkonstrukt
x10 = (10 / 270) * laenge

LoadMesh()
ShowInPolyscope()
MeshSet.set_current_mesh(0)
CreatePlaneOnBorder()
ColorizeMesh0()
RotateToFitOnXYPlane()
MeshSet.set_current_mesh(0)
MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.125, percentbv=1, colorspace=0)
MeshSet.meshing_remove_selected_vertices_and_faces()
MeshSet.compute_scalar_by_border_distance_per_vertex()
ShowInPolyscope()

MeshSet.set_current_mesh(1)
MeshSet.delete_current_mesh()
MeshSet.set_current_mesh(0)


#speichern des ausgerichteten Scans
MeshSet.set_current_mesh(0)
#MeshSet.meshing_invert_face_orientation(forceflip=True)
#MeshSet.save_current_mesh(file_name="straight.stl", save_textures=False)
MeshSet.save_current_mesh(file_name="straight.ply", save_textures=False)


# Start plane construct
MeshSet.set_current_mesh(0)
CreatePlaneOnBorder()

MeshSet.set_current_mesh(2)
MeshSet.generate_copy_of_current_mesh()  # 3
MeshSet.generate_copy_of_current_mesh()  # 4
MeshSet.generate_copy_of_current_mesh()  # 5
MeshSet.generate_copy_of_current_mesh()  # 6

MeshSet.set_current_mesh(2)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-x10)
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=angle1)  #front
MeshSet.compute_matrix_from_rotation(rotaxis=1, rotcenter=1, angle=angle2)  #front tilt

MeshSet.set_current_mesh(6)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-x10)
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=angle1)  #second front
MeshSet.compute_matrix_from_rotation(rotaxis=1, rotcenter=1, angle=angle21) #second front tilt

MeshSet.set_current_mesh(3)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-0)
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=-5)      #arc tilt
MeshSet.compute_matrix_from_rotation(rotaxis=1, rotcenter=1, angle=angle3)  #arc

MeshSet.set_current_mesh(4)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-0)            #base plane
# MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=-5)

MeshSet.set_current_mesh(5)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-x10)          #heel
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=7.5)
print("planes contructed")


ShowInPolyscope()


# Start selection
MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(0)

MeshSet.generate_by_merging_visible_meshes(mergevisible=1, deletelayer=True)

MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(1)

MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=7, radius=2*laenge)  #!radius
MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.9, percentbv=1, colorspace=1)
MeshSet.generate_from_selected_faces(deleteoriginal=0)  # 8 Mesh


print("Selection 0")
# End selection 0

ShowInPolyscope()                                                           #here you will see what this is for

# Start Auswahl 1
MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(1)

MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=7, radius=2*laenge)  #!radius
MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.95, percentbv=1, colorspace=1)
MeshSet.generate_from_selected_faces(deleteoriginal=0)  # 9 Mesh


print("Selection 1")
# Ende Auswahl 1                                                            #same thing for different thickness

ShowInPolyscope()

MeshSet.set_current_mesh(8)
MeshSet.compute_selection_by_small_disconnected_components_per_face(nbfaceratio=0.9, nonclosedonly=1)
MeshSet.meshing_remove_selected_vertices_and_faces()
MeshSet.set_current_mesh(9)
MeshSet.compute_selection_by_small_disconnected_components_per_face(nbfaceratio=0.9, nonclosedonly=1)
MeshSet.meshing_remove_selected_vertices_and_faces()
print("Überschüssige Auswahl entfernt")

ShowInPolyscope()

# Start smoothing and volumetrisation
MeshSet.set_current_mesh(8)
MeshSet.apply_coord_taubin_smoothing(lambda_=1, stepsmoothnum=50)
MeshSet.set_current_mesh(9)
MeshSet.apply_coord_taubin_smoothing(lambda_=1, stepsmoothnum=50)
print("Glätten erfolgreich")

ShowInPolyscope()

MeshSet.set_current_mesh(8)
MeshSet.generate_resampled_uniform_mesh(cellsize=Percentage(0.25), offset=Percentage(51.75), absdist=1)
MeshSet.set_current_mesh(9)
MeshSet.generate_resampled_uniform_mesh(cellsize=Percentage(0.125), offset=Percentage(51.0), absdist=1)
#Ende smoothing and volumetrisation

'''
MeshSet.set_current_mesh(8)
MeshSet.save_current_mesh(file_name="Mesh8.stl", save_textures=True)
MeshSet.set_current_mesh(9)
MeshSet.save_current_mesh(file_name="Mesh9.stl", save_textures=True)
'''

ShowInPolyscope()

# Verbinden
MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(0)
MeshSet.set_current_mesh(7)
MeshSet.set_current_mesh_visibility(0)
MeshSet.set_current_mesh(8)
MeshSet.set_current_mesh_visibility(0)
MeshSet.set_current_mesh(9)
MeshSet.set_current_mesh_visibility(0)
MeshSet.generate_by_merging_visible_meshes(mergevisible=1, deletelayer=True)
MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(1)


print("volumetrisation finished")
MeshSet.set_current_mesh(12)
# MeshSet.meshing_decimation_clustering(threshold=Percentage(0.95))
MeshSet.meshing_decimation_quadric_edge_collapse(targetfacenum=10000)
# MeshSet.compute_matrix_from_rotation(rotaxis="X axis", rotcenter="barycenter", snapflag=False, angle=180)
# MeshSet.set_current_mesh(0) #8 small insole cutout; 9 large cutout; 10 meshed 8; 11 meshed 9
SaveCurrentMesh()
print("Saving successfull, opening polyscope")
ShowInPolyscope()

'''
MeshSet.set_current_mesh()
print(MeshSet.current_mesh_id())
Author left 14.119 und 282
Author right 14.006 und 280
'''
