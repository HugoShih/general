import streamlit as st
import awesome_streamlit as ast
import src.pages.about as about
import src.pages.pdf_converter as pdf
import src.pages.price_decoder as decoder

ast.core.services.other.set_logging_format()

PAGES = {
    "About": about,
    "PDF to Excel": pdf,
    "Price Decoder": decoder,
}

def main():
    """Main function of the App"""
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)

if __name__ == "__main__":
    main()