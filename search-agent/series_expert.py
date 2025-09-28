from google.adk.agents import Agent

# Create the agent
series_expert = Agent(
    name="SeriesExpertAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are an expert at TV series. From name of files you are able to deduce the series name, "
        "season and episode number."
    ),

)
