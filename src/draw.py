import math

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Oval
from bokeh.palettes import Spectral8

from graph import * 

WIDTH = 500
HEIGHT = 500 #TODO currently graph renders sq Possible fix by Ajmal in stackoverflow
CIRCLE_SIZE = 30

graph_data = Graph()
graph_data.debug_create_test_data()
#print(graph_data.vertexes)
graph_data.bfs(graph_data.vertexes[0])

N = len(graph_data.vertexes) # N=8 makes 8 offshoots from one point. Theese are vertexes or nodes
node_indices = list(range(N))

color_list = [] #random colors
for vertex in graph_data.vertexes:
    color_list.append(vertex.color)

plot = figure(title='Graph Layout Demonstration', x_range=(0, WIDTH), y_range=(0, HEIGHT),
              tools='', toolbar_location=None)

graph = GraphRenderer()

graph.node_renderer.data_source.add(node_indices, 'index')
graph.node_renderer.data_source.add(color_list, 'color')
graph.node_renderer.glyph = circle(size=CIRCLE_SIZE, fill_color='color') # makes ovals


#TODO this is drawing the edges from start to end
start_indexes = []
end_indexes = []

for start_index, vertex in enumerate(graph_data.vertexes):
    for e in vertex.edges:
        start_indexes.append(start_index)
        end_indexes.append(graph_data.vertexes.index(e.destination))

graph.edge_renderer.data_source.data = dict(
    start=start_indexes, # this is a list of some kind that has to do with starting points
    end=end_indexes) # this is a list of some kind that has to do with ending points

print(graph.edge_renderer.data_source.data)   
### start of layout code
# looks like it sets positions of vertexes

x = [v.pos['x'] for v in graph_data.vertexes]
y = [v.pos['y'] for v in graph_data.vertexes]

graph_layout = dict(zip(node_indices, zip(x, y)))
graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

plot.renderers.append(graph)


#Create a new dict to use a data source with 3 lists in it ordered the same wayas vertexes
# List of x values
# List of y values
# List of labels
value =[v.value for v in graph_data.vertexes] #TODO possible optimization we run through loop 3 times

label_source = ColumnDataSource(data=dict(x=x, y=y, v=value))


labels = LabelSet(x='x', y='y', text='v', level='glyph',
            source=label_source, render_mode='canvas', text_align='center', text_baseline='middle')

#TODA Investigate plot.add_layout vs. plot.reducers.append

plot.add_layout(labels)

output_file('graph.html')
show(plot)


