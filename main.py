
import json
import csv

from beam import (
    canti_udl,
    canti_end_point,
    ss_udl,
    ss_off_center_point,
    ss_center_point
)


with open("config.json", "r") as file:
    data = json.load(file)

E = float(data["material"]["E"])
I = float(data["material"]["I"])

spans = data["span"]
point_loads = data["Point_load"]
uniform_loads = data["uniformly_distributed_load"]

off_center_fraction = float(data["off_center_fraction"])

beam_cases = data["beam_cases"]

# Input validation(DID THIS FOR BUG FIX- when inappropiate off center fraction and point load)
if not 0 < off_center_fraction < 1:
    raise ValueError("off_center_fraction must be between 0 and 1")
if not spans or not point_loads or not uniform_loads:
    raise ValueError("span and load lists in config.json must not be empty")

functions = {
    "ss_center_point": ss_center_point,
    "ss_udl": ss_udl,
    "ss_off_center_point": ss_off_center_point,
    "canti_end_point": canti_end_point,
    "canti_udl": canti_udl
}

print("\nBEAM DEFLECTION RESULTS\n")

csv_rows = []

for case in beam_cases:

    print("\nBeam Case:", case)
    print("-" * 75)

    if case in ["ss_udl", "canti_udl"]:
        loads = uniform_loads
        load_type = "UDL"
    else:
        loads = point_loads
        load_type = "Point Load"

    
    for L in spans:

        
        for load in loads:

            
            beam = {
                "L": L,
                "E": E,
                "I": I
            }

           
            if load_type == "UDL":
                beam["w"] = load

            else:
                beam["P"] = load

            
            if case == "ss_off_center_point":
                beam["a"] = off_center_fraction * L

            
            calculate = functions[case]

            
            x_values = [i * L / 100 for i in range(101)]

            results = []

            for x in x_values:
                y = calculate(x, beam)
                results.append((x, y))
                csv_rows.append([
                    case,
                    L,
                    load_type,
                    load,
                    x,
                    y])

           
            max_result = max(results, key=lambda item: abs(item[1]))

            x_max, y_max = max_result

            # Display results
            print(
                f"Span = {L:.2f} m | "
                f"{load_type} = {load} | "
                f"Maximum Deflection = {abs(y_max):.8f} m | "
                f"At x = {x_max:.3f} m"
            )

print("CALCULATIONS COMPLETED")

with open("beam_deflection_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Beam Case",
        "Span (m)",
        "Load Type",
        "Load Value",
        "Position (m)",
        "Deflection (m)"
    ])

    writer.writerows(csv_rows)

print("\nCSV file generated successfully!")