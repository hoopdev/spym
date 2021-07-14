import spym
import os

# List up all measurement files
data_dir = 'D:/spmdata/2021/0713/'
data_files = os.listdir(data_dir)

# Make figure for each measurement.
fig_list_Topo = []
fig_list_STS = []
for item_name in data_files:
    if item_name.endswith('.sm4'):
        # Handle STS files
        if 'STS' in item_name:
            f_sts = spym.load(os.path.join(data_dir+item_name))
            lia_current = f_sts.LIA_Current
            fig = lia_current.spym.plotly(display = False)
            fig_list_STS.append(fig)
        
        # Handle Image and other files
        else:
            f_topo = spym.load(os.path.join(data_dir+item_name))
            tf = f_topo.Topography_Forward
            tf.spym.align()
            tf.spym.plane()
            tf.spym.fixzero()
            fig = tf.spym.plotly(display = False)
            fig_list_Topo.append(fig)

# Prepare for html writer
filename= os.path.join(data_dir+"catalogue.html")
dashboard = open(filename, 'w')
dashboard.write("<html><head></head><body>" + "\n") # Write the part before body
include_plotlyjs = True

for fig in fig_list_Topo+fig_list_STS:
    inner_html = fig.to_html(include_plotlyjs = include_plotlyjs).split('<body>')[1].split('</body>')[0] # Export each fig into html and strip the body
    dashboard.write(inner_html)
    include_plotlyjs = False
dashboard.write("</body></html>" + "\n") # Write the part after body