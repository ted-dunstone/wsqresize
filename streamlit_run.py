from fileinput import filename
import streamlit as st
import io
import numpy
import wsq

from PIL import Image

st.header("Image Manipulation for WSQ")
st.info("Note: This is a work in progress. It is not yet ready for production use.")
st.warning("No data is saved or recorded to disk")
img_file_buffer=st.file_uploader("Upload a file", type=["png","wsq","jpg"])
if img_file_buffer is None:
    st.stop()

finger = Image.open(img_file_buffer)
offset_val= st.sidebar.slider("Image Width Adjust", -64, 64, 0, 1)

fp1=finger.convert('L')
st.sidebar.image(fp1)
pix = numpy.array(fp1)
val = pix.shape[1]-offset_val
raw=pix.flatten()


rows=int(len(raw)/val)
size=[rows,val]
raw=raw[:val*(rows)]
pix2=raw.reshape(size)
im = Image.fromarray(numpy.uint8(pix2))

st.image(im)
#st.write("blah")
#st.image(im2)
with io.BytesIO() as output:
    im_format = st.selectbox("Select a image format", ["png","jpg","wsq"])
    im.save(output, format=im_format)
    contents = output.getvalue()
    st.download_button(label="download image",data=contents, file_name="fixed_image."+im_format)

with st.expander("Raw Binary Data"):
    res=numpy.array(im.copy().crop((0,0,1,rows))) #.histogram()
    st.write("Standard Deviation")
    st.write(numpy.std(res))
    st.line_chart(res)
    c1,c2=st.columns(2)
    c1.write("Start of File")
    c1.write([numpy.base_repr(v, base=16) for v in raw[:abs(offset_val)]])
    c2.write("End of File")
    c2.write([numpy.base_repr(v, base=16) for v in raw[-abs(offset_val):]])
  
st.write(st.experimental_get_query_params())
