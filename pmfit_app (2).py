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
.momentum-card {
    background: rgba(34,197,94,0.06);
    border: 1px solid rgba(34,197,94,0.25);
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
.fix-path {
    background: rgba(56,189,248,0.04);
    border-left: 2px solid rgba(56,189,248,0.3);
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 12px;
    color: #7dd3fc;
    line-height: 1.65;
}
.reversal-box {
    background: rgba(167,139,250,0.04);
    border-left: 2px solid rgba(167,139,250,0.3);
    border-radius: 0 6px 6px 0;
    padding: 8px 12px;
    margin-top: 8px;
    font-size: 12px;
    color: #c4b5fd;
    line-height: 1.65;
}
.reality-block {
    background: rgba(56,189,248,0.03);
    border: 1px solid rgba(56,189,248,0.1);
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.interpretation-block {
    background: rgba(251,191,36,0.03);
    border: 1px solid rgba(251,191,36,0.1);
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
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
.hint-box {
    background: rgba(251,191,36,0.06);
    border: 1px solid rgba(251,191,36,0.15);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 11px;
    color: #a16207;
    margin-bottom: 16px;
    line-height: 1.6;
}
hr { border-color: #1e2533 !important; margin: 1.5rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOCATIONS ──────────────────────────────────────────────────────────
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
✓ No jargon — "startup", "pivot", "traction" don't use these
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
   The last method finds your REAL competitors — the ones users know

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

KEYWORD_MAP = [
    (["interview", "talk to", "speak to", "survey", "ask users", "ask customers", "ask students"], "customer_interview"),
    (["cold outreach", "reach out", "contact potential", "dm ", "message potential", "find users"], "cold_outreach"),
    (["pricing", "price point", "charge", "willingness to pay", "₹", "rupee", "monetize"], "pricing"),
    (["waitlist", "landing page", "pre-launch", "early access", "signups"], "waitlist"),
    (["manual simulation", "simulate manually", "do it manually", "manually", "wizard of oz"], "manual_simulation"),
    (["competitor", "competition", "alternatives", "existing solutions", "benchmark"], "competitor_analysis"),
]


def find_template_keys(text: str) -> list:
    found = []
    lower = text.lower()
    for keywords, key in KEYWORD_MAP:
        if any(kw in lower for kw in keywords) and key not in found:
            found.append(key)
    return found


# ── PROMPT ─────────────────────────────────────────────────────────────
def build_prompt(idea: str, location_name: str, location_context: str) -> str:
    return f"""You are PMFit AI — a structured startup idea evaluation engine that thinks WITH founders, not AT them. You are honest, precise, and strategic. You separate observed reality from interpretation. You identify problems AND fix paths. You never assume a founder has no traction or context beyond what they've shared.

IDEA SUBMITTED:
"{idea}"

MARKET CONTEXT — ground every single sentence in this:
{location_context}

YOUR PHILOSOPHY:
- Honest truth delivered well is more useful than harsh truth delivered poorly
- Separate OBSERVED REALITY from your INTERPRETATION of it — label them clearly
- Every problem you name needs a fix path, not just a verdict
- Every assumption needs a reversal: "if this assumption is wrong, here is what changes"
- Tone: direct but not final. You are thinking with the founder, not judging them
- Never use words like "fantasy", "impossible", "doomed" — use "high-risk assumption", "difficult under current behavior patterns", "requires validation"
- The founder may already have traction or context you don't know about — frame conclusions as "current framing suggests..." not "this idea is..."
- End every analysis with momentum, not discouragement

CONFIDENCE LABELING — use exactly these, consistently on every factual claim:
● HIGH CONFIDENCE — verifiable market data, named competitors, documented behavior
◐ MEDIUM CONFIDENCE — reasonable inference from patterns, not directly verified  
○ ASSUMPTION — stated by founder or inferred without external validation

BANNED PHRASES: "fantasy", "impossible", "doomed", "iterate rapidly", "build a universe", "Series B", "delight users", "leverage synergies", "game changer", "revolutionary", "product-market fit journey", "nearly impossible"

TONE RULES:
Instead of "abandon X" → use "reconsider X"
Instead of "your product makes it nearly impossible" → use "current framing creates significant adoption friction"
Instead of "this idea solves the wrong problem" → use "current framing suggests a potential customer mismatch worth testing"

Respond with EXACTLY these sections in this exact order. Use the exact headers shown:

VERDICT
One direct sentence on where this idea currently stands in this market. Frame it as a current observation, not a final judgment. Reference one specific market dynamic.

PMF SCORE: [number 0-100]
Two sentences. First: what is working in this idea's favor in this market. Second: what is creating friction. Both market-specific.

WHAT IS ACTUALLY WORKING
2-4 real strengths. For each strength write:
- The strength itself
- On a new line: the confidence label (● HIGH CONFIDENCE / ◐ MEDIUM CONFIDENCE / ○ ASSUMPTION) and a one-line reason for that label

WHAT IS ACTUALLY NOT WORKING
2-4 friction points. For each write:
- The friction point — framed as an observation, not a verdict
- Confidence label and reason
- Fix paths: 2-3 specific alternative approaches the founder could take to address this friction

REALITY VS INTERPRETATION
Separate what is observed from what is concluded. Write two sub-sections:
OBSERVED PATTERNS: 3 things that are factually documented about this market (label each with confidence)
WHAT THIS SUGGESTS: your interpretation of what those patterns mean for this idea (clearly framed as interpretation, not fact)

ASSUMPTIONS YOU ARE MAKING
List 3-5 significant unvalidated assumptions. For each:
- State the assumption precisely
- Then write: "If this assumption is wrong → [what changes or becomes possible]"
This shows founders what to validate AND what upside exists if their assumptions prove correct.

VIABLE PATH FORWARD
Strategy, not motivation. The most intelligent route given the evidence. If a reframe is needed, describe it specifically. 3-5 sentences. Direct.

HIGHEST LEVERAGE MOVE
One specific action in the next 7 days. Zero budget. Name the exact platform, exact action, what is being tested, and what a positive vs negative result looks like.

MOMENTUM CLOSE
3-4 sentences. Summarise: what is real about this idea, what needs reframing, and why the founder is early rather than wrong. This is not cheerleading — it is an honest reset that keeps the founder moving forward with clarity."""


# ── PARSE ──────────────────────────────────────────────────────────────
def parse_result(text: str) -> dict:
    patterns = {
        "verdict":     r"VERDICT\n([\s\S]*?)(?=PMF SCORE:|$)",
        "score":       r"PMF SCORE:\s*\[?(\d+)\]?([\s\S]*?)(?=WHAT IS ACTUALLY WORKING|$)",
        "pros":        r"WHAT IS ACTUALLY WORKING\n([\s\S]*?)(?=WHAT IS ACTUALLY NOT WORKING|$)",
        "cons":        r"WHAT IS ACTUALLY NOT WORKING\n([\s\S]*?)(?=REALITY VS INTERPRETATION|$)",
        "reality":     r"REALITY VS INTERPRETATION\n([\s\S]*?)(?=ASSUMPTIONS YOU ARE MAKING|$)",
        "assumptions": r"ASSUMPTIONS YOU ARE MAKING\n([\s\S]*?)(?=VIABLE PATH FORWARD|$)",
        "path":        r"VIABLE PATH FORWARD\n([\s\S]*?)(?=HIGHEST LEVERAGE MOVE|$)",
        "leverage":    r"HIGHEST LEVERAGE MOVE\n([\s\S]*?)(?=MOMENTUM CLOSE|$)",
        "momentum":    r"MOMENTUM CLOSE\n([\s\S]*?)$",
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


# ── RENDERERS ──────────────────────────────────────────────────────────
def render_confidence_blocks(text: str, show_fix_paths: bool = False):
    if not text:
        return
    items = re.split(r'\n\n+|\n(?=\d+\.)', text)
    for item in items:
        item = item.strip()
        if not item:
            continue
        upper = item.upper()

        # Extract fix paths if present
        fix_path_match = re.search(r'Fix paths?:([\s\S]*?)$', item, re.IGNORECASE)
        fix_path_text = fix_path_match.group(1).strip() if fix_path_match else ""
        clean_item = item[:fix_path_match.start()].strip() if fix_path_match else item

        if "HIGH CONFIDENCE" in upper or "● HIGH" in upper:
            parts = re.split(r'●?\s*HIGH CONFIDENCE', clean_item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-high">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#22c55e">● High Confidence</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        elif "MEDIUM CONFIDENCE" in upper or "◐ MEDIUM" in upper:
            parts = re.split(r'◐?\s*MEDIUM CONFIDENCE', clean_item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-medium">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#fbbf24">◐ Medium Confidence</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        elif "ASSUMPTION" in upper or "○ ASSUMPTION" in upper:
            parts = re.split(r'○?\s*ASSUMPTION', clean_item, flags=re.IGNORECASE)
            main_text = parts[0].strip().rstrip(':').strip()
            label_text = parts[1].strip().lstrip(':').strip() if len(parts) > 1 else ""
            st.markdown(f"""<div class="confidence-assumption">
                <div class="btext" style="color:#e2e8f0;margin-bottom:8px">{main_text}</div>
                <div class="clabel" style="color:#64748b">○ Assumption — Not Verified</div>
                <div class="btext" style="font-size:12px">{label_text}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="btext" style="padding:6px 0">{clean_item}</div>', unsafe_allow_html=True)

        if fix_path_text:
            st.markdown(
                f'<div class="fix-path"><strong style="color:#38bdf8">Possible fix paths →</strong><br>{fix_path_text}</div>',
                unsafe_allow_html=True
            )


def render_assumptions(text: str):
    if not text:
        return
    items = re.split(r'\n\n+|\n(?=\d+\.|-)', text)
    for item in items:
        item = item.strip()
        if not item:
            continue
        reversal_match = re.search(r'If this assumption is wrong[^→\n]*[→:]([\s\S]*?)$', item, re.IGNORECASE)
        reversal_text = reversal_match.group(1).strip() if reversal_match else ""
        assumption_text = item[:reversal_match.start()].strip() if reversal_match else item

        st.markdown(
            f'<div class="confidence-assumption" style="margin-bottom:4px">'
            f'<div class="clabel" style="color:#64748b">○ Unvalidated Assumption</div>'
            f'<div class="btext" style="color:#e2e8f0">{assumption_text}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
        if reversal_text:
            st.markdown(
                f'<div class="reversal-box">If this is wrong → {reversal_text}</div>',
                unsafe_allow_html=True
            )


def render_reality_vs_interpretation(text: str):
    if not text:
        return
    observed_match = re.search(r'OBSERVED PATTERNS?:([\s\S]*?)(?=WHAT THIS SUGGESTS?:|$)', text, re.IGNORECASE)
    suggests_match = re.search(r'WHAT THIS SUGGESTS?:([\s\S]*?)$', text, re.IGNORECASE)

    if observed_match:
        st.markdown(
            '<div class="slabel" style="color:#38bdf8;margin-bottom:8px">🧾 Observed Patterns</div>',
            unsafe_allow_html=True
        )
        obs_text = observed_match.group(1).strip()
        for line in obs_text.split('\n'):
            if line.strip():
                st.markdown(
                    f'<div class="reality-block"><div class="btext">{line.strip()}</div></div>',
                    unsafe_allow_html=True
                )

    if suggests_match:
        st.markdown(
            '<div class="slabel" style="color:#fbbf24;margin-top:14px;margin-bottom:8px">🧠 What This Suggests</div>',
            unsafe_allow_html=True
        )
        sug_text = suggests_match.group(1).strip()
        for line in sug_text.split('\n'):
            if line.strip():
                st.markdown(
                    f'<div class="interpretation-block"><div class="btext" style="color:#fde68a">{line.strip()}</div></div>',
                    unsafe_allow_html=True
                )

    if not observed_match and not suggests_match:
        st.markdown(f'<div class="btext">{text}</div>', unsafe_allow_html=True)


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


# ── MAIN ───────────────────────────────────────────────────────────────
def main():
    st.markdown('<div class="eyebrow">PMFit AI · v5 · Think With Founders</div>', unsafe_allow_html=True)
    st.markdown("# Does your idea fit\nyour actual market?")
    st.markdown(
        '<p style="color:#475569;font-size:0.9rem;margin-top:-0.5rem;margin-bottom:1.5rem;">'
        'Structured PMF analysis. Separates reality from interpretation. '
        'Every problem comes with fix paths. Every assumption comes with a reversal.'
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
    location_key = st.selectbox(
        "market",
        options=list(LOCATIONS.keys()),
        label_visibility="collapsed"
    )
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
                    max_tokens=2500,
                    messages=[{
                        "role": "user",
                        "content": build_prompt(idea, loc_data["name"], location_context)
                    }]
                )
                raw_text = message.content[0].text
                result = parse_result(raw_text)

                st.divider()

                # ── SCORE ──
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
                        f'<div style="font-size:12px;color:#64748b;line-height:1.65">{result.get("score_context", "")}</div>',
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f'<div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.15);'
                    f'border-radius:8px;padding:8px 14px;font-size:11px;color:#64748b;margin:12px 0">'
                    f'{location_key.split()[0]} Grounded in <strong style="color:#94a3b8">'
                    f'{loc_data["name"]}</strong> market dynamics'
                    f'</div>', unsafe_allow_html=True
                )

                # ── VERDICT ──
                if result.get("verdict"):
                    st.markdown("## Verdict")
                    st.markdown(
                        f'<div class="section-card"><div class="vtext">{result["verdict"]}</div></div>',
                        unsafe_allow_html=True
                    )

                # ── PROS ──
                if result.get("pros"):
                    st.markdown("## What Is Actually Working")
                    st.markdown('<div class="pros-card">', unsafe_allow_html=True)
                    render_confidence_blocks(result["pros"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── CONS ──
                if result.get("cons"):
                    st.markdown("## What Is Actually Not Working")
                    st.markdown(
                        '<p style="font-size:12px;color:#475569;margin-bottom:10px">'
                        'Each friction point includes possible fix paths — ways to address it.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    render_confidence_blocks(result["cons"], show_fix_paths=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── REALITY VS INTERPRETATION ──
                if result.get("reality"):
                    st.markdown("## Reality vs Interpretation")
                    st.markdown(
                        '<p style="font-size:12px;color:#475569;margin-bottom:10px">'
                        'What is observed vs what it means — kept separate so you can challenge the interpretation.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    render_reality_vs_interpretation(result["reality"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── ASSUMPTIONS ──
                if result.get("assumptions"):
                    st.markdown("## Assumptions You Are Making")
                    st.markdown(
                        '<p style="font-size:12px;color:#475569;margin-bottom:10px">'
                        'Each assumption includes what changes if you prove it wrong — '
                        'showing both risk and upside.</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    render_assumptions(result["assumptions"])
                    st.markdown('</div>', unsafe_allow_html=True)

                # ── VIABLE PATH ──
                if result.get("path"):
                    st.markdown("## Viable Path Forward")
                    st.markdown(
                        f'<div class="path-card">'
                        f'<div class="slabel" style="color:#a78bfa">Strategic direction — not motivation</div>'
                        f'<div class="btext" style="color:#c4b5fd">{result["path"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # ── HIGHEST LEVERAGE ──
                if result.get("leverage"):
                    st.markdown("## Highest Leverage Move")
                    st.markdown(
                        f'<div class="leverage-card">'
                        f'<div class="slabel" style="color:#38bdf8">Do this in the next 7 days · costs ₹0</div>'
                        f'<div class="btext" style="color:#7dd3fc">{result["leverage"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # ── MOMENTUM CLOSE ──
                if result.get("momentum"):
                    st.markdown("## Where You Actually Stand")
                    st.markdown(
                        f'<div class="momentum-card">'
                        f'<div class="slabel" style="color:#22c55e">Honest reset — not cheerleading</div>'
                        f'<div class="btext" style="color:#86efac">{result["momentum"]}</div>'
                        f'</div>', unsafe_allow_html=True
                    )

                # ── PLAYBOOKS ──
                all_text = " ".join([
                    result.get("path", ""),
                    result.get("leverage", ""),
                    result.get("cons", ""),
                    result.get("assumptions", ""),
                    result.get("momentum", ""),
                ])
                found_keys = find_template_keys(all_text)

                if found_keys:
                    st.divider()
                    st.markdown("## Playbooks for Your Next Steps")
                    st.markdown(
                        '<div class="hint-box">'
                        '⚡ Based on the analysis — expand any playbook for '
                        'word-for-word scripts, exact questions, and success metrics.'
                        '</div>', unsafe_allow_html=True
                    )
                    for key in found_keys:
                        tpl = TEMPLATES.get(key)
                        if tpl:
                            with st.expander(f"📋 {tpl['title']}"):
                                st.markdown(
                                    f'<div class="template-box">{tpl["content"]}</div>',
                                    unsafe_allow_html=True
                                )

                # ── FULL LIBRARY ──
                st.divider()
                st.markdown("## Full Playbook Library")
                st.markdown(
                    '<p style="font-size:12px;color:#475569;margin-bottom:10px">'
                    'All scripts and templates — available for any next step.</p>',
                    unsafe_allow_html=True
                )
                for key, tpl in TEMPLATES.items():
                    with st.expander(f"📋 {tpl['title']}"):
                        st.markdown(
                            f'<div class="template-box">{tpl["content"]}</div>',
                            unsafe_allow_html=True
                        )

                st.divider()
                st.markdown(
                    '<p style="text-align:center;font-size:11px;color:#1e2533">'
                    'PMFit AI · ● High Confidence = verified · ◐ Medium = inferred · ○ Assumption = validate first</p>',
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
