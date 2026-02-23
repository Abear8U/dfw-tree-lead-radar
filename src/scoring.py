# scoring.py

def normalize(text: str) -> str:
    return (text or "").lower()


# Cities ~1 hour around Eagle Mountain / Fort Worth
SERVICE_CITIES = [
    "fort worth","saginaw","haslet","keller","watauga","haltom city",
    "north richland hills","hurst","euless","bedford","white settlement",
    "benbrook","lake worth","azle","pelican bay","eagle mountain",
    "weatherford","aledo","hudson oaks","willow park","granbury",
    "roanoke","trophy club","southlake","argyle","denton","corinth",
    "lewisville","flower mound",
    "arlington","grand prairie","mansfield","burleson",
    "irving","grapevine","colleyville","dallas"
]

# Obvious non-job “tree” contexts
EXCLUDE_TERMS = [
    "family tree", "skill tree", "decision tree",
    "christmas tree", "tree stand", "treehouse",
    "genealogy", "ancestry", "botany"
]

# Words that strongly indicate a tree-service job
TREE_WORDS = ["tree", "trees"]

ACTION_TERMS = [
    "remove", "removal", "cut down", "cutting", "trim", "trimming",
    "prune", "pruning", "limb", "limbs", "branch", "branches",
    "stump", "stump grinding", "grind stump",
    "storm", "cleanup", "damage", "fallen", "downed", "fell",
    "haul", "haul off", "debris", "yard cleanup", "brush"
]

SERVICE_PHRASES = [
    "tree removal", "tree trimming", "tree service", "tree guy", "arborist",
    "stump removal", "stump grinding", "storm cleanup", "storm damage",
    "fallen tree", "downed tree", "tree fell", "tree on house", "tree on fence"
]

INTENT_TERMS = [
    "need", "looking for", "recommend", "anyone know",
    "quote", "estimate", "how much", "asap", "urgent", "today", "help"
]


def looks_like_tree_job(t: str) -> bool:
    t = normalize(t)

    if any(bad in t for bad in EXCLUDE_TERMS):
        return False

    has_tree = any(w in t for w in TREE_WORDS)
    if not has_tree:
        return False

    # Accept if it has strong phrases OR tree + action terms OR tree + intent terms
    has_strong_phrase = any(p in t for p in SERVICE_PHRASES)
    has_action = any(a in t for a in ACTION_TERMS)
    has_intent = any(i in t for i in INTENT_TERMS)

    return has_strong_phrase or (has_action and has_tree) or (has_intent and has_tree)


def score_text(text: str) -> tuple[int, str]:
    t = normalize(text)

    if not looks_like_tree_job(t):
        return 0, ""

    score = 2
    city = ""

    # City bonus
    for c in SERVICE_CITIES:
        if c in t:
            city = c
            score += 2
            break

    # Strong phrase bonus
    if any(p in t for p in SERVICE_PHRASES):
        score += 3

    # Intent bonus
    if any(i in t for i in INTENT_TERMS):
        score += 2

    # Urgency bonus
    urgent_terms = ["asap", "urgent", "today", "storm", "fallen", "downed"]
    if any(u in t for u in urgent_terms):
        score += 2

    return score, city
