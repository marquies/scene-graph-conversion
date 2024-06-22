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

for element in tuples:
    if element.x not in g.nodes:
        g.add_node(element.x)
    if element.z not in g.nodes:
        g.add_node(element.z)
    g.add_edge(element.x, element.z).add_label(element.y)

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

prompt = "" # pylint: disable=invalid-name
for element in tuples:
    objA = element.x.split('/')[-1]
    objB = element.z.split('/')[-1]
    print("\n" + objA + " is " + element.y + " " + objB + ".")
    prompt += "\n" + objA + " is " + element.y + " " + objB + "."
    #print(f"\n object {objA.name} is {left_right} of object
    # {objB.name} and {above_below} object {objB.name}
    #  and {front_back} object {objB.name}.")

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

FILENAME = 'image.jpg'
image_url = response.data[0].url
print(image_url)

res = requests.get(image_url, stream = True, timeout=120)
if res.status_code == 200:
    with open(FILENAME,'wb') as f:
        shutil.copyfileobj(res.raw, f)
    print('Image sucessfully Downloaded: ',FILENAME)
else:
    print('Image Couldn\'t be retrieved')
