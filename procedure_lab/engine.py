"""Replay two candidate meanings of "started" at one packing station.

A regular order progresses in a fixed sequence. Exactly one rush order arrives.
Rush takes priority unless a started, unfinished regular order must be completed.
The proposer supplies the supporting clauses. Matching excerpts checks provenance,
while judging their semantic fit remains a separate review step.
"""

REGULAR_PROGRESS = ("label_printed", "first_item_placed", "packing_finished")
START_EVENTS = REGULAR_PROGRESS[:2]
ARRIVAL_POSITIONS = ("before_label", "after_label", "after_item", "after_finish")
RUSH_ARRIVAL = "rush_arrived"


def replay(events, starts_at):
    """Return the next order on rush arrival. Reject physically impossible traces."""
    if starts_at not in START_EVENTS:
        raise ValueError("Unsupported packing-start event")
    if not isinstance(events, (list, tuple)) or not events or events[-1] != RUSH_ARRIVAL:
        raise ValueError("A decision trace must end at rush arrival")

    progress = tuple(events[:-1])
    if progress != REGULAR_PROGRESS[:len(progress)]:
        raise ValueError("Regular-order events must form a legal packing sequence")

    if starts_at in progress and "packing_finished" not in progress:
        return "regular"
    return "rush"


def _source_span(procedure, quote, field):
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError(f"{field} requires a nonblank source quote")
    offset = procedure.find(quote)
    if offset == -1:
        raise ValueError(f"{field} must quote the submitted procedure exactly")
    return {"quote": quote, "start": offset, "end": offset + len(quote)}


def analyze(procedure, proposal):
    """Validate a proposal, then exhaust the supported arrival positions.

    Returned offsets are zero-based Python string indices with exclusive ends.
    If an identical quote occurs twice, its first occurrence is highlighted.
    The three open-order cases and the terminal control are reported separately.
    """
    if not isinstance(procedure, str) or not procedure.strip():
        raise ValueError("A nonblank procedure is required")
    if not isinstance(proposal, dict):
        raise ValueError("Expected a structured proposal")

    status = proposal.get("status")
    candidates = proposal.get("readings")
    if status == "outside_scope":
        if candidates != []:
            raise ValueError("An abstention must have an empty list of readings")
        reason = proposal.get("reason", "Outside the supported packing workflow")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("An abstention reason must be nonblank text")
        return {
            "status": "abstained", "reason": reason, "readings": [],
            "preconditions": {}, "cases": [], "post_finish_control": None,
            "witness": None, "searched_traces": 0,
        }
    if status != "interpreted" or not isinstance(candidates, list) or len(candidates) not in (1, 2):
        raise ValueError("An interpreted proposal requires one or two readings")

    preconditions = {
        name: _source_span(procedure, proposal.get(name), name)
        for name in ("rush_priority_quote", "finish_started_quote")
    }
    readings = []
    seen = set()
    for candidate in candidates:
        if not isinstance(candidate, dict) or candidate.get("starts_at") not in START_EVENTS:
            raise ValueError("Each reading must specify a supported packing-start event")
        meaning = candidate["starts_at"]
        if meaning in seen:
            raise ValueError("Duplicate interpretations cannot support a divergence")
        seen.add(meaning)
        readings.append({
            "starts_at": meaning,
            **_source_span(procedure, candidate.get("quote"), "reading"),
        })

    cases = []
    for count, position in enumerate(ARRIVAL_POSITIONS):
        events = [*REGULAR_PROGRESS[:count], RUSH_ARRIVAL]
        actions = {r["starts_at"]: replay(events, r["starts_at"]) for r in readings}
        cases.append({
            "position": position,
            "events": events,
            "actions": actions,
            "diverges": len(set(actions.values())) > 1,
        })

    # Cases are ordered by event count, so the first divergence is a shortest one.
    witness = next((case for case in cases if case["diverges"]), None)
    return {
        "status": "divergent" if witness else "single_reading",
        "readings": readings,
        "preconditions": preconditions,
        "cases": cases[:-1],
        "post_finish_control": cases[-1],
        "witness": witness,
        "searched_traces": len(cases),
    }
