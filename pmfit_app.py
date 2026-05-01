import streamlit as st
import anthropic
import re

# ── PAGE CONFIG ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PMFit AI",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #08090c;
    color: #e2e8f0;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 640px; }

/* Headings */
h1 { 
    font-size: 2.2rem !important; 
    font-weight: 700 !important; 
    letter-spacing: -0.02em !important;
    color: #f1f5f9 !important;
    line-height: 1.15 !important;
}
h2 { 
    font-size: 1rem !important; 
    font-weight: 600 !important;
    color: #38bdf8 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
h3 {
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Text inputs and textareas */
textarea, input[type="text"] {
    background-color: #0f1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #0f1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* Buttons */
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
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Score card */
.score-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 20px;
}

/* Section cards */
.section-card {
    background: #0f1117;
    border: 1px solid #1e2533;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
}

/* Eyebrow label */
.eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.5rem;
}

/* Template boxes */
.template-box {
    background: #080a0f;
    border: 1px solid #1e2533;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 10px 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #94a3b8;
    line-height: 1.8;
    white-space: pre-wrap;
}

/* Info/warn boxes */
.info-box {
    background: rgba(56,189,248,0.06);
    border-left: 2px solid #38bdf8;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #7dd3fc;
    line-height: 1.65;
    margin: 10px 0;
}
.warn-box {
    background: rgba(251,191,36,0.06);
    border-left: 2px solid #fbbf24;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #fcd34d;
    line-height: 1.65;
    margin: 10px 0;
}
.success-box {
    background: rgba(34,197,94,0.06);
    border-left: 2px solid #22c55e;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #86efac;
    line-height: 1.65;
    margin: 10px 0;
}

/* Divider */
hr { border-color: #1e2533 !important; margin: 1.5rem 0 !important; }

/* Metric */
.big-score {
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ── LOCATION DATA ──────────────────────────────────────────────────────
LOCATIONS = {
    "🇮🇳 Hyderabad": {
        "name": "Hyderabad",
        "context": (
            "Market: Hyderabad, India (Tier-1 city). Currency: Indian Rupees (₹). "
            "Key realities: intense JEE/NEET/CA exam pressure culture, strong coaching institute ecosystem "
            "(BYJU's, Allen, Unacademy already dominant), parental decision-making power over children's education spending, "
            "extreme price sensitivity (₹99/month feels different from ₹999/month), pharma/IT/finance job market is "
            "hyper-competitive, tier-2 city students increasingly aspirational but cash-strapped, family-first culture "
            "means B2C education products need parent buy-in not just student buy-in, WhatsApp is the primary "
            "communication channel not email."
        )
    },
    "🇮🇳 Mumbai": {
        "name": "Mumbai",
        "context": (
            "Market: Mumbai, India (financial capital). Currency: ₹. Key realities: finance career aspirations "
            "are intense (CA, CFA, investment banking), extremely high cost of living means disposable income for "
            "ed-products is limited despite salaries, local train culture means mobile-first is non-negotiable, "
            "Dharavi to Bandra economic diversity means pricing tiers matter enormously, UPSC/banking exam culture strong, "
            "Marathi/Hindi/English trilingual market."
        )
    },
    "🇮🇳 Delhi NCR": {
        "name": "Delhi NCR",
        "context": (
            "Market: Delhi NCR, India. Currency: ₹. Key realities: UPSC is a dominant career aspiration, "
            "government job security valued over startup culture, Kota coaching migration affects secondary market, "
            "extreme income disparity between South Delhi and outer NCR, competitive exam culture (SSC, banking, IAS) "
            "is massive, Hindi-first market with English aspiration."
        )
    },
    "🇮🇳 Bengaluru": {
        "name": "Bengaluru",
        "context": (
            "Market: Bengaluru, India (startup and tech capital). Currency: ₹. Key realities: highest density of "
            "tech-savvy early adopters in India, SaaS and B2B products find early traction here, startup ecosystem "
            "means founders understand product language, but also most saturated with ed-tech competitors, "
            "English-first professional culture, high disposable income in IT sector but jaded by too many subscriptions, "
            "Kannada-speaking local population often underserved."
        )
    },
    "🇮🇳 Tier-2 India": {
        "name": "Tier-2 India",
        "context": (
            "Market: Tier-2/3 Indian cities (Nagpur, Patna, Lucknow, Coimbatore etc). Currency: ₹. "
            "Key realities: ₹99/month is a real purchase decision, parents control all spending for students under 22, "
            "aspirational toward metros but local job market is limited, coaching centre culture even stronger than metros, "
            "first-generation learners, Jio-driven mobile internet penetration but low desktop access, "
            "vernacular language crucial, trust built through relatives and teachers not ads."
        )
    },
    "🇳🇬 Lagos": {
        "name": "Lagos",
        "context": (
            "Market: Lagos, Nigeria. Currency: Naira (₦). Key realities: massive youth population with strong "
            "entrepreneurial energy, fintech-forward (Flutterwave/Paystack ecosystem), mobile money primary, "
            "data costs are significant friction, trust deficit with new products (scam-awareness high), "
            "WAEC/JAMB exam culture dominant, WhatsApp commerce is primary channel."
        )
    },
    "🇰🇪 Nairobi": {
        "name": "Nairobi",
        "context": (
            "Market: Nairobi, Kenya. Currency: KES. Key realities: M-Pesa mobile money penetration means payment "
            "friction is low, strong tech community (Silicon Savannah), KCPE/KCSE exam culture drives education spend, "
            "middle class growing but price-sensitive, English and Swahili bilingual market."
        )
    },
    "🇺🇸 United States": {
        "name": "United States",
        "context": (
            "Market: United States. Currency: USD. Key realities: highest willingness to pay for SaaS globally, "
            "credit card penetration near 100%, individualistic decision-making, student loan debt crisis makes "
            "career ROI salient, LinkedIn-driven professional networking, strong regulation around data and privacy."
        )
    },
    "🇬🇧 United Kingdom": {
        "name": "United Kingdom",
        "context": (
            "Market: United Kingdom. Currency: GBP. Key realities: strong skepticism of American-style hustle culture, "
            "NHS/public sector employment valued, university culture different from US, UCAS application pressure, "
            "class dynamics affect aspiration signaling, London vs rest-of-UK is a massive divide, GDPR compliance non-negotiable."
        )
    },
    "🌍 Other (describe below)": {
        "name": "Custom",
        "context": ""
    }
}

# ── TEMPLATES ──────────────────────────────────────────────────────────
TEMPLATES = {
    "customer_interview": {
        "title": "Customer Interview — Word-for-Word Guide",
        "content": """HOW TO FIND PEOPLE
Post in relevant WhatsApp groups, Reddit communities, or LinkedIn.
DM 20 people directly — expect 5 to respond.
Do NOT interview friends or family. Find strangers who match your target user.

OPENING SCRIPT (say this exactly)
"Hi [Name], I'm building something for [target user type] and I'm doing research —
not selling anything. Would you have 15 minutes this week for a quick call?
I'd love to understand your experience with [problem area]."

QUESTIONS TO ASK
1. "Walk me through the last time you dealt with [problem]. What happened?"
2. "What did you do to solve it? What tools or people did you use?"
3. "What was the most frustrating part?"
4. "How much does this problem cost you — in time, money, or stress?"
5. "Have you ever paid for a solution? Why or why not?"
6. "If a perfect solution existed, what would it look like?"

WHAT 'GOOD' LOOKS LIKE
✓ They describe the problem without being prompted
✓ They mention having tried something else already
✓ They use emotional language ("hate", "waste", "stress")
✓ They ask when your product will be ready
✗ They say "yeah that would be cool" but can't describe the problem specifically

AFTER THE INTERVIEW
Write 3 bullet points within 1 hour:
- What surprised you
- What confirmed your hypothesis
- What you'd change about the product"""
    },
    "cold_outreach": {
        "title": "Cold Outreach — Copy-Paste Scripts",
        "content": """WHATSAPP / SMS (India-specific, best channel)
"Hi [Name], I got your number from [mutual contact/group].
I'm building something for [specific problem] and doing research.
Can I ask you 5 quick questions over text or a 10-min call?
No sales, just learning."

LINKEDIN MESSAGE (under 75 words)
"Hi [Name] — I'm building a tool for [target user] and I'm doing
15-minute research calls this week. No pitch, just questions.
Your profile looks like exactly the right person to talk to.
Would you be open to a quick call?"

WHAT MAKES PEOPLE RESPOND
✓ Specific — mention something about them personally
✓ Short — under 75 words always
✓ No jargon — "startup", "pivot", "traction" → don't use these
✓ Low commitment ask — "15 minutes" not "detailed feedback session"
✗ Never start with "I hope this message finds you well"
✗ Never attach a pitch deck in the first message"""
    },
    "pricing": {
        "title": "Pricing Experiment — How to Test What People Will Pay",
        "content": """NEVER ASK "HOW MUCH WOULD YOU PAY?"
People always lie downward. Instead ask:
"We're thinking of charging ₹[X]/month. Does that feel too low,
about right, or too high?"
Then shut up and wait. Their hesitation tells you more than their words.

THE VAN WESTENDORP METHOD (simplified)
Ask 4 questions:
1. "At what price would this feel too cheap to trust?"
2. "At what price would this feel like a bargain?"
3. "At what price would you start thinking it's getting expensive?"
4. "At what price would you definitely not buy it?"
Ask 10+ people. Your price lives between answers 2 and 3.

INDIA PRICING TIERS
₹99/month  → impulse buy, no decision needed
₹299/month → considered purchase, needs proof of value
₹999/month → requires parent/institutional approval
₹2999/month → B2B territory, needs procurement process

ANCHOR TO OUTCOMES, NOT PRICE
"Less than one coaching class session" beats "₹499/month" every time.
"Save 3 hours of prep time" beats "comprehensive platform" every time."""
    },
    "waitlist": {
        "title": "Build a Waitlist — Free Setup in 30 Minutes",
        "content": """THE FASTEST SETUP (free, 30 minutes)
1. Create a Google Form with:
   - Name
   - Email or WhatsApp number
   - "What's your biggest challenge with [problem]?"
2. Share the link everywhere:
   WhatsApp groups, Reddit, LinkedIn, Instagram bio
3. Set a goal: 100 signups before building anything
4. DM every single person who signs up within 24 hours

WHAT TO SAY ON THE LANDING PAGE
Headline: State the outcome, not the product
  Bad:  "AI-powered career platform"
  Good: "Know which finance career fits you before wasting 3 years finding out"

Sub-headline: Who it's for + the specific pain
CTA button: "Join 200 students on the waitlist" (social proof matters)

SUCCESS METRIC
If fewer than 5% of visitors sign up:
→ your message isn't resonating, not your idea
→ rewrite the headline and test again before assuming the idea is wrong"""
    },
    "manual_simulation": {
        "title": "Manual Simulation — Be the Algorithm Before You Build It",
        "content": """WHAT THIS MEANS
Before building software, do the thing manually.
If your product matches students to careers → manually match them.
If it scores resumes → manually score them.
You are the algorithm. Prove it works on humans first.

HOW TO RUN IT
Step 1: Find 5–10 real users (not friends, actual target users)
Step 2: Run the core interaction via WhatsApp/Google Meet/email
Step 3: Deliver the result manually (even if it takes you 2 hours)
Step 4: Ask them: "Was this valuable? Would you pay ₹X for this?"
Step 5: Do this 10 times before writing a single line of code

WHAT TO TRACK (keep a simple doc)
- Date and user name
- What they submitted / asked
- What you gave them back
- Their exact reaction (quote them)
- Would they pay? Y/N
- How much?

SUCCESS SIGNALS
✓ 3 out of 10 users ask "when can I use this regularly?"
✓ 2 out of 10 offer to pay without being asked
✓ You can describe the core value in one sentence after doing it
✗ Everyone says "great idea" but nobody asks for it again"""
    },
    "competitor_analysis": {
        "title": "Competitor Analysis — Find Who You're Actually Up Against",
        "content": """FIND THEM (don't guess)
1. Google "[problem] app India", "[problem] platform", "[problem] tool"
2. Search the Play Store for your core keyword
3. Search r/india, r/IndiaTech, r/indianstartups for the problem
4. Post in 3 WhatsApp groups: "What do you use for [problem]?"
   → The last method finds your REAL competitors, the ones users know

WHAT TO EVALUATE FOR EACH COMPETITOR
- Pricing (what tier, annual vs monthly)
- Play Store reviews (1-star reviews = your opportunity list)
- What they don't do (gaps in features)
- Who they ignore (their target user vs yours)
- How they acquire users (ads, SEO, word-of-mouth?)

THE 1-STAR REVIEW GOLDMINE
Go to the Play Store page of every competitor.
Read ALL 1 and 2-star reviews.
Copy the exact phrases users use to describe what's broken or missing.
These are:
→ Your product's reasons to exist
→ Your exact marketing language
→ The features you build first"""
    }
}

# ── KEYWORD → TEMPLATE MAPPING ─────────────────────────────────────────
KEYWORD_MAP = [
    (["interview", "talk to", "speak to", "survey", "ask students", "ask users"], "customer_interview"),
    (["cold outreach", "reach out", "contact potential", "dm ", "message potential"], "cold_outreach"),
    (["pricing", "price point", "charge", "willingness to pay", "₹", "rupee"], "pricing"),
    (["waitlist", "landing page", "pre-launch", "early access", "signups"], "waitlist"),
    (["manual simulation", "simulate manually", "do it manually", "manually"], "manual_simulation"),
    (["competitor", "competition", "alternatives", "existing solutions", "benchmark"], "competitor_analysis"),
]

def find_template_key(text: str) -> str | None:
    lower = text.lower()
    for keywords, key in KEYWORD_MAP:
        if any(kw in lower for kw in keywords):
            return key
    return None

def highlight_actionable_phrases(text: str) -> tuple[str, list[str]]:
    """Returns displayed text and list of found template keys"""
    found_keys = []
    lower = text.lower()
    for keywords, key in KEYWORD_MAP:
        if any(kw in lower for kw in keywords) and key not in found_keys:
            found_keys.append(key)
    return text, found_keys

# ── AI CALL ────────────────────────────────────────────────────────────
def build_prompt(idea: str, location_name: str, location_context: str) -> str:
    return f"""You are a PMF (Product-Market Fit) analyst. You give precise, market-specific analysis — not generic startup advice.

IDEA:
"{idea}"

MARKET CONTEXT — READ THIS CAREFULLY AND LET IT SHAPE EVERY WORD YOU WRITE:
{location_context}

CRITICAL RULES:
1. Every sentence must be specific to this idea AND this market. Zero generic startup bingo phrases.
2. Use local currency, local examples, local competitors, local cultural realities.
3. Reference real behaviours, real platforms, real channels that exist in this market.
4. When you suggest an action, name the exact platform, channel, or method relevant to this market.
5. BANNED phrases: "product-market fit journey", "iterate rapidly", "build a universe", "Series B", "delight users", "leverage synergies", "scalable solution", "disrupt the market".

Respond in EXACTLY this structure with these exact headers:

VERDICT
One blunt sentence on whether this idea has a real market here. Name the specific market reality that most affects this idea.

PMF SCORE: [number 0-100]
Two sentences explaining the score — tied to this specific market, not generic.

MARKET REALITY CHECK
3 specific observations about how this market actually works that directly affect this idea. Name real companies, platforms, price points, behaviours.

TOP 3 GAPS
The 3 biggest missing pieces for PMF — each tied to a specific local market dynamic.

ACTION PLAN
5 sequential steps the founder can take right now. Each step must name the exact platform or channel to use (not "social media" — which platform, which group). Include a specific success metric for each step.

BIGGEST RISKS
3 risks specific to this idea in this specific market. Name real competitors or cultural blockers.

SHARP OBSERVATION
One thing that is uniquely true about this idea in this specific market that most advisors would miss."""

def call_anthropic(idea: str, location_name: str, location_context: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1400,
        messages=[{
            "role": "user",
            "content": build_prompt(idea, location_name, location_context)
        }]
    )
    return message.content[0].text

# ── PARSE RESULT ───────────────────────────────────────────────────────
def parse_result(text: str) -> dict:
    patterns = {
        "verdict":  r"VERDICT\n([\s\S]*?)(?=PMF SCORE:|$)",
        "score":    r"PMF SCORE:\s*\[?(\d+)\]?([\s\S]*?)(?=MARKET REALITY|$)",
        "reality":  r"MARKET REALITY CHECK\n([\s\S]*?)(?=TOP 3 GAPS|$)",
        "gaps":     r"TOP 3 GAPS\n([\s\S]*?)(?=ACTION PLAN|$)",
        "actions":  r"ACTION PLAN\n([\s\S]*?)(?=BIGGEST RISKS|$)",
        "risks":    r"BIGGEST RISKS\n([\s\S]*?)(?=SHARP OBSERVATION|$)",
        "sharp":    r"SHARP OBSERVATION\n([\s\S]*?)$",
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

def score_color(score: int | None) -> str:
    if score is None: return "#6b7280"
    if score >= 70: return "#22c55e"
    if score >= 45: return "#f59e0b"
    return "#ef4444"

def score_label(score: int | None) -> str:
    if score is None: return "Unscored"
    if score >= 70: return "Strong PMF signal"
    if score >= 45: return "Moderate signal"
    return "Weak signal — keep digging"

# ── MAIN APP ───────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown('<div class="eyebrow">PMFit AI · Market-Aware Edition</div>', unsafe_allow_html=True)
    st.markdown("# Does your idea fit\nyour actual market?")
    st.markdown(
        '<p style="color:#475569;font-size:0.9rem;margin-top:-0.5rem;margin-bottom:1.5rem;">'
        'Location-aware PMF analysis. Expand any action step below for scripts and templates.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # ── API KEY ──
    st.markdown("### 🔑 Anthropic API Key")
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("API key not configured. Contact the app owner.")
        st.stop()

    st.divider()

    # ── IDEA INPUT ──
    st.markdown("### 💡 Your Idea")
    idea = st.text_area(
        "Describe your idea",
        placeholder="What is it, who is it for, what problem does it solve? Be specific.",
        height=100,
        label_visibility="collapsed"
    )

    # ── LOCATION ──
    st.markdown("### 📍 Your Market")
    location_key = st.selectbox(
        "Select your market",
        options=list(LOCATIONS.keys()),
        label_visibility="collapsed"
    )

    loc_data = LOCATIONS[location_key]
    custom_context = ""

    if loc_data["name"] == "Custom":
        custom_context = st.text_area(
            "Describe your market",
            placeholder=(
                "City/country, currency, cultural dynamics, key competitors, "
                "price sensitivity, how people communicate (WhatsApp? email?), major barriers..."
            ),
            height=100,
            label_visibility="collapsed"
        )

    location_context = custom_context if loc_data["name"] == "Custom" else loc_data["context"]

    st.divider()

    # ── SUBMIT ──
    analyze_clicked = st.button("Analyze PMF →", use_container_width=True)

    # ── ANALYSIS ──
    if analyze_clicked:
        if not api_key:
            st.error("Add your Anthropic API key above to continue.")
        elif not idea.strip():
            st.error("Describe your idea first.")
        elif loc_data["name"] == "Custom" and not custom_context.strip():
            st.error("Describe your market context.")
        else:
            with st.spinner(f"Analyzing for {loc_data['name']}..."):
                try:
                    raw_text = call_anthropic(idea, loc_data["name"], location_context, api_key)
                    result = parse_result(raw_text)

                    st.divider()

                    # Score card
                    score = result.get("score_num")
                    color = score_color(score)
                    label = score_label(score)

                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(
                            f'<div class="big-score" style="color:{color}">{score if score else "—"}</div>'
                            f'<div style="font-size:0.7rem;color:#334155;font-family:DM Mono,monospace">/ 100</div>',
                            unsafe_allow_html=True
                        )
                    with col2:
                        st.markdown(
                            f'<div style="font-size:1.1rem;font-weight:600;color:{color};margin-bottom:6px">{label}</div>'
                            f'<div style="font-size:0.82rem;color:#64748b;line-height:1.65">{result.get("score_context","")}</div>',
                            unsafe_allow_html=True
                        )

                    # Market badge
                    st.markdown(
                        f'<div class="info-box" style="margin-top:12px">'
                        f'{location_key.split()[0]} Analysis grounded in <strong>{loc_data["name"]}</strong> market dynamics'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    st.divider()

                    # ── VERDICT ──
                    if result.get("verdict"):
                        st.markdown("### Verdict")
                        st.markdown(
                            f'<div class="section-card"><p style="font-size:0.9rem;color:#e2e8f0;line-height:1.75">'
                            f'{result["verdict"]}</p></div>',
                            unsafe_allow_html=True
                        )

                    # ── MARKET REALITY ──
                    if result.get("reality"):
                        st.markdown("### Market Reality Check")
                        st.markdown(
                            f'<div class="section-card">'
                            f'<p style="font-size:0.85rem;color:#94a3b8;line-height:1.8;white-space:pre-wrap">'
                            f'{result["reality"]}</p></div>',
                            unsafe_allow_html=True
                        )

                    # ── GAPS ──
                    if result.get("gaps"):
                        st.markdown("### Top 3 Gaps")
                        st.markdown(
                            f'<div class="section-card">'
                            f'<p style="font-size:0.85rem;color:#94a3b8;line-height:1.8;white-space:pre-wrap">'
                            f'{result["gaps"]}</p></div>',
                            unsafe_allow_html=True
                        )

                    # ── ACTION PLAN with expandable templates ──
                    if result.get("actions"):
                        st.markdown("### Action Plan")
                        st.markdown(
                            '<div class="warn-box">Tap any expander below for word-for-word scripts, '
                            'templates, and success metrics.</div>',
                            unsafe_allow_html=True
                        )
                        st.markdown(
                            f'<div class="section-card">'
                            f'<p style="font-size:0.85rem;color:#e2e8f0;line-height:1.8;white-space:pre-wrap">'
                            f'{result["actions"]}</p></div>',
                            unsafe_allow_html=True
                        )

                        # Find relevant templates
                        _, found_keys = highlight_actionable_phrases(result["actions"])

                        if found_keys:
                            st.markdown(
                                '<p style="font-size:0.75rem;color:#475569;margin-top:6px;">'
                                'Playbooks for actions mentioned above ↓</p>',
                                unsafe_allow_html=True
                            )
                            for key in found_keys:
                                tpl = TEMPLATES.get(key)
                                if tpl:
                                    with st.expander(f"📋 {tpl['title']}"):
                                        st.markdown(
                                            f'<div class="template-box">{tpl["content"]}</div>',
                                            unsafe_allow_html=True
                                        )

                    # ── RISKS ──
                    if result.get("risks"):
                        st.markdown("### Biggest Risks")
                        st.markdown(
                            f'<div class="section-card">'
                            f'<p style="font-size:0.85rem;color:#94a3b8;line-height:1.8;white-space:pre-wrap">'
                            f'{result["risks"]}</p></div>',
                            unsafe_allow_html=True
                        )

                    # ── SHARP OBSERVATION ──
                    if result.get("sharp"):
                        st.markdown("### Sharp Observation")
                        st.markdown(
                            f'<div class="section-card" style="border-color:rgba(232,121,249,0.2)">'
                            f'<p style="font-size:0.88rem;color:#e2e8f0;line-height:1.8;font-style:italic">'
                            f'{result["sharp"]}</p></div>',
                            unsafe_allow_html=True
                        )

                    st.divider()

                    # All templates at the bottom regardless
                    st.markdown("### 📚 Full Playbook Library")
                    st.markdown(
                        '<p style="font-size:0.8rem;color:#475569;">Even if not mentioned above — '
                        'use these for your next steps.</p>',
                        unsafe_allow_html=True
                    )
                    for key, tpl in TEMPLATES.items():
                        with st.expander(f"📋 {tpl['title']}"):
                            st.markdown(
                                f'<div class="template-box">{tpl["content"]}</div>',
                                unsafe_allow_html=True
                            )

                except anthropic.AuthenticationError:
                    st.error("Invalid API key. Check it at console.anthropic.com → API Keys.")
                except anthropic.RateLimitError:
                    st.error("Rate limit hit. Wait 30 seconds and try again.")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

    # Footer
    st.markdown(
        '<p style="text-align:center;font-size:0.72rem;color:#1e2533;margin-top:3rem;">'
        'PMFit AI · Built with Streamlit + Claude</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
