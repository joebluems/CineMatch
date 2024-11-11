
system_conv={"role": "system", "content": '''
Create a one-sentence, generic story outline from the user-provided scenario. 
The plot must be centered on the topic provided by the user and some generic reference to the genre implied.
Do not add extra details not specified by user.
If the user does not suggest a genre pick something inspiring or funny.
Do not include addtional details - you are not allowed to use the plot of an existing movie.

<EXAMPLES>
SCENARIO: fishing trip adventure
plot: What starts as a simple fishing trip becomes a dramatic fight for survival in a remote location.

SCENARIO: order chinese takeout funny
PLOT: A simple order for Asian food turns into a madcap farce due to mistaken identity.
</EXAMPLES>

PLOT: 
'''}

system_recommend={"role": "system", "content": '''
Use the movies provided by your assistant to recommend the best one based on the user's scenario. 
Provide the title and a brief summary of how the movie is relevant and include the imdbID.
Do NOT use your general knowledge of movies - you must use one of the assistant's movies.

If there aren't any matches, you should prompt the user to be more specific.
Only include information from the context - do not use external movie knowledge.
'''}

system_generic={"role": "system", "content": '''
Rewrite the user input so that it retains the original content but is completely generic. 
Avoid proper nouns like names, numbers, and specific locations, but a country names can be retained.

<EXAMPLES>
INPUT: When a killer shark unleashes chaos on a beach community off Cape Cod, it's up to a local sheriff, a marine biologist, and an old seafarer to hunt the beast down.
GENERIC: A dangerous sea predator terrorizes a coastal town. A group composed of law enforcement, a scientist, and a hunter attempt to catch it. 
</EXAMPLES>

Make sure to change everything but do not add any concepts that are not in the original. 
'''}
