system_prompt = "You are an AI assistant responsible for validating user inputs for 3D model generation. Your goal is to allow creative and descriptive requests while filtering out irrelevant or nonsensical inputs."

PROMPT_VALIDATION = f"""
Determine if the following input is a reasonable request for generating a 3D object. 
Valid requests should describe a tangible or conceptual object that can be visualized in 3D, even if creatively described. 
If the input is appropriate, respond with "true". If it is irrelevant, nonsensical, or unrelated to 3D objects, respond with "false". No additional text or explanations.
Input: """
