import re
import pandas as pd
import numpy as np

COLUMN_NAMES = [
    'Material family',
    'Youngs modulus',
    'Specific stiffness',
    'Yield strength',
    'Tensile strength',
    'Specific strength',
    'Elongation',
    'Compressive strength',
    'Flexural modulus',
    'Flexural strength',
    'Shear modulus',
    'Bulk modulus',
    'Poisson ratio',
    'Shape factor',
    'Hardness vickers',
    'Elastic stored energy',
    'Fatigue strength',
    'Fracture toughness',
    'Toughness',
    'Ductility index',
    'Melting point',
    'Max service temp',
    'Min service temp',
    'Thermal conductivity',
    'Specific heat capacity',
    'Thermal expansion coefficient',
    'Thermal shock resistance',
    'Thermal distortion resistance',
    'Latent heat of fusion',
    'Electrical resistivity',
    'Electrical conductivity',
    'Galvanic potential',
    'Mechanical loss coefficient',
]

BAD_PROPERTIES = [
    'Elongation', # This is because there's over 600 bad properties in the dataset
    'Hardness vickers',
    # not worth saving
    'Specific stiffness',
    'Specific strength',
    'Shape factor',
    'Elastic stored energy',
    'Toughness',
    'Ductility index',
    'Thermal shock resistance',
    'Thermal distortion resistance',
    # These properties are not actually real properties of the material
    'Max service temp',
    'Min service temp',
    'Electrical resistivity',
    # This really messes with our data selection
    'Galvanic potential',
]

# These are materials with invalid values for one or more properties
# This entry is here because there's materials with higher, but valid values
# And I don't want to lose them
BAD_MATERIALS = [
    "PEEK/IM carbon fiber, UD prepreg, UD lay-up"
]

def parsing_material_data(material_text, new_file):
    with open(material_text, "r") as stuff_to_write:
        with open(new_file, "w") as stuff_written:
            in_thermal_properties = False
            in_electrical_properties = False
            in_mechanical_properties = False
            in_impact_properties = False
            for line in stuff_to_write:
                if line.startswith("done"):
                    stuff_written.write(line)
                elif "Mechanical properties" in line:
                    in_mechanical_properties = True
                elif "Impact & fracture properties" in line:
                    in_mechanical_properties = False
                    in_impact_properties = True
                elif "Thermal properties" in line:
                    in_thermal_properties = True
                    in_impact_properties = False
                elif "Electrical properties" in line:
                    in_thermal_properties = False
                    in_electrical_properties = True
                elif "Magnetic properties" in line:
                    in_electrical_properties = False
                    in_mechanical_properties = False
                    in_thermal_properties = False
                    in_impact_properties = False
                elif "Mechanical loss coefficient" in line:
                    stuff_written.write(line)
                elif line.startswith("Material family"):
                    stuff_written.write(line)
                elif in_thermal_properties is True or in_electrical_properties is True or in_mechanical_properties is True or in_impact_properties is True:
                    stuff_written.write(line)

def parsing_refined_data(new_file):
    material_name = []
    material_family = []
    young_modulus_values = []
    specific_stiffness_values = []
    yield_strength_values = []
    tensile_strength_values = []
    specific_strength_values = []
    elongation_values = []
    compressive_strength_values = []
    flexural_modulus_values = []
    flexural_strength_values = []
    shear_modulus_values = []
    bulk_modulus_values = []
    poisson_ratio_values = []
    shape_factor_values = []
    hardness_vickers_values = []
    elastic_stored_energy_values = []
    fatigue_strength_values = []
    fracture_toughness_values = []
    toughness_values = []
    ductility_index_values = []
    melting_values = []
    max_service_temp_values = []
    min_service_temp_values = []
    therm_cond_values = []
    spec_heat_cap_values = []
    therm_expan_coeff_values = []
    therm_shock_resist_values = []
    therm_dist_resist_values = []
    latent_heat_fusion_values = []
    elec_resist_values = []
    elec_cond_values = []
    galvanic_potential_values = []
    mech_loss_coeff_values = []
    with open(new_file, "r") as sample_info:
        for line in sample_info:
            if line.startswith("done"):
                for line_item in range(2, len(line.split('  '))):
                    material_name.append((line.split('  ')[line_item].strip('" ,\t\n')))
            elif line.startswith("Material family"):
                for line_item in range(1, len(line.split('  ')) - 1):
                    material_family.append(line.split('  ')[line_item].strip(' ",\t\n'))
            elif line.startswith("Young's modulus (10^6 psi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        young_modulus_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        young_modulus_values.append("Null")
                    else:
                        young_modulus_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Specific stiffness (lbf.ft/lb)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        specific_stiffness_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        specific_stiffness_values.append("Null")
                    else:
                        specific_stiffness_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Yield strength (elastic limit) (ksi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        yield_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        yield_strength_values.append("Null")
                    else:
                        yield_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Tensile strength (ksi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        tensile_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        tensile_strength_values.append("Null")
                    else:
                        tensile_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Specific strength (lbf.ft/lb)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        specific_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        specific_strength_values.append("Null")
                    else:
                        specific_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Elongation (% strain)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        elongation_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        elongation_values.append("Null")
                    else:
                        elongation_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Compressive strength (ksi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        compressive_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        compressive_strength_values.append("Null")
                    else:
                        compressive_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Flexural modulus (10^6 psi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        flexural_modulus_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        flexural_modulus_values.append("Null")
                    else:
                        flexural_modulus_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Flexural strength (modulus of rupture) (ksi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        flexural_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        flexural_strength_values.append("Null")
                    else:
                        flexural_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Shear modulus (10^6 psi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        shear_modulus_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        shear_modulus_values.append("Null")
                    else:
                        shear_modulus_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Bulk modulus (10^6 psi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        bulk_modulus_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        bulk_modulus_values.append("Null")
                    else:
                        bulk_modulus_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Poisson's ratio"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        poisson_ratio_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        poisson_ratio_values.append("Null")
                    else:
                        poisson_ratio_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Shape factor"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        shape_factor_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        shape_factor_values.append("Null")
                    else:
                        shape_factor_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Hardness - Vickers (HV)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        hardness_vickers_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        hardness_vickers_values.append("Null")
                    else:
                        hardness_vickers_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Elastic stored energy (springs) (ft.lbf/in^3)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        elastic_stored_energy_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        elastic_stored_energy_values.append("Null")
                    else:
                        elastic_stored_energy_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Fatigue strength at 10^7 cycles (ksi)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        fatigue_strength_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        fatigue_strength_values.append("Null")
                    else:
                        fatigue_strength_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Fracture toughness (ksi.in^0.5)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        fracture_toughness_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        fracture_toughness_values.append("Null")
                    else:
                        fracture_toughness_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Toughness (G) (ft.lbf/in^2)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        toughness_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        toughness_values.append("Null")
                    else:
                        toughness_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Ductility index (mil)"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        ductility_index_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        ductility_index_values.append("Null")
                    else:
                        ductility_index_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Melting"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        melting_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        melting_values.append("Null")
                    else:
                        melting_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Maximum service temperature"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        max_service_temp_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        max_service_temp_values.append("Null")
                    else:
                        max_service_temp_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Minimum service temperature"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        min_service_temp_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        min_service_temp_values.append("Null")
                    else:
                        min_service_temp_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Thermal conductivity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        therm_cond_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        therm_cond_values.append("Null")
                    else:
                        therm_cond_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Specific heat capacity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        spec_heat_cap_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        spec_heat_cap_values.append("Null")
                    else:
                        spec_heat_cap_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Thermal expansion coefficient"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        therm_expan_coeff_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        therm_expan_coeff_values.append("Null")
                    else:
                        therm_expan_coeff_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Thermal shock resistance"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        therm_shock_resist_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        therm_shock_resist_values.append("Null")
                    else:
                        therm_shock_resist_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Thermal distortion resistance"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        therm_dist_resist_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        therm_dist_resist_values.append("Null")
                    else:
                        therm_dist_resist_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Latent heat of fusion"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        latent_heat_fusion_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        latent_heat_fusion_values.append("Null")
                    else:
                        latent_heat_fusion_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Electrical resistivity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        elec_resist_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        elec_resist_values.append("Null")
                    else:
                        elec_resist_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Electrical conductivity"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        elec_cond_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        elec_cond_values.append("Null")
                    else:
                        elec_cond_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Galvanic potential"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        galvanic_potential_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        galvanic_potential_values.append("Null")
                    else:
                        galvanic_potential_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            elif line.startswith("Mechanical loss coefficient"):
                for line_item in range(1, (len(line.split(",")) - 1)):
                    if " - " in line.split(",")[line_item].strip(" "):
                        left_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[0]
                        right_of_dash = line.split(",")[line_item].strip(" ").split(" - ")[1]
                        average_of_dash = (float(left_of_dash) + float(right_of_dash)) / 2
                        mech_loss_coeff_values.append(round(average_of_dash, 6))
                    elif line.split(",")[line_item] is '':
                        mech_loss_coeff_values.append("Null")
                    else:
                        mech_loss_coeff_values.append(round(float(line.split(",")[line_item].strip(" ")), 6))
            #Brinell Hardness, Dielectric Constant, Dielectric Strength, Dissipation Factor, excluded because lacking way too much data (>10 rows of materials non-existent)
    null_extender = ["Null"] * 18
    material_name.extend(null_extender)
    material_family.extend(null_extender)

    return(material_name, material_family, young_modulus_values, specific_stiffness_values, yield_strength_values,
           tensile_strength_values, specific_strength_values, elongation_values, compressive_strength_values,
           flexural_modulus_values, flexural_strength_values, shear_modulus_values, bulk_modulus_values,
           poisson_ratio_values, shape_factor_values, hardness_vickers_values,
           elastic_stored_energy_values, fatigue_strength_values, fracture_toughness_values, toughness_values,
           ductility_index_values, melting_values, max_service_temp_values, min_service_temp_values,
           therm_cond_values, spec_heat_cap_values, therm_expan_coeff_values, therm_shock_resist_values, therm_dist_resist_values,
           latent_heat_fusion_values, elec_resist_values, elec_cond_values, galvanic_potential_values, mech_loss_coeff_values)

def null_invalid_properties(frame: pd.DataFrame):
    # This drops elements in our dataset which have invalid values for any of the following properties
    # found to contain a salvagable amount of invalid data
    COLUMNS_TO_SCRUB = [
        "Tensile strength",
        "Compressive strength",
        "Flexural modulus",
        "Flexural strength",
        "Bulk modulus",
        "Elastic stored energy",
        "Fatigue strength",
        "Fracture toughness",
        "Toughness",
        "Thermal expansion coefficient",
        ]
    for c in COLUMNS_TO_SCRUB:
        # They're all some kind of number between 40k and 50k
        # with bias towards repeating values
        frame[c].mask(frame[c].gt(40000), inplace=True)
    
    # Be gingerly with this column because there's larger entries with valid values
    frame["Thermal shock resistance"].mask(frame["Thermal shock resistance"].eq(47650), inplace=True)
    frame["Fracture toughness"].mask(frame["Fracture toughness"].gt(12000), inplace=True)

def properties_dataframe_from_file(path: str):
    property_lists = parsing_refined_data(path)
    frame = pd.DataFrame(index=property_lists[0], data={
        k: v for (k, v) in zip(COLUMN_NAMES, property_lists[1:])
    })

    frame.replace("Null", np.nan, inplace=True)
    null_invalid_properties(frame)
    return frame



if __name__ == "__main__":
    parsing_material_data("C:/Users/Everet/Documents/AMP_Project/Pres_3/Updated_PCM.csv", "C:/Users/Everet/Documents/AMP_Project/Pres_3/new_TEM.csv")
    material_name, material_family, young_modulus_values, specific_stiffness_values, yield_strength_values, tensile_strength_values, specific_strength_values, elongation_values, compressive_strength_values, flexural_modulus_values, flexural_strength_values, shear_modulus_values, bulk_modulus_values, poisson_ratio_values, shape_factor_values, hardness_vickers_values, elastic_stored_energy_values, fatigue_strength_values, fracture_toughness_values, toughness_values, ductility_index_values, melting_values, max_service_temp_values, min_service_temp_values, therm_cond_values, spec_heat_cap_values, therm_expan_coeff_values, therm_shock_resist_values, therm_dist_resist_values, latent_heat_fusion_values, elec_resist_values, elec_cond_values, galvanic_potential_values, mech_loss_coeff_values = parsing_refined_data("C:/Users/Everet/Documents/AMP_Project/Pres_3/new_TEM.csv")
    print(len(material_name), len(material_family), len(young_modulus_values), len(specific_stiffness_values), len(yield_strength_values), len(tensile_strength_values))
    print(material_name[0])
    print(material_family[0])
    print(material_family[-4])
    print(set(material_family))
    #print(len(specific_strength_values), len(elongation_values), len(compressive_strength_values), len(flexural_modulus_values), len(flexural_strength_values))
    #print(len(shear_modulus_values), len(bulk_modulus_values), len(poisson_ratio_values), len(shape_factor_values), len(hardness_vickers_values))
    #print(len(elastic_stored_energy_values), len(fatigue_strength_values), len(fracture_toughness_values), len(toughness_values), len(ductility_index_values))
    #print(len(melting_values), len(max_service_temp_values), len(min_service_temp_values), len(therm_cond_values), len(spec_heat_cap_values))
    #print(len(therm_expan_coeff_values), len(therm_shock_resist_values), len(therm_dist_resist_values), len(latent_heat_fusion_values), len(elec_resist_values))
    #print(len(elec_cond_values), len(galvanic_potential_values), len(mech_loss_coeff_values))

    #33 properties total
