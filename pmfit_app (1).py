import streamlit as st
import anthropic
import re

st.set_page_config(
    page_title="PMFit AI",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #08090c;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 680px; }

h1 {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: #f1f5f9 !important;
    line-height: 1.15 !important;
}
h2 {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    color: #38bdf8 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.5rem !important;
}
textarea, input[type="text"] {
    background-color: #0f1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div {
    background-color: #0f1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stButton > button {
    width: 100%;
    background-color: #38bdf8 !important;
    color: #08090c !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.85rem !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.section-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.pros-card {
    background: rgba(34,197,94,0.04);
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.path-card {
    background: rgba(167,139,250,0.04);
    border: 1px solid rgba(167,139,250,0.18);
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.leverage-card {
    background: rgba(56,189,248,0.05);
    border: 1px solid rgba(56,189,248,0.25);
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.confidence-high {
    background: rgba(34,197,94,0.05);
    border: 1px solid rgba(34,197,94,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.confidence-medium {
    background: rgba(251,191,36,0.05);
    border: 1px solid rgba(251,191,36,0.2);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.confidence-assumption {
    background: rgba(148,163,184,0.05);
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.clabel {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.5rem;
}
.slabel {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.btext { font-size: 13px; color: #94a3b8; line-height: 1.8; white-space: pre-wrap; }
.vtext { font-size: 15px; color: #e2e8f0; line-height: 1.75; }
.big-score { font-size: 4rem; font-weight: 700; line-height: 1; font-family: 'DM Mono', monospace; }
hr { border-color: #1e2533 !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

LOCATIONS = {
    "🇮🇳 Hyderabad": {
        "name": "Hyderabad",
        "context": "Market: Hyderabad, India (Tier-1 city). Currency: ₹. Key realities: intense JEE/NEET/CA exam pressure culture, strong coaching institute ecosystem (BYJU's, Allen, Unacademy already dominant), parental decision-making power over education spending, extreme price sensitivity (₹99/month feels different from ₹999/month), pharma/IT/finance job market hyper-competitive, WhatsApp is primary communication channel not email, family-first culture means B2C products need parent buy-in not just user buy-in."
    },
    "🇮🇳 Mumbai": {
        "name": "Mumbai",
        "context": "Market: Mumbai, India (financial capital). Currency: ₹. Key realities: finance career aspirations intense (CA, CFA, investment banking), high cost of living limits disposable income despite salaries, mobile-first non-negotiable (local train culture), Dharavi to Bandra economic diversity means pricing tiers matter enormously, UPSC/banking exam culture strong, Marathi/Hindi/English trilingual market."
    },
    "🇮🇳 Delhi NCR": {
        "name": "Delhi NCR",
        "context": "Market: Delhi NCR, India. Currency: ₹. Key realities: UPSC dominant career aspiration, government job security valued over startup culture, Kota coaching migration affects secondary market, extreme income disparity, competitive exam culture (SSC, banking, IAS) massive, Hindi-first market with English aspiration."
    },
    "🇮🇳 Bengaluru": {
        "name": "Bengaluru",
        "context": "Market: Bengaluru, India (startup and tech capital). Currency: ₹. Key realities: highest density of tech-savvy early adopters in India, SaaS and B2B find early traction here, most saturated with ed-tech competitors, English-first professional culture, high disposable income in IT sector but jaded by too many subscriptions."
    },
    "🇮🇳 Tier-2 India": {
        "name": "Tier-2 India",
        "context": "Market: Tier-2/3 Indian cities (Nagpur, Patna, Lucknow, Coimbatore etc). Currency: ₹. Key realities: ₹99/month is a real purchase decision, parents control all student spending, coaching centre culture even stronger than metros, first-generation learners, Jio-driven mobile internet but low desktop access, vernacular language crucial, trust built through relatives and teachers not ads."
    },
    "🇳🇬 Lagos": {
        "name": "Lagos",
        "context": "Market: Lagos, Nigeria. Currency: Naira (₦). Key realities: massive youth population, fintech-forward (Flutterwave/Paystack ecosystem), mobile money primary, data costs significant friction, trust deficit with new products, WAEC/JAMB exam culture dominant, WhatsApp commerce primary channel."
    },
    "🇰🇪 Nairobi": {
        "name": "Nairobi",
        "context": "Market: Nairobi, Kenya. Currency: KES. Key realities: M-Pesa mobile money means low payment friction, strong tech community (Silicon Savannah), KCPE/KCSE exam culture drives education spend, middle class growing but price-sensitive, English and Swahili bilingual market."
    },
    "🇺🇸 United States": {
        "name": "United States",
        "context": "Market: United States. Currency: USD. Key realities: highest willingness to pay for SaaS globally, credit card penetration near 100%, individualistic decision-making, student loan debt crisis makes career ROI salient, LinkedIn-driven professional networking, strong data/privacy regulation."
    },
    "🇬🇧 United Kingdom": {
        "name": "United Kingdom",
        "context": "Market: United Kingdom. Currency: GBP. Key realities: strong skepticism of American-style hustle culture, NHS/public sector employment valued, UCAS application pressure, class dynamics affect aspiration signaling, London vs rest-of-UK massive divide, GDPR compliance non-negotiable."
    },
    "🌍 Other (describe below)": {
        "name": "Custom",
        "context": ""
    }
}


def build_prompt(idea: str, location_name: str, location_context: str) -> str:
    return f"""You are PMFit AI — a structured startup idea evaluation engine. You operate like a FICO score for startup ideas: precise, evidence-based, and useful. You are truthful and strategic, not motivational and not purely critical.

IDEA SUBMITTED:
"{idea}"

MARKET CONTEXT — shape every sentence around this:
{location_context}

YOUR PHILOSOPHY:
- Truth is more useful than encouragement or discouragement
- A 28/100 with a clear path forward is more valuable than a 72/100 with vague praise
- Separate what you KNOW from what you ASSUME — label them explicitly
- Every weakness must come with its strategic implication
- Every strength must be real — do not manufacture positives
- The goal is to make the founder think clearly, not feel good or bad

CONFIDENCE LABELING — use exactly these labels:
HIGH CONFIDENCE — based on verifiable market data, named competitors, documented behavior
MEDIUM CONFIDENCE — reasonable inference from market patterns, not directly verified
ASSUMPTION — based on what the founder stated without external validation

BANNED PHRASES: "iterate rapidly", "build a universe", "Series B", "delight users", "leverage synergies", "scalable solution", "disrupt the market", "game changer", "revolutionary", "product-market fit journey"

Respond with EXACTLY these headers in this order:

VERDICT
One blunt specific sentence on where this idea stands in this market. Name the single market reality that most determines success or failure here.

PMF SCORE: [number 0-100]
Two sentences. First: what drove the score up. Second: what drove it down. Both specific to this market.

WHAT IS ACTUALLY WORKING
2-4 genuine strengths. For each: state the strength, then on a new line write HIGH CONFIDENCE, MEDIUM CONFIDENCE, or ASSUMPTION followed by a colon and why you labeled it that way. Only include real strengths that hold up under scrutiny.

WHAT IS ACTUALLY NOT WORKING
2-4 real weaknesses. For each: state the weakness, then on a new line write the confidence label and the strategic implication — not just what is wrong but what it means for the founder's next move.

MARKET REALITY CHECK
3 observations about how this specific market works that directly affect this idea. Name real companies, real price points, real platforms. Each followed by its confidence label.

ASSUMPTIONS YOU ARE MAKING
List every significant unvalidated assumption embedded in this idea. Be precise — not "you assume there is demand" but "you assume that [specific user] will [specific behavior] — this has not been demonstrated." This is the founder's validation checklist.

VIABLE PATH FORWARD
Strategy, not motivation. Given the score and market realities — what is the single most intelligent route to making this work? If a pivot is needed, name it specifically. If viable as stated, describe the exact sequence. 3-5 sentences. Be direct.

HIGHEST LEVERAGE MOVE
One specific action in the next 7 days. Zero budget. Name the exact platform, the exact message or action, what they are testing, and what a positive result looks like versus a negative result.

SHARP OBSERVATION
One thing uniquely true about this idea in this specific market that most advisors would miss."""


def parse_result(text: str) -> dict:
    patterns = {
        "verdict":     r"VERDICT\n([\s\S]*?)(?=PMF SCORE:|$)",
        "score":       r"PMF SCORE:\s*\[?(\d+)\]?([\s\S]*?)(?=WHAT IS ACTUALLY WORKING|$)",
        "pros":        r"WHAT IS ACTUALLY WORKING\n([\s\S]*?)(?=WHAT IS ACTUALLY NOT WORKING|$)",
        "cons":        r"WHAT IS ACTUALLY NOT WORKING\n([\s\S]*?)(?=MARKET REALITY CHECK|$)",
        "reality":     r"MARKET REALITY CHECK\n([\s\S]*?)(?=ASSUMPTIONS YOU ARE MAKING|$)",
        "assumptions": r"ASSUMPTIONS YOU ARE MAKING\n([\s\S]*?)(?=VIABLE PATH FORWARD|$)",
        "path":        r"VIABLE PATH FORWARD\n([\s\S]*?)(?=HIGHEST LEVERAGE MOVE|$)",
        "leverage":    r"HIGHEST LEVERAGE MOVE\n([\s\S]*?)(?=SHARP OBSERVATION|$)",
        "sharp":       r"SHARP OBSERVATION\n([\s\S]*?)$",
    }
    result = {"raw": text}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if key == "score":
                result["score_num"] = int(match.group(1))
                result["score_context"] = match.group(2).strip()
            else:
                result[key] = match.group(1).strip()
    if "score_num" not in result:
        m = re.search(r"(\d{1,3})\s*/\s*100", text)
        result["score_num"] = int(m.group(1)) if m else None
        result["score_context"] = ""
    return result


def render_confidence_blocks(text: str):
    if not text:
        return
    # Split on numbered items or double newlines
    items = re.split(r'\n\n+|\n(?=\d+\.)', text)
    for item in items:
        item = item.strip()
        if not item:
            continue
        upper = item.upper()
        if "HIGH CONFIDENCE" in upper:
            parts = re.split(r'HIGH CONFIDENCE', item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-high">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#22c55e">● High Confidence</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        elif "MEDIUM CONFIDENCE" in upper:
            parts = re.split(r'MEDIUM CONFIDENCE', item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-medium">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#fbbf24">◐ Medium Confidence</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        elif "ASSUMPTION" in upper:
            parts = re.split(r'ASSUMPTION', item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-assumption">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#64748b">○ Assumption — Not Verified</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="btext" style="padding:6px 0">{item}</div>', unsafe_allow_html=True)


def score_color(s):
    if s is None: return "#6b7280"
    if s >= 70: return "#22c55e"
    if s >= 45: return "#f59e0b"
    return "#ef4444"

def score_label(s):
    if s is None: return "Unscored"
    if s >= 70: return "Strong PMF signal"
    if s >= 45: return "Moderate signal"
    return "Weak signal — keep digging"


def main():
    st.markdown('<div class="eyebrow">PMFit AI · v4 · Confidence-Layered</div>', unsafe_allow_html=True)
    st.markdown("# Does your idea fit\nyour actual market?")
    st.markdown(
        '<p style="color:#475569;font-size:0.9rem;margin-top:-0.5rem;margin-bottom:1.5rem;">'
        'Structured PMF analysis. Separates facts from assumptions. Location-specific. Honest about both sides.'
        '</p>', unsafe_allow_html=True
    )
    st.divider()

    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("API key not configured.")
        st.stop()

    st.markdown("## Your Idea")
    idea = st.text_area(
        "idea",
        placeholder="What is it? Who is it for? What problem does it solve? Be specific.",
        height=110,
        label_visibility="collapsed"
    )

    st.markdown("## Your Market")
    location_key = st.selectbox("market", options=list(LOCATIONS.keys()), label_visibility="collapsed")
    loc_data = LOCATIONS[location_key]
    custom_context = ""
    if loc_data["name"] == "Custom":
        custom_context = st.text_area(
            "market context",
            placeholder="City/country, currency, cultural dynamics, key competitors, price sensitivity, communication channels, major barriers...",
            height=100,
            label_visibility="collapsed"
        )
    location_context = custom_context if loc_data["name"] == "Custom" else loc_data["context"]

    st.divider()

    if st.button("Analyze PMF →", use_container_width=True):
        if not idea.strip():
            st.error("Describe your idea first.")
            return
        if loc_data["name"] == "Custom" and not custom_context.strip():
            st.error("Describe your market context.")
            return

        with st.spinner(f"Analyzing for {loc_data['name']}..."):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                message = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": build_prompt(idea, loc_data["name"], location_context)}]
                )
                raw_text = message.content[0].text
                result = parse_result(raw_text)

                st.divider()

                # Score
                score = result.get("score_num")
                color = score_color(score)
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown(
                        f'<div class="big-score" style="color:{color}">{score if score else "—"}</div>'
                        f'<div style="font-size:0.7rem;color:#334155;font-family:DM Mono,monospace;margin-top:4px">/ 100</div>',
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f'<div style="font-size:1rem;font-weight:600;color:{color};margin-bottom:4px">{score_label(score)}</div>'
                        f'<div style="font-size:12px;color:#64748b;line-height:1.65">{result.get("score_context","")}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.15);'
                    f'border-radius:8px;padding:8px 14px;font-size:11px;color:#64748b;margin:12px 0">'
                    f'{location_key.split()[0]} Grounded in <strong style="color:#94a3b8">{loc_data["name"]}</strong> market dynamics'
                    f'</div>', unsafe_allow_html=True
                )

                # Verdict
                if result.get("verdict"):
                    st.markdown("## Verdict")
                    st.markdown(f'<div class="section-card"><div class="vtext">{result["verdict"]}</div></div>', unsafe_allow_html=True)

                # Pros
                if result.get("pros"):
                    st.markdown("## What Is Actually Working")
                    st.markdown('<div class="pros-card">', unsafe_allow_html=True)
                    render_confidence_blocks(result["pros"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Cons
                if result.get("cons"):
                    st.markdown("## What Is Actually Not Working")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    render_confidence_blocks(result["cons"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Reality
                if result.get("reality"):
                    st.markdown("## Market Reality Check")
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    render_confidence_blocks(result["reality"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # Assumptions
                if result.get("assumptions"):
                    st.markdown("## Assumptions You Are Making")
                    st.markdown(
                        '<p style="font-size:12px;color:#475569;margin-bottom:10px">'
                        'Everything your idea depends on that has not yet been validated. This is your validation checklist.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    for line in result["assumptions"].split('\n'):
                        if line.strip():
                            st.markdown(
                                f'<div style="font-size:13px;color:#94a3b8;line-height:1.75;'
                                f'padding:7px 0;border-bottom:1px solid #1e2533">{line.strip()}</div>',
                                unsafe_allow_html=True
                            )
                    st.markdown('</div>', unsafe_allow_html=True)

                # Viable path
                if result.get("path"):
                    st.markdown("## Viable Path Forward")
                    st.markdown(
                        f'<div class="path-card">'
                        f'<div class="slabel" style="color:#a78bfa">Strategic direction — not motivation</div>'
                        f'<div class="btext" style="color:#c4b5fd">{result["path"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # Highest leverage
                if result.get("leverage"):
                    st.markdown("## Highest Leverage Move")
                    st.markdown(
                        f'<div class="leverage-card">'
                        f'<div class="slabel" style="color:#38bdf8">Do this in the next 7 days · costs ₹0</div>'
                        f'<div class="btext" style="color:#7dd3fc">{result["leverage"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # Sharp observation
                if result.get("sharp"):
                    st.markdown("## Sharp Observation")
                    st.markdown(
                        f'<div class="section-card" style="border-color:rgba(232,121,249,0.2)">'
                        f'<div class="btext" style="color:#e2e8f0;font-style:italic">{result["sharp"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                st.divider()
                st.markdown(
                    '<p style="text-align:center;font-size:11px;color:#1e2533">'
                    'PMFit AI · Read confidence labels before acting on any finding. '
                    'High confidence = verified. Assumption = go validate this first.</p>',
                    unsafe_allow_html=True
                )

            except anthropic.AuthenticationError:
                st.error("Invalid API key. Check console.anthropic.com → API Keys.")
            except anthropic.RateLimitError:
                st.error("Rate limit hit. Wait 30 seconds and try again.")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

    st.markdown(
        '<p style="text-align:center;font-size:0.72rem;color:#1e2533;margin-top:3rem;">'
        'PMFit AI · Built with Streamlit + Claude</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
