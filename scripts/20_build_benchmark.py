"""boundaries.jsonl → benchmark.jsonl: gold obligations (filtered by the real message), natural_loss, and variants.
Resumable (--resume skips boundary ids already in the output). Parallel over boundaries."""
import argparse, json, random, sys, threading, time
import concurrent.futures as cf
from pathlib import Path
from handoffcheck.llm import LLM
from handoffcheck.schema import read_jsonl, boundary_from_dict, context_to_text, to_dict, Variant, append_jsonl
from handoffcheck.gold import extract_gold, split_by_message
from handoffcheck.inject import inject_absent, inject_altered_value, inject_altered_semantic, insert_fabricated, alter_value, make_rng, present
from handoffcheck.synth_data import paraphrase, fabricate, altered_semantic_llm

ap = argparse.ArgumentParser()
ap.add_argument("--in", dest="inp", default="data/boundaries.jsonl")
ap.add_argument("--out", default="data/benchmark.jsonl")
ap.add_argument("--domains", default="")
ap.add_argument("--limit", type=int, default=0, help="per domain")
ap.add_argument("--min-obligations", type=int, default=2)
ap.add_argument("--workers", type=int, default=8)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--resume", action="store_true")
a = ap.parse_args()

llm = LLM()
lock = threading.Lock()
done = set()
if a.resume and Path(a.out).exists():
    done = {r["boundary"]["id"] for r in read_jsonl(a.out)}
rows = [boundary_from_dict(r) for r in read_jsonl(a.inp)]
if a.domains:
    keep = set(a.domains.split(","))
    rows = [b for b in rows if b.domain in keep]
if a.limit:
    per = {}
    sel = []
    for b in rows:
        per[b.domain] = per.get(b.domain, 0) + 1
        if per[b.domain] <= a.limit:
            sel.append(b)
    rows = sel
rows = [b for b in rows if b.id not in done]
print(f"building {len(rows)} boundaries (skipping {len(done)} done)", flush=True)


def build(b):
    ctx = context_to_text(b.context)
    msg = b.message
    obs = extract_gold(llm, ctx, msg, b.receiver_role)
    kept, lost = split_by_message(obs, msg)
    b.obligations, b.natural_loss = kept, lost
    b.meta["n_extracted"] = len(obs)
    stats = {"id": b.id, "domain": b.domain, "extracted": len(obs), "kept": len(kept), "lost": len(lost), "variants": {}}
    if len(kept) < a.min_obligations:
        stats["skipped"] = "too few obligations"
        return b, [], stats
    variants = []
    vid = 0

    def add(kind, message, target=None, fab=None, excluded=None, meta=None):
        nonlocal vid
        vid += 1
        variants.append(Variant(id=f"{b.id}#v{vid}", boundary_id=b.id, kind=kind, message=message, target_obligation_id=target,
                                fabricated_claim=fab, excluded_obligation_ids=excluded or [], meta=meta or {}))
        stats["variants"][kind] = stats["variants"].get(kind, 0) + 1

    add("clean", msg)
    # paraphrase
    ptxt, excluded = paraphrase(llm, msg, kept)
    if ptxt:
        add("clean_paraphrase", ptxt, excluded=excluded, meta={"n_excluded": len(excluded)})
    else:
        stats["paraphrase_failed"] = True
    # absent / altered_value per eligible obligation
    others = lambda o: [x for x in kept if x.id != o.id]
    for o in kept:
        rng = make_rng(a.seed, b.id, o.id)
        r = inject_absent(msg, o, others(o), rng)
        if r:
            add("absent", r["message"], target=o.id, meta={"level": r.get("level")})
        rng = make_rng(a.seed, b.id, o.id)
        r = inject_altered_value(msg, o, others(o), rng)
        if r:
            add("altered_value", r["message"], target=o.id, meta={"kv": r["kv"], "new_kv": r["new_kv"]})
    # altered_semantic: one obligation (rule first, LLM fallback), deterministic order
    order = list(kept)
    make_rng(a.seed, b.id, "sem").shuffle(order)
    sem_done = False
    for o in order:
        r = inject_altered_semantic(msg, o, make_rng(a.seed, b.id, o.id + "sem"))
        if r:
            add("altered_semantic", r["message"], target=o.id, meta={"rule": r["rule"], "source": "rule"})
            sem_done = True
            break
    if not sem_done:
        for o in order[:2]:
            t = altered_semantic_llm(llm, msg, o)
            if t:
                add("altered_semantic", t, target=o.id, meta={"rule": "llm", "source": "llm"})
                sem_done = True
                break
    # fabricated
    fab = fabricate(llm, ctx, msg)
    if fab:
        add("fabricated", insert_fabricated(msg, fab["sentence"]), fab=fab)
    return b, variants, stats


t0 = time.time()
n_ok = 0
with cf.ThreadPoolExecutor(a.workers) as ex:
    futs = {ex.submit(build, b): b for b in rows}
    for f in cf.as_completed(futs):
        b = futs[f]
        try:
            bb, variants, stats = f.result()
        except Exception as e:  # noqa
            print("ERROR", b.id, repr(e)[:200], flush=True)
            continue
        with lock:
            if variants:
                append_jsonl(a.out, {"boundary": to_dict(bb), "variants": [to_dict(v) for v in variants]})
                n_ok += 1
            print(json.dumps(stats), flush=True)
print(f"done: {n_ok} boundaries written in {time.time()-t0:.0f}s; usage: {llm.usage}")
