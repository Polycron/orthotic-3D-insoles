
#Disclaimer: I had no Idea what I was doing. I just coded this script to not have to do it all by hand in Meshlab
#Don't expect anything fancy really, but it "works" somehow. If it makes sense in a anatomical way is up to the debate!
#The Output file is meant to be part of a orthotic insole, it is meant to be 3D printed in a suitable material.

import pymeshlab  # Meshlab
import polyscope  # 3D GUI         or import "as MeshSet"? I have no Idea


MeshSet = pymeshlab.MeshSet()  #class containing all meshes
Percentage = pymeshlab.Percentage #something for percentage values at some point (no idea)
polyscope.set_up_dir("neg_z_up")  #set "upwards" direction in polyscope
polyscope.init()


# Begin declaration of functions

def LoadMesh():                                             #Load Mesh and decrease number of faces
    Dateiname = input("Geben sie den Namen der Datei ein:/Input Filename:")
    MeshSet.load_new_mesh(Dateiname)
    MeshSet.meshing_decimation_clustering(threshold=Percentage(0.75))
    MeshSet.compute_matrix_from_scaling_or_normalization(scalecenter=1, uniformflag=1, axisx=skalierungsfaktor)
    # MeshSet.meshing_decimation_quadric_edge_collapse(targetfacenum=10000)
    return

'''
def PrintLenghtOfMeshSet():
    MeshSet.__getitem__(0)
    var = len(MeshSet)                                      #no idea, didn't work i guess. Don't need it anyway
    print("Die Anzahl der Netzkörper beträgt:", var)
    return
'''

def ShowInPolyscope():                                      #show what has happened in Polyscope (3D GUI)
    MeshSet.current_mesh()
    MeshSet.show_polyscope()
    return


def RotateToFitOnXYPlane():                                 #Rotate the Scan of the foot (negative Z up)
    MeshSet.set_selection_all()                             #No idea how it works, but it's alway negative z up for all scans I had, so...
    # MeshSet.compute_selection_from_mesh_border()
    MeshSet.compute_matrix_by_principal_axis
    MeshSet.compute_matrix_by_fitting_to_plane(targetplane="XY plane", toorigin=True)
    MeshSet.compute_matrix_by_principal_axis
    MeshSet.compute_matrix_by_fitting_to_plane(targetplane="XY plane", toorigin=True)
    return


def CreatePlaneOnBorder():                                  #Creates A Plane that covers the whole scan. You will see why
    MeshSet.compute_selection_from_mesh_border()
    MeshSet.generate_plane_fitting_to_selection(extent=1, subdiv=60, orientation=1)
    return


def ColorizeMesh0():                                        #colorizes the Mesh according to the euclidean distance to the Plane
    MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=1)
    return


def SelectOverhang():                                       #Selects the unnecesary part of the scan to delete it afterwards
    MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.2, percentbv=1, colorspace=0)
    return


def MoveSelectedFacesToAnotherLayer():                      #For editing certain parts of the mesh
    MeshSet.generate_from_selected_faces(deleteoriginal=True)
    return


def SaveCurrentMesh():                                      #For creating a printable file format
    MeshSet.save_current_mesh(file_name="Output.stl", save_textures=True)
    return


# End of declaration of the functions (not all are being used i guess)


# Begin Inputs
print("Geben sie die gemessene Fußlänge in mm ein:/Input the Length of the Foot:")
fusslaenge = int(input())

while fusslaenge > 400 or fusslaenge < 200:
    print("Geben sie einen Wert zwischen 200 und 400mm ein:/Input a value between 200 and 400mm:")
    fusslaenge = int(input())
else:                                                                                   #This is for obtaining the scaling factor
    print("Input:", fusslaenge, "mm Footlength")

    print("Geben sie die gemessene Fußlänge aus Meshlab ein:/Input the length of the foot in Meshlab:")
    fusslaengemeshlab = float(input())
    print("Input:", fusslaengemeshlab, "Meshlab units")

    skalierungsfaktor = fusslaenge / fusslaengemeshlab                                  #for obtaining the scaling factor

    print("Skalierungsfaktor berechnet/Factor for scaling calculated")

    print("geben sie links oder rechts ein/input left or right foot")                   #<- Here you have to decide if left or right foot is being used

'''
lire = str(input())
while lire != "links" or lire !="L" or lire != "l" or lire !="rechts" or lire !="R" or lire != "r": #bullshit i guess
    print("Eingabe ungültig.")
    lire = str(input())

else:
'''

lire = str(input())                                                                      #input left or right
if lire == "links" or lire == "L" or lire == "l":
    print("sie haben ", lire, " eingegeben.")
    angle1 = float(-35)
    angle2 = float(-7.5)
    angle21 = float(7.5) #0 für Torsionsschnitt, 7.5 normal
    angle3 = float(17.5)
                                                                                        #values for either left or right foot
elif lire == "rechts" or lire == "R" or lire == "r":
    print("sie haben ", lire, " eingegeben.")
    angle1 = float(-35)
    angle2 = float(7.5)
    angle21 = float(-7.5) #0 für Torsionsschnitt, -7.5 normal
    angle3 = float(-17.5)
# Ende Eingaben


# Berechnungen der Höhen für das Ebenenkonstrukt
x70 = (70 / 270) * fusslaenge
x60 = (60 / 270) * fusslaenge
x50 = (50 / 270) * fusslaenge                           #fusslaenge = footlength
x40 = (40 / 270) * fusslaenge                           #some values, bullshit i guess
x30 = (30 / 270) * fusslaenge                           #This was for maintaining correct relative distances of the planes
x20 = (20 / 270) * fusslaenge
x10 = (10 / 270) * fusslaenge                           #only x10 is being used
# Ende der Berechnungen

LoadMesh()
ShowInPolyscope()

# begin cutting
MeshSet.set_current_mesh(0)
CreatePlaneOnBorder()  # Abdruck vom Überhang entfernen
ColorizeMesh0()
MeshSet.set_current_mesh(1)
MeshSet.delete_current_mesh()
MeshSet.set_current_mesh(0)
SelectOverhang()
MeshSet.meshing_remove_selected_vertices_and_faces()
print("cutting successful")
# end cutting

ShowInPolyscope()

RotateToFitOnXYPlane()

#MeshSet.save_current_mesh(file_name="Gedreht und geschnitten.stl", save_textures=True) #uncomment here for saving just the aligned Scan

ShowInPolyscope()

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
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=-3.5)    #arc tilt
MeshSet.compute_matrix_from_rotation(rotaxis=1, rotcenter=1, angle=angle3)  #arc

MeshSet.set_current_mesh(4)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-0)            #base plane
# MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=-5)

MeshSet.set_current_mesh(5)
MeshSet.compute_matrix_from_translation(traslmethod=0, axisz=-x10)          #heel
MeshSet.compute_matrix_from_rotation(rotaxis=0, rotcenter=1, angle=7.5)

print("planes contructed")
# End plane construct

ShowInPolyscope()                                                           #here you will see what this is

# Start selection

MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(0)

MeshSet.generate_by_merging_visible_meshes(mergevisible=1, deletelayer=True)

MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(1)

MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=7, radius=2*fusslaenge)  #!radius
MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.9, percentbv=1, colorspace=1)
MeshSet.generate_from_selected_faces(deleteoriginal=0)  # 8

print("Auswahl 0 getroffen")
# End selection 0

ShowInPolyscope()                                                           #here you will see what this is for

# Start Auswahl 1
MeshSet.set_current_mesh(0)
MeshSet.set_current_mesh_visibility(1)

MeshSet.compute_scalar_by_distance_from_point_cloud_per_vertex(coloredmesh=0, vertexmesh=7, radius=2*fusslaenge)  #!radius
MeshSet.compute_selection_by_color_per_face(percentrh=1, percentgs=0.95, percentbv=1, colorspace=1)
MeshSet.generate_from_selected_faces(deleteoriginal=0)  # 9

print("Auswahl 1 getroffen")
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
MeshSet.set_current_mesh(8)
MeshSet.generate_resampled_uniform_mesh(cellsize=Percentage(0.5), offset=Percentage(51.75), absdist=1)
MeshSet.set_current_mesh(9)
MeshSet.generate_resampled_uniform_mesh(cellsize=Percentage(0.25), offset=Percentage(51.25), absdist=1)
#Ende smoothing and volumetrisation

ShowInPolyscope()           #just take a look, it will make sense from now on

#Verbinden
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


print("Volumetrische Darstellung abgeschlossen")
MeshSet.set_current_mesh(12)
SaveCurrentMesh()
print("Speichern erfolgreich, öffne Polyscope:")
ShowInPolyscope()

'''
Author left foot Meshlab value: 14.119 units; Real life value: 282mm
Author right foot Meshlab value: 14.006 units; real life value: 280mm
'''