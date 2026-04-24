from __future__ import annotations

import streamlit as st

from api import (
    DEMO_HIGHLIGHTS,
    IKIC_DEMO_HIGHLIGHTS,
    INTELLIGENCE_SUMMARY,
    detect_pest,
    get_export_check,
    get_product_info,
    runnerbot_response,
    trip_intelligence,
    load_priority,
    value_preserved,
    carrier_monitor,
    caas_model,
)

st.set_page_config(page_title="Runnerbot 1 Demo", page_icon="🌱", layout="wide")

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(180deg, #f7f8f5 0%, #f1f4ed 100%);}
    [data-testid="stToolbar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1.2rem !important; max-width: 1450px;}
    .hero-card {padding: 1.6rem 1.8rem; border-radius: 22px; background: linear-gradient(135deg, #0f2a1d 0%, #183826 100%); color: white; box-shadow: 0 14px 40px rgba(0,0,0,0.10); margin-bottom: 1rem; margin-top: 0.2rem;}
    .hero-title {font-size: 3rem; font-weight: 800; line-height: 1.05; margin-bottom: 0.4rem;}
    .hero-subtitle {font-size: 1.15rem; opacity: 0.92; margin-bottom: 0.8rem;}
    .mini-badge {display: inline-block; padding: 0.35rem 0.7rem; border-radius: 999px; background: rgba(255,255,255,0.12); margin-right: 0.45rem; margin-top: 0.35rem; font-size: 0.9rem;}
    .premium-card {background: white; padding: 1.2rem 1.2rem 1rem 1.2rem; border-radius: 20px; border: 1px solid rgba(15, 42, 29, 0.08); box-shadow: 0 10px 24px rgba(0,0,0,0.04); margin-bottom: 1rem;}
    .section-label {font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.08em; color: #4e6b5c; font-weight: 700; margin-bottom: 0.2rem;}
    .section-title {font-size: 1.95rem; font-weight: 800; color: #10281c; margin-bottom: 0.5rem;}
    .note-text {color: #42584b; font-size: 1rem; line-height: 1.55;}
    .metric-strip {background: linear-gradient(135deg, #ffffff 0%, #f6f8f2 100%); border: 1px solid rgba(15, 42, 29, 0.08); border-radius: 18px; padding: 1rem 1rem 0.75rem 1rem; box-shadow: 0 8px 20px rgba(0,0,0,0.03); min-height: 140px;}
    .investor-proof {border-left: 4px solid #1d6b3c; padding-left: 0.9rem; margin-top: 0.6rem;}
    .stButton > button {border-radius: 14px !important; border: 1px solid rgba(15, 42, 29, 0.10) !important; height: 3.2rem !important; font-weight: 700 !important;}
    .stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {border-radius: 14px !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">🌱 Runnerbot 1 — Venture 1</div>
        <div class="hero-subtitle">Nigeria-first agricultural intelligence for safer inputs, stronger yields, export-grade compliance, and cold-chain decisions.</div>
        <div>
            <span class="mini-badge">WhatsApp / USSD / Voice-ready</span>
            <span class="mini-badge">Pesticide Safety Copilot</span>
            <span class="mini-badge">Export-Grade Compliance Layer</span>
            <span class="mini-badge">IKIC Cold Chain Ops</span>
            <span class="mini-badge">Investor Demo Build</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Demo Controls")
    language = st.selectbox("Language", ["English", "Yoruba", "Hausa"])
    crop = st.selectbox("Crop", ["Tomato", "Pepper", "Cassava", "Maize", "Plantain", "Beans", "Cocoa", "Okra", "Eggplant", "Mushrooms", "Herbs", "Leafy Vegetables"])
    location = st.selectbox("Location", ["Ogun", "Lagos"])

    st.markdown("---")
    st.markdown("**What this demo proves**")
    st.write("1. Farmer-grade advisory UX")
    st.write("2. Product safety intelligence")
    st.write("3. Pest triage with escalation logic")
    st.write("4. Export compliance positioning")
    st.write("5. Future data moat / policy dashboard")
    st.write("6. IKIC cold-chain decision intelligence")

    st.markdown("---")
    st.metric("Q4 sign-up target", 1000)
    st.metric("Q4 Pro target", 300)
    st.metric("Month 6 farmers", 5000)
    st.metric("Month 6 Pro", 1200)

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
    st.metric("Strategic moat", "Compliance + Cold Data")
    st.caption("Regulatory + export + operations intelligence")
    st.markdown("</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Operator Console", "Investor View", "IKIC / Cold Chain Ops"])

with tab1:
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown('<div class="section-label">Conversation layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Chat Demo</div>', unsafe_allow_html=True)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Welcome to Runnerbot 1. Ask about pesticide safety, weather, prices, fertiliser, pest triage, export compliance, or IKIC cold-chain ops."}
            ]

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_message = st.chat_input("Type a question for Runnerbot 1...")
        if user_message:
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            reply = runnerbot_response(user_message, crop, location)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        st.markdown("---")
        st.markdown('<div class="section-label">Data moat preview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pesticide Intelligence Map Stub</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="note-text"><strong>Top flagged products:</strong> {', '.join(INTELLIGENCE_SUMMARY['top_flagged_products_demo'])}</div>
                <div class="note-text"><strong>Priority states:</strong> {', '.join(INTELLIGENCE_SUMMARY['priority_states_demo'])}</div>
                <div class="note-text"><strong>Priority crops:</strong> {', '.join(INTELLIGENCE_SUMMARY['priority_crops_demo'])}</div>
                <div class="investor-proof"><strong>Insight:</strong> {INTELLIGENCE_SUMMARY['insight']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<div class="section-label">Safety intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Product Safety Check</div>', unsafe_allow_html=True)

        product_name = st.text_input("Enter pesticide / chemical product", placeholder="e.g. Paraquat")
        if st.button("Run Product Check", use_container_width=True):
            if not product_name.strip():
                st.warning("Enter a product name first.")
            else:
                try:
                    data = get_product_info(product_name)
                    st.markdown(
                        f"""
                        <div class="premium-card">
                            <div class="section-label">Runnerbot verdict</div>
                            <div class="section-title" style="font-size:1.35rem;">{data['runnerbot_verdict']}</div>
                            <div class="note-text"><strong>Product:</strong> {product_name}</div>
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
                    st.error(str(exc))

        st.markdown("---")
        st.markdown('<div class="section-label">Crop health support</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Pest Triage</div>', unsafe_allow_html=True)

        symptoms = st.text_area("Describe symptoms", placeholder="e.g. holes in leaves, frass, yellowing")
        if st.button("Run Pest Triage", use_container_width=True):
            if not symptoms.strip():
                st.warning("Describe the symptoms first.")
            else:
                data = detect_pest(symptoms)
                badge = "Escalate to captain" if data["confidence"] < 0.60 else "Guidance acceptable"
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

        st.markdown("---")
        st.markdown('<div class="section-label">Trade layer</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Export Compliance Check</div>', unsafe_allow_html=True)

        export_product = st.text_input("Optional product for export check", placeholder="e.g. Dichlorvos or Paraquat", key="export_product")
        if st.button("Run Export Check", use_container_width=True):
            data = get_export_check(crop, export_product if export_product.strip() else None)
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="section-label">Export readiness view</div>
                    <div class="section-title" style="font-size:1.35rem;">{crop} compliance profile</div>
                    <div class="note-text"><strong>Priority market:</strong> {data['priority_market']}</div>
                    <div class="note-text"><strong>Residue risk:</strong> {data['residue_risk']}</div>
                    <div class="note-text"><strong>Compliance advice:</strong> {data['compliance_advice']}</div>
                    <div class="investor-proof"><strong>Product overlay:</strong> {data['product_risk_overlay']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab2:
    left, right = st.columns([1.15, 1])

    with left:
        st.markdown('<div class="section-label">Investor narrative</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">What this demo proves</div>', unsafe_allow_html=True)
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="note-text">
            Runnerbot 1 is not just an agronomy chatbot. It is a Nigeria-first agricultural intelligence system that combines advisory, pesticide safety, export-compliance logic, and now cold-chain decision support in one farmer-grade interface. That gives it stronger trust, stronger policy relevance, stronger monetisation logic, and a more defensible data moat than a standard advice product.
            </div>
            """,
            unsafe_allow_html=True,
        )
        for item in DEMO_HIGHLIGHTS + IKIC_DEMO_HIGHLIGHTS:
            st.markdown(f"- {item}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="premium-card">
                <div class="section-label">Monetisation logic</div>
                <div class="note-text">
                Venture 1 monetises through Pro subscriptions, input-linked commerce, future compliance and buyer tools, and now cold-chain operating intelligence for carriers, cooperatives, aggregators, and Cooling-as-a-Service models. Every interaction creates structured safety, market, compliance, and operations data that increases enterprise value over time.
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
                    <strong>5.</strong> Open <strong>IKIC / Cold Chain Ops</strong> and run Trip Intelligence + ROI<br><br>
                    <strong>6.</strong> Close on the intelligence map and data moat
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
                    Nigerian AI protecting farmers, food systems, export credibility, and cold-chain margins.
                </div>
                <div class="note-text">
                    This is the bridge between agronomy, safety, compliance, and first-mile operating intelligence.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab3:
    st.markdown('<div class="section-label">IKIC partner layer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">IKIC / Cold Chain Ops</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="premium-card">
            <div class="note-text">
            This section turns Runnerbot 1 into the software intelligence layer on top of passive cold-chain hardware. It helps decide what to cool first, whether a trip is still commercially worth running, how much value is being protected, and what next action protects margin best.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown('<div class="section-label">Trip planner</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">FreshCarrier Trip Intelligence</div>', unsafe_allow_html=True)
        trip_crop = st.selectbox("Trip crop", ["Tomato", "Pepper", "Okra", "Eggplant", "Leafy Vegetables", "Mushrooms", "Herbs", "Beans", "Cassava"], key="trip_crop")
        trip_hours = st.number_input("Trip duration (hours)", min_value=1.0, max_value=72.0, value=12.0, step=1.0)
        ambient = st.number_input("Ambient temperature (°C)", min_value=20.0, max_value=50.0, value=34.0, step=1.0)
        destination = st.selectbox("Destination", ["Cold room", "Urban market", "Processor", "Export aggregator"], key="destination")
        freshcarrier = st.checkbox("FreshCarrier available", value=True)
        charged = st.checkbox("Thermostatic batteries fully charged", value=True)

        if st.button("Run Trip Intelligence", use_container_width=True):
            data = trip_intelligence(trip_crop, trip_hours, ambient, freshcarrier, charged, destination)
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="section-label">Decision output</div>
                    <div class="section-title" style="font-size:1.35rem;">Cold-chain fit: {data['cold_chain_fit']}</div>
                    <div class="note-text"><strong>Cold-chain window:</strong> {data['cold_chain_window_hours']} hours</div>
                    <div class="note-text"><strong>Spoilage risk:</strong> {data['spoilage_risk']} ({data['risk_score']}/100)</div>
                    <div class="note-text"><strong>Quality at arrival:</strong> {data['quality_score']}/100</div>
                    <div class="note-text"><strong>Premium market eligible:</strong> {data['premium_market_eligible']}</div>
                    <div class="note-text"><strong>Best next action:</strong> {data['best_next_action']}</div>
                    <div class="investor-proof"><strong>Commercial note:</strong> {data['commercial_note']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with sub2:
        st.markdown('<div class="section-label">Load logic</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Produce Load Prioritiser</div>', unsafe_allow_html=True)
        crops_input = st.text_input("Comma-separated crops", value="Tomato, Pepper, Eggplant, Leafy Vegetables")
        if st.button("Rank Loading Order", use_container_width=True):
            crops = [c.strip() for c in crops_input.split(",") if c.strip()]
            ranked = load_priority(crops)
            text = "".join([f"<div class='note-text'><strong>{i+1}.</strong> {r['crop']} — priority {r['priority_score']}/10 — {r['reason']}</div>" for i, r in enumerate(ranked)])
            st.markdown(f"<div class='premium-card'><div class='section-label'>Recommended loading order</div>{text}</div>", unsafe_allow_html=True)

    sub3, sub4 = st.columns(2)
    with sub3:
        st.markdown('<div class="section-label">Commercial logic</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Value Preserved Calculator</div>', unsafe_allow_html=True)
        vp_crop = st.selectbox("Crop for ROI", ["Tomato", "Pepper", "Okra", "Eggplant", "Leafy Vegetables", "Mushrooms", "Herbs", "Beans", "Cassava"], key="vp_crop")
        volume = st.number_input("Volume (kg)", min_value=10.0, max_value=5000.0, value=200.0, step=10.0)
        price = st.number_input("Base realised price per kg (₦)", min_value=50.0, max_value=10000.0, value=600.0, step=50.0)
        trips_week = st.number_input("Trips per week", min_value=1, max_value=20, value=4, step=1)
        if st.button("Calculate Value Preserved", use_container_width=True):
            vp = value_preserved(vp_crop, volume, price, trips_week)
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="section-label">Economic readout</div>
                    <div class="section-title" style="font-size:1.35rem;">₦{vp['value_preserved_per_trip_ngn']:,.0f} preserved per trip</div>
                    <div class="note-text"><strong>Loss without cold:</strong> {vp['loss_without_cold_pct']}%</div>
                    <div class="note-text"><strong>Premium uplift potential:</strong> {vp['premium_uplift_pct']}%</div>
                    <div class="note-text"><strong>Monthly value preserved:</strong> ₦{vp['monthly_value_preserved_ngn']:,.0f}</div>
                    <div class="investor-proof"><strong>Decision summary:</strong> {vp['decision_summary']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with sub4:
        st.markdown('<div class="section-label">IoT mockup</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Carrier Monitor</div>', unsafe_allow_html=True)
        elapsed = st.number_input("Trip hours elapsed", min_value=0.0, max_value=72.0, value=7.0, step=1.0)
        charged2 = st.checkbox("Batteries charged", value=True, key="charged2")
        locked = st.checkbox("Smart lock enabled", value=True)
        crates_loaded = st.number_input("Crates loaded", min_value=0, max_value=2, value=2, step=1)
        if st.button("Run Carrier Monitor", use_container_width=True):
            cm = carrier_monitor(elapsed, charged2, locked, crates_loaded)
            st.markdown(
                f"""
                <div class="premium-card">
                    <div class="section-label">Live carrier status</div>
                    <div class="section-title" style="font-size:1.35rem;">{cm['system_status']}</div>
                    <div class="note-text"><strong>Temperature:</strong> {cm['temperature_status']}</div>
                    <div class="note-text"><strong>Remaining cold life:</strong> {cm['remaining_cold_life_hours']} hours</div>
                    <div class="note-text"><strong>Battery status:</strong> {cm['battery_status']}</div>
                    <div class="note-text"><strong>Geo-status:</strong> {cm['geo_status']}</div>
                    <div class="note-text"><strong>Lock:</strong> {cm['lock_status']}</div>
                    <div class="note-text"><strong>Inventory count:</strong> {cm['inventory_count']}</div>
                    <div class="investor-proof"><strong>Alert:</strong> {cm['alert']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown('<div class="section-label">Business model layer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Cooling-as-a-Service Economics</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        units = st.number_input("Units in micro-fleet", min_value=1, max_value=50, value=4, step=1)
    with c2:
        weekly_trips = st.number_input("Trips per week per route cluster", min_value=1, max_value=50, value=8, step=1)
    with c3:
        avg_preserved = st.number_input("Average value preserved per trip (₦)", min_value=1000.0, max_value=5000000.0, value=85000.0, step=5000.0)

    if st.button("Run Cooling-as-a-Service Model", use_container_width=True):
        caas = caas_model(units, weekly_trips, avg_preserved)
        st.markdown(
            f"""
            <div class="premium-card">
                <div class="section-label">Operating model</div>
                <div class="section-title" style="font-size:1.35rem;">{caas['recommended_operating_model']}</div>
                <div class="note-text"><strong>Estimated monthly trips:</strong> {caas['estimated_monthly_trips']}</div>
                <div class="note-text"><strong>Estimated utilisation:</strong> {caas['estimated_utilisation_pct']}%</div>
                <div class="note-text"><strong>Estimated monthly value preserved:</strong> ₦{caas['estimated_monthly_value_preserved_ngn']:,.0f}</div>
                <div class="investor-proof"><strong>Commercial readout:</strong> {caas['commercial_readout']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
