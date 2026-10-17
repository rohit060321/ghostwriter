import os
import requests
import streamlit as st

API_URL = os.getenv("GHOSTWRITER_API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="GhostWriter AI", page_icon="✍️", layout="wide")

st.title("GhostWriter AI")
st.subheader("Turn one product idea into a ready-to-publish sales kit.")
st.caption("Powered by an open-weight model. With local Ollama, your product details stay on your computer.")

with st.sidebar:
    st.header("Your sales style")
    platform = st.selectbox("Where will you sell?", ["Instagram", "WhatsApp Business", "Etsy", "Facebook Marketplace", "General"])
    tone = st.selectbox("Writing tone", ["Friendly", "Premium", "Funny", "Minimal", "Persuasive"])
    language = st.selectbox("Output language", ["English", "Hindi", "Marathi", "Hinglish"])
    st.markdown("---")
    st.caption("Supports local Ollama or hosted inference on Render.")

left, right = st.columns([1, 1])
with left:
    product_name = st.text_input("Product name", placeholder="Handmade lavender candle")
    product_type = st.text_input("Product category", placeholder="Home decor")
    features = st.text_area("Features and details", placeholder="Soy wax, lavender scent, reusable glass jar...", height=130)
    audience = st.text_input("Target customer", placeholder="People who enjoy relaxing home spaces")
with right:
    price = st.text_input("Price (optional)", placeholder="₹499")
    offer = st.text_input("Offer or special detail (optional)", placeholder="Gift wrapping available")
    call_to_action = st.text_input("Preferred call to action", value="Message us to order")
    st.info("Tip: Add real features and prices. The AI may phrase your details creatively, so review the result before publishing.")

if st.button("Make This Sell", type="primary", use_container_width=True):
    if not product_name.strip() or not features.strip():
        st.error("Please enter at least a product name and its features.")
    else:
        payload = {
            "product_name": product_name.strip(),
            "category": product_type.strip(),
            "features": features.strip(),
            "audience": audience.strip(),
            "price": price.strip(),
            "offer": offer.strip(),
            "platform": platform,
            "tone": tone,
            "language": language,
            "call_to_action": call_to_action.strip(),
        }
        with st.spinner("Creating your sales kit..."):
            try:
                response = requests.post(f"{API_URL}/generate", json=payload, timeout=180)
                response.raise_for_status()
                result = response.json()
                st.session_state["sales_kit"] = result["sales_kit"]
                st.session_state["provider"] = result.get("provider", "AI")
                st.session_state["model"] = result.get("model", "")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not reach the backend at {API_URL}. Start the FastAPI server and try again.")
            except requests.exceptions.Timeout:
                st.error("The model took too long to respond. Try again or check your backend connection.")
            except requests.exceptions.HTTPError as exc:
                detail = "The backend returned an error."
                try:
                    detail = response.json().get("detail", detail)
                except Exception:
                    pass
                st.error(f"{detail} ({exc})")
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")

if "sales_kit" in st.session_state:
    st.markdown("---")
    st.header("Your sales kit")
    provider = st.session_state.get("provider")
    model = st.session_state.get("model")
    if provider and model:
        st.caption(f"Generated with **{model}** via **{provider}**")
    sales_kit = st.session_state["sales_kit"]
    st.markdown(sales_kit)
    st.download_button(
        "Download sales kit (.md)",
        data=sales_kit,
        file_name="ghostwriter-sales-kit.md",
        mime="text/markdown",
        use_container_width=True,
    )
