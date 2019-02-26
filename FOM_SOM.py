import numpy as np
import scipy.sparse as sp
import scipy.io as spio
import matplotlib.pyplot as plt
import pandas as pd

def parsing_material_data(material_text, new_file):
    with open(material_text, "r") as stuff_to_write:
        with open(new_file, "w") as stuff_written:
            in_sequence = False
            in_thermal_properties = False
            for line in stuff_to_write:
                if line.startswith(",,,"):
                    in_sequence = True
                elif "General information" in line or "Composition overview" in line:
                    in_sequence = False
                elif "Thermal properties" in line:
                    in_thermal_properties = True
                elif "Electrical properties" in line:
                    in_thermal_properties = False
                elif "Density" in line:
                    stuff_written.write(line)
                elif in_sequence is True or in_thermal_properties is True:
                    stuff_written.write(line)

def parsing_refined_data(new_file):
    material_labels = []
    density_values = []
    melting_values = []
    therm_cond_values = []
    spec_heat_cap_values = []
    with open(new_file, "r") as sample_info:
        for line in sample_info:
            if line.startswith("done"):
                for line_item in range(1, len(line.split(',"'))):
                    material_labels.append(line.split(',"')[line_item].strip('" '))
                #print(len(material_labels))
                #2722 materials in the lists material_labels, density_values, melting_values, therm_cond_values,
            elif line.startswith("Density"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if "-" in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split("-")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split("-")[1]
                        density_values.append((float(left_of_dash) + float(right_of_dash)) / 2)
                    else:
                        density_values.append(float(line.split(",")[line_item].strip(" ")))
            elif line.startswith("Melting"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if "-" in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split("-")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split("-")[1]
                        melting_values.append((float(left_of_dash) + float(right_of_dash)) / 2)
                    else:
                        melting_values.append(float(line.split(",")[line_item].strip(" ")))
            elif line.startswith("Thermal conductivity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if "-" in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split("-")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split("-")[1]
                        therm_cond_values.append((float(left_of_dash) + float(right_of_dash)) / 2)
                    else:
                        therm_cond_values.append(float(line.split(",")[line_item].strip(" ")))
            elif line.startswith("Specific heat capacity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if "-" in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split("-")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split("-")[1]
                        spec_heat_cap_values.append((float(left_of_dash) + float(right_of_dash)) / 2)
                    else:
                        spec_heat_cap_values.append(float(line.split(",")[line_item].strip(" ")))
            #Not all materials have a latent heat of fusion!!!
    return(material_labels, density_values, melting_values, therm_cond_values, spec_heat_cap_values)
    
if __name__=="__main__":
    list_of_materials, list_of_densities, list_of_melting_points, list_of_therm_cond, list_of_heat_cap = parsing_refined_data("data/new_PCM.csv")
    print(len(list_of_materials), len(list_of_densities), len(list_of_melting_points), len(list_of_therm_cond), len(list_of_heat_cap))
    print(list_of_heat_cap[19])

