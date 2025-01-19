import trimesh
import sys
import os

def convert(input_filename,output_filename):
    print("Converting ",input_filename," to ",output_filename)
    mesh = trimesh.load(input_filename)
    mesh.export(output_filename,"stl")

def convertFolder(folder_path):
    files = [e for e in os.listdir(folder_path) if e.endswith(".obj")]
    if(folder_path.endswith("/") == False):
        folder_path += "/"
    for e in files:
        input_filename = folder_path + e
        output_filename = folder_path + e.rstrip(".obj") + ".stl"
        convert(input_filename,output_filename)


def printInvalidUsage():
    print("Invalid usage:")
    print("python obj2stl.py <FolderName>")


if __name__ == '__main__':

    if(len(sys.argv) != 2):
        printInvalidUsage()
        exit(-1)
   
    if(os.path.isdir(sys.argv[1]) == False ):
        print(sys.argv[1], " <-- folder does not exist")
        printInvalidUsage()
        exit(-1)

    convertFolder(sys.argv[1])

