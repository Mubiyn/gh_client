import requests
from pydantic import BaseModel
from typing import List, Dict, Optional

# Define the API base URL
API_URL = "http://127.0.0.1:8000/geometry/generate-mesh/"

# Define the MeshParams data structure
class MeshParams(BaseModel):
    name: str  # Name of the part
    type: str = "flexure_box"  # Default mesh type
    length: float = 1.0  # Length of the link
    width: float = 1.0   # Width of the link
    height: float = 1.0  # Height of the link
    radius: Optional[float] = 'low'  # Radius for spherical or cylindrical parts
    
    # Flexure-specific fields
    flexure_density: Optional[str] = 'low'  # Flexure density: "low", "medium", "high"
    flexure_regions: Optional[List[Dict[str, float]]] = []  # Regions for lattice flexures

# Function to generate a part by sending a POST request
def generate_part(ground_params: MeshParams, input_params: MeshParams, coupler_params: MeshParams, output_params: MeshParams,params_flexure:MeshParams):

# def generate_part(part_name, payload: MeshParams):
    print(f"Generating four-bar linkage...")

    # Prepare the payload as a dictionary
    linkage_params = {
    "ground": ground_params.model_dump(),
    "input": input_params.model_dump(),
    "coupler": coupler_params.model_dump(),
    "output": output_params.model_dump(),
    "flexure": params_flexure.model_dump()
}

    # Send the request to the server to create the four-bar linkage
    response = requests.post(API_URL, json=linkage_params)
    
    if response.status_code == 200:
        print(f"Four-bar linkage created successfully: {response.json()}")
    else:
        print(f"Error generating four-bar linkage: {response.json()}")

# Define payloads based on your schematic
# 1. Ground Link
params_ground = MeshParams(
    name="Ground Link",
    type="cylinder",  # Ground link is a rigid box with no flexures
    length=5.0,  
    width=0.5,  
    height=1.0, 
    radius= 0.5  ,  
    flexure_density='low',
    flexure_regions=[]
)

# 2. Input Link
params_input = MeshParams(
    name="Input Link",
    type="cylinder",  
    length=10.0, 
    width=0.5,
    height=10.0,
    radius= 0.5  ,
    flexure_density='low',
    flexure_regions=[]
)

# 3. Coupler Link (Connecting Link)
params_coupler = MeshParams(
    name="Coupler Link",
    type="cylinder",
    length=5.0,   # Slightly longer to connect input and output links
    width=0.5,
    height=5.0,
    radius= 0.5  ,
   flexure_density='low',
    flexure_regions=[]
)

# 4. Output Link
params_output = MeshParams(
    name="Output Link",
    type="cylinder",
    length=10.0,   # Same length as input link
    width=0.5,
    height=10.0,
    radius= 0.5  ,
   flexure_density='low',
    flexure_regions=[]
)

params_flexure = MeshParams(
    name="Flexure box",
    type="cylinder",  
    length=10.0, 
    width= 0.5, 
    radius=0.5,  
    height=10.0,  
    flexure_density="medium", 
    flexure_regions=[
        {
            "x_min": 0.0,
            "x_max": 0.5,
            "y_min": 0.0,
            "y_max": 0.5,  # Focus on cylindrical section
            "z_min": 0.0,
            "z_max": 0.5  # Flexure near coupler connection
        },
        {
            "x_min": 9.5,
            "x_max": 10.0,
            "y_min": 0.0,
            "y_max": 0.5,  # Flexure near the end of the link
            "z_min": 0.0,
            "z_max": 0.5
        }
    ]
)

# Generate all parts
generate_part( params_ground,
 params_input, params_coupler, params_output, params_flexure)
