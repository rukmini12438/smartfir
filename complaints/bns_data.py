"""
Curated demo dataset of common Bharatiya Nyaya Sanhita (BNS) sections.

NOTE: Ye sirf EDUCATIONAL/PORTFOLIO purpose ke liye ek chhota, curated
subset hai (poora BNS nahi) — real police use ke liye poora official
BNS text (India Code / official gazette se) use karna hoga. Ye interview
mein bhi clearly explain karne wali baat hai: "maine RAG concept ek
representative dataset ke saath demonstrate kiya hai."
"""

BNS_SECTIONS = [
    {
        "section": "BNS 103",
        "title": "Punishment for murder",
        "text": "Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. Applies to cases involving intentional killing of another person.",
    },
    {
        "section": "BNS 115",
        "title": "Voluntarily causing hurt",
        "text": "Whoever voluntarily causes hurt shall be punished with imprisonment and/or fine. Applies to physical injury caused intentionally, without grievous harm.",
    },
    {
        "section": "BNS 118",
        "title": "Voluntarily causing grievous hurt",
        "text": "Whoever voluntarily causes grievous hurt shall be punished with imprisonment. Applies to serious physical injury, fractures, permanent disfigurement, or danger to life.",
    },
    {
        "section": "BNS 125",
        "title": "Act endangering life or personal safety of others",
        "text": "Whoever does any act so rashly or negligently as to endanger human life or personal safety of others, including causing hurt by such act, shall be punished. Commonly applied to rash/negligent driving causing injury.",
    },
    {
        "section": "BNS 137",
        "title": "Kidnapping",
        "text": "Whoever kidnaps any person from India or from lawful guardianship shall be punished with imprisonment. Applies to cases of a person being taken away without consent.",
    },
    {
        "section": "BNS 140",
        "title": "Kidnapping for ransom",
        "text": "Kidnapping or abducting in order to extort money or valuable security, or to compel a person to do something, shall be punished, potentially with death or life imprisonment.",
    },
    {
        "section": "BNS 303",
        "title": "Theft",
        "text": "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, commits theft. Punishment includes imprisonment and/or fine. Applies to general theft of property, vehicles, phones, etc.",
    },
    {
        "section": "BNS 304",
        "title": "Snatching",
        "text": "Theft is snatching if the offender suddenly or quickly seizes, secures, or grabs movable property from a person or their possession. Applies to chain-snatching, phone-snatching cases.",
    },
    {
        "section": "BNS 305",
        "title": "Theft in a dwelling house",
        "text": "Theft committed in a building, tent, or vessel used as a human dwelling, or for custody of property, is punished more severely. Applies to house burglary/theft cases.",
    },
    {
        "section": "BNS 306",
        "title": "Theft by clerk or servant of property in possession of master",
        "text": "Theft committed by a clerk or servant in respect of property in the possession of their master or employer. Applies when domestic help, employees are suspected of theft.",
    },
    {
        "section": "BNS 309",
        "title": "Robbery",
        "text": "Theft or extortion becomes robbery when the offender causes or threatens to cause death, hurt, or wrongful restraint, in order to commit the theft. Applies to theft involving violence or threat.",
    },
    {
        "section": "BNS 316",
        "title": "Criminal breach of trust",
        "text": "Whoever, being entrusted with property, dishonestly misappropriates or converts it to their own use, commits criminal breach of trust. Applies to financial fraud by someone in a position of trust.",
    },
    {
        "section": "BNS 318",
        "title": "Cheating",
        "text": "Whoever deceives a person and thereby dishonestly induces them to deliver property or do/omit an act, commits cheating. Applies to fraud, scams, online cheating.",
    },
    {
        "section": "BNS 324",
        "title": "Mischief causing damage",
        "text": "Whoever causes destruction of property, or diminishes its value/utility, with intent to cause wrongful loss, commits mischief. Applies to property/vehicle damage cases.",
    },
    {
        "section": "BNS 351",
        "title": "Criminal intimidation",
        "text": "Whoever threatens another with injury to person, reputation, or property, with intent to cause alarm, commits criminal intimidation. Applies to threats, coercion.",
    },
    {
        "section": "BNS 352",
        "title": "Intentional insult with intent to provoke breach of peace",
        "text": "Whoever intentionally insults another, intending to provoke a breach of the peace, shall be punished. Applies to verbal abuse, public altercations.",
    },
    {
        "section": "BNS 78",
        "title": "Stalking",
        "text": "Whoever follows or contacts a woman despite clear indication of disinterest, or monitors her use of the internet/email, commits stalking. Applies to harassment, cyberstalking cases involving women.",
    },
    {
        "section": "BNS 74",
        "title": "Assault or use of criminal force to woman with intent to outrage her modesty",
        "text": "Whoever assaults or uses criminal force intending to outrage the modesty of a woman shall be punished. Applies to molestation cases.",
    },
    {
        "section": "BNS 111",
        "title": "Organised crime",
        "text": "Any continuing unlawful activity by a person(s) acting as a member of an organised crime syndicate, using violence, threat, or corruption for material benefit. Applies to gang-related and syndicate crime.",
    },
    {
        "section": "BNS 336",
        "title": "Forgery",
        "text": "Whoever makes a false document or electronic record with intent to cause damage, or to commit fraud, commits forgery. Applies to fake documents, ID fraud, forged signatures.",
    },
]