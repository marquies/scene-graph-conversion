"""
Demo
"""

import shutil # save img locally
import pyyed

from openai import OpenAI

import requests # request img from web
import converter.conversion as converter

#inputs, camera = filter_log_file("input_data/scenegraphlog11.log", "Camera")
inputs, camera = converter.filter_log_file("input_data/scenegraphlog20.log", "Main Camera")

print("Found " + str(len(inputs)) + " objects in the log file.  ")

objects = converter.get_objects_from_input(inputs)

print("Filtered " + str(len(objects)) + " objects from the log file.   ")

tuples = converter.determine_arrangement2(camera, objects)

tuples = converter.remove_bidirectional_duplicates(tuples)

g = pyyed.Graph()

for i in range(len(tuples)):
    if tuples[i].x not in g.nodes:
        g.add_node(tuples[i].x)
    if tuples[i].z not in g.nodes:
        g.add_node(tuples[i].z)
    g.add_edge(tuples[i].x, tuples[i].z).add_label(tuples[i].y)

print("Added " + str(len(g.nodes)) + " nodes and " + str(len(g.edges)) + " edges to the graph.   ")
#g.add_node('foo', font_family="Zapfino")
#g.add_node('foo2', shape="roundrectangle", font_style="bolditalic", underlined_text="true")

#g.add_edge('foo1', 'foo2')
#g.add_node('abc', font_size="72", height="100")

#g.add_node('bar', label="Multi\nline\ntext")
#g.add_node('foobar', label="""Multi
#Line
#Text!""")
    
#print(g.get_graph())

# print a string for each set of tuples

prompt = ""
for i in range(len(tuples)):
    objA = tuples[i].x.split('/')[-1]
    objB = tuples[i].z.split('/')[-1]
    print("\n" + objA + " is " + tuples[i].y + " " + objB + ".")
    prompt += "\n" + objA + " is " + tuples[i].y + " " + objB + "."
    #print(f"\n object {objA.name} is {left_right} of object {objB.name} and {above_below} object {objB.name} and {front_back} object {objB.name}.")

#just keep first 1000 characters from prompt   
prompt = prompt[:4000]

# To write to file:
with open('test_graph.graphml', 'w', encoding='utf-8') as fp:
    fp.write(g.get_graph())
client = OpenAI()

response = client.images.generate(
  model="dall-e-3",
  prompt=prompt, #"a white siamese cat",
  size="1024x1024",
  quality="standard",
  #seed=1234567890,
  #temperature=0.7,
  n=1,
)

file_name = 'image.jpg'
image_url = response.data[0].url
print(image_url)

res = requests.get(image_url, stream = True, timeout=120)
if res.status_code == 200:
    with open(file_name,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ',file_name)
else:
    print('Image Couldn\'t be retrieved')