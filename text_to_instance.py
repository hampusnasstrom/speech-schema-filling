from pydantic import BaseModel, Field
from typing import List


class Solution(BaseModel):
    temperature: float = Field(..., description="The temperature of the solution creation")
    atmosphere: str = Field(..., description="The atmosphere of the solution creation")
    method: str = Field(..., description="The method of the solution creation")
    time: float = Field(..., description="The time needed for the solution creation")
    solutes: List[str] = Field(..., description="The solutes used in the solution")
    solute_masses: List[float] = Field(..., description="The masses in miligramm of the solutes used in the solution")
    solvents: List[str] = Field(..., description="The solvents used in the solution")
    solvent_volumes: List[float] = Field(...,
                                         description="The volumes in mililiter of the solvents used in the solution")

functions = [
    {
        "name": "create_solution_entry",
        "description": "Create an entry for a chemical solution",
        "parameters": Solution.schema()
    }
]

messages = []
messages.append({"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."})
while(True):
    message = input("Next message: ")
    messages.append({"role": "user", "content": message})
    chat_response = chat_completion_request(
        messages, functions=functions
    )
    assistant_message = chat_response.json()["choices"][0]["message"]
    messages.append(assistant_message)
    print(assistant_message)

    stop = input("Press Enter to continue...")
    if stop:
        break
 # "Please create a solution of 2mg lead iodide as a solute and 100 ml ethanol as a solvent. The solution is produced at 25 degree celsius stirred for 15 minutes."
