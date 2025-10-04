from google.adk.agents import Agent

# Create the agent
series_expert = Agent(
    name="SeriesExpertAgent",
    model="gemini-2.0-flash",
    instruction=(
        "You are an expert at TV series. From name of files you are able to deduce the series name, "
        "season and episode number and return it in a structured way." \
        "" \
        "Example: 'Doctor Who S01E14 1080p GLBO WEB-DL AAC2 0 H 264-SiGLA[EZTVx.to].mkv' -> "
        "{'series': 'Doctor Who', 'season': 1, 'episode': 14}" \
    ),

)
