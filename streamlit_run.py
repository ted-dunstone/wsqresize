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
val= st.sidebar.slider("Image Offset", 0, 64, 1)

fp1=finger.convert('L')
st.sidebar.image(fp1)
pix = numpy.array(fp1)
val = pix.shape[1]-val
raw=pix.flatten()
#for i in range(30,40):
#  const=i*100;
#
rows=int(len(raw)/val)
size=[rows,val]
raw=raw[:val*(rows)]
pix2=raw.reshape(size)

im = Image.fromarray(numpy.uint8(pix2))
st.image(im)
with io.BytesIO() as output:
    im_format = st.selectbox("Select a image format", ["png","jpg","wsq"])
    im.save(output, format=im_format)
    contents = output.getvalue()
    st.download_button(label="download image",data=contents, file_name="fixed_image."+im_format)