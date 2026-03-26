from __future__ import annotations

import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Runnerbot 1 Demo", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f7f8f5 0%, #f1f4ed 100%);
    }

    [data-testid="stToolbar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.2rem !important;
        max-width: 1450px;
    }

    .hero-card {
        padding: 1.6rem 1.8rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #0f2a1d 0%, #183826 100%);
        color: white;
        box-shadow: 0 14px 40px rgba(0,0,0,0.10);
        margin-bottom: 1rem;
        margin-top: 0.2rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.92;
        margin-bottom: 0.8rem;
    }

    .mini-badge {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        margin-right: 0.45rem;
        margin-top: 0.35rem;
        font-size: 0.9rem;
    }

    .premium-card {
        background: white;
        padding: 1.2rem 1.2rem 1rem 1.2rem;
        border-radius: 20px;
        border: 1px solid rgba(15, 42, 29, 0.08);
        box-shadow: 0 10px 24px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }

    .section-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #4e6b5c;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .section-title {
        font-size: 1.95rem;
        font-weight: 800;
        color: #10281c;
        margin-bottom: 0.5rem;
    }

    .note-text {
        color: #42584b;
        font-size: 1rem;
        line-height: 1.55;
    }

    .metric-strip {
        background: linear-gradient(135deg, #ffffff 0%, #f6f8f2 100%);
        border: 1px solid rgba(15, 42, 29, 0.08);
        border-radius: 18px;
        padding: 1rem 1rem 0.75rem 1rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.03);
        min-height: 140px;
    }

    .investor-proof {
        border-left: 4px solid #1d6b3c;
        padding-left: 0.9rem;
        margin-top: 0.6rem;
    }

    .stButton > button {
        border-radius: 14px !important;
        border: 1px solid rgba(15, 42, 29, 0.10) !important;
        height: 3.2rem !important;
        font-weight: 700 !important;
    }

    .stTextInput input, .stTextArea textarea {
        border-radius: 14px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🌱 Runnerbot 1 — Venture 1</div>
        <div class="hero-subtitle">Nigeria-first agricultural intelligence for safer inputs, stronger yields, and export-grade compliance.</div>
        <div>
            <span class="mini-badge">WhatsApp / USSD / Voice-ready</span>
            <span class="mini-badge">Pesticide Safety Copilot</span>
            <span class="mini-badge">Export-Grade Compliance Layer</span>
            <span class="mini-badge">Investor Demo Build</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Demo Controls")
    language = st.selectbox("Language", ["English", "Yoruba", "Hausa"])
    crop = st.selectbox("Crop", ["Tomato", "Pepper", "Cassava", "Maize", "Plantain", "Beans", "Cocoa", "Okra"])
    location = st.selectbox("Location", ["Ogun", "Lagos"])

    st.markdown("---")
    st.markdown("**What this demo proves**")
    st.write("1. Farmer-grade advisory UX")
    st.write("2. Product safety intelligence")
    st.write("3. Pest triage with escalation logic")
    st.write("4. Export compliance positioning")
    st.write("5. Future data moat / policy dashboard")

    st.markdown("---")
    try:
        metrics = requests.get(f"{API_BASE}/metrics", timeout=5).json()
        st.metric("Q4 sign-up target", metrics["demo_signups_target_q4"])
        st.metric("Q4 Pro target", metrics["demo_pro_target_q4"])
        st.metric("Month 6 farmers", metrics["demo_month6_target_farmers"])
        st.metric("Month 6 Pro", metrics["demo_month6_target_pro"])
    except Exception:
        st.error("API not running yet.")

top1, top2, top3 = st.columns(3)

with top1:
    st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
    st.metric("Core wedge", "AI Safety Copilot")
    st.caption("Immediate trust + differentiation")
    st.markdown("</div>", unsafe_allow_html=True)

with top2:
    st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
    st.metric("Monetisation path", "Pro + Inputs")
    st.caption("Recurring revenue + commissions")
    st.markdown("</div>", unsafe_allow_html=True)

with top3:
    st.markdown('<div class="metric-strip">', unsafe_allow_html=True)
    st.metric("Strategic moat", "Compliance Data")
    st.caption("Regulatory + export intelligence")
    st.markdown("</div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Operator Console", "Investor View"])

with tab1:
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="section-label">Conversation layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Chat Demo</div>', unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": "Welcome to Runnerbot 1. Ask about pesticide safety, weather, prices, fertiliser, pest triage, or export compliance.",
                }
            ]

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_message = st.chat_input("Type a question for Runnerbot 1...")
        if user_message:
            st.session_state.chat_history.append({"role": "user", "content": user_message})

            try:
                response = requests.post(
                    f"{API_BASE}/chat",
                    json={
                        "message": user_message,
                        "language": language,
                        "crop": crop,
                        "location": location,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                reply = response.json()["reply"]
            except Exception as exc:
                reply = f"API error: {exc}"

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-label">Data moat preview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pesticide Intelligence Map Stub</div>', unsafe_allow_html=True)

        try:
            intel = requests.get(f"{API_BASE}/intelligence-summary", timeout=5).json()
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="note-text"><strong>Top flagged products:</strong> {', '.join(intel['top_flagged_products_demo'])}</div>
                    <div class="note-text"><strong>Priority states:</strong> {', '.join(intel['priority_states_demo'])}</div>
                    <div class="note-text"><strong>Priority crops:</strong> {', '.join(intel['priority_crops_demo'])}</div>
                    <div class="investor-proof"><strong>Insight:</strong> {intel['insight']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as exc:
            st.error(f"Could not load intelligence summary: {exc}")

    with col2:
        st.markdown('<div class="section-label">Safety intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Product Safety Check</div>', unsafe_allow_html=True)

        product_name = st.text_input("Enter pesticide / chemical product", placeholder="e.g. Paraquat")
        if st.button("Run Product Check", use_container_width=True):
            if not product_name.strip():
                st.warning("Enter a product name first.")
            else:
                try:
                    result = requests.post(
                        f"{API_BASE}/product-check",
                        json={"product_name": product_name},
                        timeout=10,
                    )
                    if result.status_code == 404:
                        st.error(result.json()["detail"])
                    else:
                        data = result.json()
                        st.markdown(
                            f"""
                            <div class="premium-card">
                                <div class="section-label">Runnerbot verdict</div>
                                <div class="section-title" style="font-size:1.35rem;">{data['runnerbot_verdict']}</div>
                                <div class="note-text"><strong>Product:</strong> {data['product_name']}</div>
                                <div class="note-text"><strong>Toxicity:</strong> {data['toxicity']}</div>
                                <div class="note-text"><strong>EU status:</strong> {data['eu_status']}</div>
                                <div class="note-text"><strong>Nigeria status:</strong> {data['nigeria_status']}</div>
                                <div class="note-text"><strong>Risk summary:</strong> {data['risk_summary']}</div>
                                <div class="note-text"><strong>Safer alternative:</strong> {data['safer_alternative']}</div>
                                <div class="note-text"><strong>PPE guidance:</strong> {data['ppe']}</div>
                                <div class="investor-proof"><strong>Export risk:</strong> {data['export_risk']}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                except Exception as exc:
                    st.error(f"API error: {exc}")

        st.markdown("---")
        st.markdown('<div class="section-label">Crop health support</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pest Triage</div>', unsafe_allow_html=True)

        symptoms = st.text_area("Describe symptoms", placeholder="e.g. holes in leaves, frass, yellowing")
        if st.button("Run Pest Triage", use_container_width=True):
            if not symptoms.strip():
                st.warning("Describe the symptoms first.")
            else:
                try:
                    result = requests.post(
                        f"{API_BASE}/pest-triage",
                        json={
                            "crop": crop,
                            "symptoms": symptoms,
                            "location": location,
                        },
                        timeout=10,
                    )
                    result.raise_for_status()
                    data = result.json()

                    badge = "Escalate to captain" if data["escalate_to_captain"] else "Guidance acceptable"
                    st.markdown(
                        f"""
                        <div class="premium-card">
                            <div class="section-label">Triage result</div>
                            <div class="section-title" style="font-size:1.35rem;">{data['diagnosis']}</div>
                            <div class="note-text"><strong>Confidence:</strong> {data['confidence']:.2f}</div>
                            <div class="note-text"><strong>Action:</strong> {data['action']}</div>
                            <div class="investor-proof"><strong>Routing logic:</strong> {badge}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                except Exception as exc:
                    st.error(f"API error: {exc}")

        st.markdown("---")
        st.markdown('<div class="section-label">Trade layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Export Compliance Check</div>', unsafe_allow_html=True)

        export_product = st.text_input(
            "Optional product for export check",
            placeholder="e.g. Dichlorvos or Paraquat",
            key="export_product",
        )

        if st.button("Run Export Check", use_container_width=True):
            try:
                result = requests.post(
                    f"{API_BASE}/export-check",
                    json={
                        "crop": crop,
                        "product_name": export_product if export_product.strip() else None,
                    },
                    timeout=10,
                )
                result.raise_for_status()
                data = result.json()

                st.markdown(
                    f"""
                    <div class="premium-card">
                        <div class="section-label">Export readiness view</div>
                        <div class="section-title" style="font-size:1.35rem;">{data['crop']} compliance profile</div>
                        <div class="note-text"><strong>Priority market:</strong> {data['priority_market']}</div>
                        <div class="note-text"><strong>Residue risk:</strong> {data['residue_risk']}</div>
                        <div class="note-text"><strong>Compliance advice:</strong> {data['compliance_advice']}</div>
                        <div class="investor-proof"><strong>Product overlay:</strong> {data['product_risk_overlay']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            except Exception as exc:
                st.error(f"API error: {exc}")

with tab2:
    left, right = st.columns([1.15, 1])

    with left:
        st.markdown('<div class="section-label">Investor narrative</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What this demo proves</div>', unsafe_allow_html=True)

        try:
            highlights = requests.get(f"{API_BASE}/demo-highlights", timeout=5).json()["highlights"]
        except Exception:
            highlights = []

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="note-text">
            Runnerbot 1 is not just an agronomy chatbot. It is a Nigeria-first agricultural intelligence system that combines advisory, pesticide safety, and export-compliance logic in one farmer-grade interface. That gives it stronger trust, stronger policy relevance, stronger monetisation logic, and a more defensible data moat than a standard advice product.
            </div>
            """,
            unsafe_allow_html=True,
        )
        for item in highlights:
            st.markdown(f"- {item}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="premium-card">
                <div class="section-label">Monetisation logic</div>
                <div class="note-text">
                Venture 1 monetises through Pro subscriptions, input-linked commerce, and future compliance and buyer tools. Every farmer interaction also creates structured safety, market, and compliance data that strengthens the product and increases enterprise value over time.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="section-label">Demo script</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Best investor flow</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="premium-card">
                <div class="note-text">
                    <strong>1.</strong> Start with chat: “hello” or “weather”<br><br>
                    <strong>2.</strong> Run Product Safety Check on <strong>Paraquat</strong><br><br>
                    <strong>3.</strong> Run Pest Triage with <strong>holes in leaves and frass</strong><br><br>
                    <strong>4.</strong> Run Export Check on <strong>Beans + Dichlorvos</strong><br><br>
                    <strong>5.</strong> Close on the intelligence map and data moat
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="premium-card">
                <div class="section-label">Positioning line</div>
                <div class="section-title" style="font-size:1.35rem;">
                    Nigerian AI protecting farmers, food systems, and export credibility.
                </div>
                <div class="note-text">
                    This is the bridge between agronomy, safety, compliance, and national-scale agricultural intelligence.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
