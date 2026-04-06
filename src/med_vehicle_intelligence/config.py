"""MED Vehicle Intelligence MCP Server — Configuration."""

SERVER_NAME = "MED Vehicle Intelligence"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = (
    "Expert car repair and maintenance advisory tools "
    "from a 20-year mechanic veteran. Get fair price ranges, "
    "maintenance schedules, fix-or-replace recommendations, "
    "and shop red flag detection."
)

SITE_URL = "https://myeverydaydriver.com"

# CTA disabled for MVP. Uncomment and configure when Calendly is set up.
# CALENDLY_URL = "https://calendly.com/myeverydaydriver/advisory"
# CTA_ESTIMATE = (
#     "\n\n---\n"
#     "Want a personalized review of your specific estimate? "
#     f"Book a 15-minute advisory session: {CALENDLY_URL}"
# )
CTA_ESTIMATE = ""
CTA_MAINTENANCE = ""
CTA_REPAIR_REPLACE = ""
CTA_RED_FLAGS = ""
