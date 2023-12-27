import streamlit as st
import stanza
from PIL import Image
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt

@st.cache_resource
def loading_model():
    return stanza.Pipeline('vi', depparse_model_path="./vi_vtb_charlm_parser.pt")

def parse_text(pipeline, user_input):
    doc = pipeline(user_input)
    dependencies = doc.sentences[0].dependencies_string()
    return doc, dependencies

def visualize_tree(doc):
    edges = []
    for sentence in doc.sentences:
        for edge in sentence.dependencies:
            edges.append((edge[2].text, edge[0].text))

    G = nx.DiGraph(edges)
    G = G.reverse()

    plt.figure(figsize=(10, 8))

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=1500, font_size=8, arrowsize=10)


    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)

    img = Image.open(img_stream)

    st.image(img)


def main():
    st.title("Dependecy Parsing")

    # Download the model and create the pipeline
    pipeline = loading_model()

    user_input = st.text_area("Enter some text:")

    _, col1, _, col2,_ = st.columns(5)

    parse_btn = col1.button("Parse Text")
    visualize_btn = col2.button("Visualize Tree")

    if parse_btn:
        if user_input:
            result, dependencies = parse_text(pipeline, user_input)
            st.text("Dependency Relations:")
            st.text(dependencies)     
        else:
            st.warning("Please enter some text.")

    if visualize_btn:
        if user_input:
            result, dependencies = parse_text(pipeline, user_input)
            st.text("Dependency Tree:")
            visualize_tree(result) 
        else:
            st.warning("Please enter some text.")

if __name__ == "__main__":
    main()

