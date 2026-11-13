# Actual-change receipt

Prepare this receipt after implementation and verification whenever a material
slice is about to be represented as done, implemented, complete, shipped,
verified, or ready for commit or release. Trigger on the meaning of the claim,
not the appearance of those words in quoted text, tests, or documentation.

The receipt describes actual consequence. It does not certify repository
continuity or promote a slice into durable project truth.

## Reconstruct the realized transition

Use the final worktree and evidence, not the implementation narrative. Record:

1. **Authorization:** the accepted spec revision, bounded request, or other
   authority under which the change was made.
2. **Realized change shape:** the promised surfaces beside the surfaces actually
   changed, including any newly crossed state, trust, persistence, delivery, or
   lifecycle boundary.
3. **Final risk floor:** the risk classification after inspecting the complete
   diff. An initial green or amber classification does not survive contrary
   evidence automatically.
4. **Adversarial receipts:** every risk-triggered review, its source or diff
   revision, and the reconciled disposition of each finding. Preserve whether a
   finding is confirmed, inferred, ambiguous, or demonstrated by a
   counterexample. Do not pass raw allegations downstream as settled fact.
5. **Proof and gaps:** checks actually run, observed results, skipped or
   unavailable proof, and owner-only or external verification still required.
6. **Departures:** unmet acceptance criteria, altered obligations, behavior that
   differs from the accepted transition, and decisions that require owner
   authority.
7. **Durability:** state separately whether the result is uncommitted,
   committed, pushed, deployed, migrated, or otherwise externally projected.
   Do not infer one state from another.

When exact revisions are available, include them. If a receipt was produced
against an earlier diff, mark it stale and refresh the affected review before
using it to support a terminal claim.

## Hand off without usurping promotion

If the target repository has a continuity or formal close workflow, pass this
receipt to that workflow. The close workflow owns reconciliation of current
repository truth and any outcome such as `closed`, `partial`, or `divergent`.

If no such workflow is available, include the receipt's material facts in the
ordinary handoff. Claim only the implementation and proof actually observed;
do not imply that every durable representation, accepted spec, or external
projection has been reconciled.

The receipt is normally transient. Do not create a receipt log or session
memoir unless the target repository explicitly owns such an artifact.
