# Synthetic training-data label review

- **Scope:** all 2,448 questions in `data/synthetic/raw/*.jsonl` (42 files, 924 states), plus the 136 questions in the round-2 hard-case files that existed when the review started (`hnum_01`, `hpar_01`, `hpar_02`). Not covered: `hinj_01`, `hmul_01` and `htmp_01`, which appeared mid-review, and `data/distill.jsonl`, whose labels come from a teacher model rather than a generator.
- **Pass 1:** 11 Claude Opus reviewers each took about 4 files. For every question they answered first and then compared against the target, redid all date and number math, and checked the labeling policy in `data/synthetic/BRIEF.md`. One verdict per question is in `verdicts_<file>.jsonl`: ok / wrong / ambiguous / malformed, plus a suggested target and a reason. Every question has exactly one verdict, and the ids and targets match the raw files.
- **Pass 2:** Claude Opus (the orchestrating session) re-read every non-ok item in full context, plus a random sample of 30 items marked ok (29 held up, and 1 new malformed item was found: roub-0110-q0).
- **Result:** out of 2,584 questions reviewed, pass 1 flagged 53 (9 wrong, 44 ambiguous, 0 malformed). The final decisions in `flags.json` are **6 relabel, 37 drop, 11 keep**. Nothing has been changed or deleted in `raw/`.
- **Caveat:** these are LLM judgments of LLM-written labels (same model family), not human review. The flags are recommendations.

## Dropped or relabeled, by file prefix

| prefix | family | questions | drop + relabel |
|---|---|---|---|
| adva | syn adversarial (a) | 176 | 1 |
| advb | syn adversarial (b) | 165 | 2 |
| evia | syn evidence (a) | 245 | 3 |
| evib | syn evidence (b) | 144 | 1 |
| hnum | hardcases numeric | 49 | 0 |
| hpar | hardcases paraphrase | 87 | 0 |
| mula | syn multilabel (a) | 120 | 4 |
| mulb | syn multilabel (b) | 216 | 5 |
| pola | syn policy (a) | 55 | 2 |
| polb | syn policy (b) | 213 | 6 |
| roua | syn routing (a) | 276 | 5 |
| roub | syn routing (b) | 272 | 1 |
| urga | syn urgency (a) | 277 | 7 |
| urgb | syn urgency (b) | 289 | 6 |

## Relabel (clear error, clear fix)

| id | old target | new target | why |
|---|---|---|---|
| evia-0016-q3 | `["custom_reporting_module", "dedicated_support_line", "erp_api_integration"]` | `["custom_reporting_module", "erp_api_integration"]` | Amara named only the reporting module and ERP integration; the support line was Daniel's line. |
| mula-0044-q1 | `["billed_119_99_annual", "expected_12_99_monthly", "five_day_response_time", "three_days_of_notes_lost"]` | `["billed_119_99_annual", "expected_12_99_monthly"]` | The 5-day response and the 3 days of lost notes are not about the billing mismatch. |
| mulb-0062-q2 | `true` | `false` | The memo only recommends approval; nothing says DeskFlow is approved. |
| mulb-0068-q0 | `["drivers_license_required", "paid_training_provided"]` | `["drivers_license_required"]` | Paid training is something the employer offers, not a hiring requirement. |
| polb-0036-q2 | `["failed_to_mitigate", "roof_covered"]` | `["failed_to_mitigate"]` | The state never says the windstorm roof damage is covered. |
| roua-0082-q2 | `["backup_failure_undetected", "ransomware_incident_reported", "potential_data_loss"]` | `["backup_failure_undetected", "ransomware_incident_reported", "potential_data_loss", "promotional_content_present"]` | The state literally contains an unrelated promo_banner. |

## Drop (wrong with no clean fix, ambiguous, or malformed)

| id | old target | new target | why |
|---|---|---|---|
| adva-0026-q1 | `["update_payment_method", "asks_hypothetical_question"]` | — | An 'asks a hypothetical question' candidate doesn't fit a question about actions to perform now. |
| advb-0049-q2 | `["motor_only_replacement_tried_first", "buyer_missed_the_return_deadline_with_no_consequence"]` | — | The state contradicts itself: the Day 20 drop-off is inside the Day 9+14=23 window, yet the story treats it as late. |
| advb-0063-q2 | `["weighting_is_fixed_at_original_terms", "vendor_b_has_highest_technical_score", "vendor_c_has_lowest_price"]` | — | The conclusion never states that Vendor C has the lowest price (that is only in the table). |
| evia-0045-q0 | `"anders"` | — | Priya's roadmap doc is also still 'in review' (unresolved), so two answers fit. |
| evia-0068-q1 | `["reduced_oceania_queue_times", "the_early_community_speculation"]` | — | Whether the community speculation is 'attributed to the algorithm' or to a comms gap is debatable. |
| evib-0012-q3 | `["active_role"]` | — | 'Active sales role' isn't necessarily 'substantially similar'; the employee's role is never given. |
| mula-0001-q1 | `["firmware_update"]` | — | 'Hoping a firmware update fixes it' isn't clearly an explicit request. |
| mula-0005-q3 | `["clause_1_standard_warranty", "clause_3_extended_care", "clause_6_registration"]` | — | 'Directly relevant clauses' is subjective, and the target is inconsistent (clause 1 in, clause 4 out). |
| mula-0029-q0 | `["feature_request", "compliment_about_support", "plan_comparison_question"]` | — | The user asks about one plan's limit; whether that counts as 'comparing two plans' is debatable. |
| mulb-0020-q1 | `["health_benefits", "paid_time_off", "equipment_provided"]` | — | Needing to own a laptop implies, but doesn't 'explicitly' exclude, a provided laptop. |
| mulb-0037-q2 | `["signed_commitment_date_for_mfa"]` | — | It's unclear whether a promised future date counts as 'confirmed evidence'. |
| mulb-0040-q1 | `["no_preliminary_data", "postdoc_listed_as_pi", "equipment_preapproval_requested_after_submission"]` | — | The guidelines don't say that late equipment pre-approval makes an application ineligible. |
| pola-0009-q2 | `"outstanding_invoice_must_be_settled"` | — | The invoice was already paid by the memo date, so 'must be settled' describes the past. |
| pola-0022-q2 | `["within_warranty_time_window", "proof_of_purchase_provided", "defect_confirmed"]` | — | The policy defines no warranty time window, so 'within window' can't be decided. |
| polb-0016-q1 | `"both_required"` | — | The manager says the promotion alone makes him eligible (for the list); two readings fit. |
| polb-0018-q0 | `true` | — | The policy covers non-exempt staff only; Grace's classification is never stated. |
| polb-0018-q1 | `"time_half"` | — | Same gap: non-exempt status is assumed. |
| polb-0028-q0 | `true` | — | The policy never says the claim 'will be denied'; the consequence is not stated. |
| polb-0050-q2 | `["keep_1500", "one_dd"]` | — | 'Meeting both conditions' would also waive the fee, so the non-target candidate is actually true. |
| roua-0033-q0 | `"integration_sync_failure"` | — | The customer never ranks urgency; the sync failure vs the broken export button is a judgment call. |
| roua-0058-q0 | `"none"` | — | product_feedback_review ('general product reviews') fits as well as 'none'. |
| roua-0083-q0 | `"returns_refunds"` | — | A skin-reaction safety review is as defensible as refunds. |
| roua-0098-q1 | `"account_settings_admin"` | — | Two equal requests; nothing marks the retention change as the primary one. |
| roub-0110-q0 | `"financial_aid_bursar"` | — | The question asks 'what was decided' but the candidates are team names (malformed). |
| urga-0018-q0 | `false` | — | The latest update asks the agent to edit the postmortem doc, which is further agent action. |
| urga-0060-q0 | `["prorated_refund_of_annual_plan"]` | — | The policy requires the 'app unusable'; only the sync feature was down. |
| urga-0060-q1 | `true` | — | Same gap as q0. |
| urga-0074-q0 | `"qualifies_as_emergency_exception"` | — | The stated policy has no emergency exception; the label relies on outside knowledge. |
| urga-0083-q1 | `"before"` | — | The expected load time of the results is unknown; 'unclear' is equally defensible. |
| urga-0095-q1 | `["the_seller_agreed_to_a_full_refund", "the_buyer_already_shipped_the_item_back", "the_refund_has_already_been_completed"]` | — | The refund was released but hasn't landed, and the item was delivered, not in transit. |
| urga-0107-q2 | `["the_dispute_finalized_in_the_customers_favor"]` | — | The Mar 2 message is arguably a follow-up that came before the window closed. |
| urgb-0002-q0 | `true` | — | 'Right now' is undefined; by the end of the thread the fix is deployed. |
| urgb-0007-q2 | `["occurred_during_published_maintenance"]` | — | The alert was elevated from 09:22 to 10:58, so '>10 minutes' is arguably true. |
| urgb-0030-q1 | `true` | — | 'Due end of day Thursday' vs 'before Thursday' is a wording trap with no clear answer. |
| urgb-0078-q0 | `true` | — | The ordinance applies Oct 1 to May 1; no date is given. |
| urgb-0078-q1 | `"ordinance_violation_emergency_repair_required"` | — | Same missing date. |
| urgb-0095-q0 | `"imminent_need_for_emergency_contact_procedure"` | — | The office later says the procedure is for unreachable parents; 'imminent' is debatable. |

## Flagged by a reviewer, kept after the second look

| id | old target | new target | why |
|---|---|---|---|
| evia-0040-q3 | `["support_getting_meaningfully_worse", "greenstack_price_increase_at_renewal"]` | unchanged | Tobias says he doubts they'd move before the contract ends; the target holds. |
| hpar-0005-q2 | `"p3_low"` | unchanged | 'Not urgent, just flagging' with no errors reasonably fits P3. |
| mula-0044-q2 | `"data_recovery_and_refund"` | unchanged | Fixing the data and the billing is the clear implied request. |
| mulb-0002-q0 | `["food_handler_cert_required", "weekend_availability_required"]` | unchanged | The candidate says 'must obtain' a certificate, which is true. |
| mulb-0018-q0 | `["two_reference_letters", "data_management_plan_if_over_100k"]` | unchanged | The DMP requirement reasonably belongs to the full-proposal stage. |
| polb-0011-q0 | `false` | unchanged | Nothing establishes Kevin as Lisa's approver, so false holds. |
| polb-0011-q1 | `"lisa_supervisor"` | unchanged | Her supervisor is the right approver under either reading. |
| polb-0041-q2 | `true` | unchanged | An undisclosed heart condition is the policy's own example of a material misstatement. |
| roub-0090-q1 | `["broken_streetlight"]` | unchanged | A farmers-market question isn't something needing repair or action. |
| urga-0108-q0 | `"mixed_feelings"` | unchanged | The candidate description matches the message exactly. |
| urgb-0002-q2 | `["checkout_payments_failing"]` | unchanged | 'Down to 4% and falling' is not yet fixed. |

## State-level slips that don't change any label

- advb-0017: Zenith's total is given as 89.6 in one place and 77.3 in another (the components sum to 77.3).
- adva-0043: the state says the report came '8 days after trip end'; 22 Sep minus 15 Sep is 7.
- urgb-0016: '40k to 61k in an hour' is about 350 per minute, not the stated 2k per minute.
- roub-0110: the notes are dated Oct 2025 but discuss a January appeal.
- roua-0014 and roub-0058: the notes contain small day-count errors; the targets are still right.
- polb-0063: the agent and customer lines are swapped in one exchange.

## Applying the flags

`flags.json` uses the same shape as `data/eval/review/overrides.json` (`{id: {target, note} | {drop: true}}`), plus `action`/`old_target`/`reviewer_*` fields. `scripts/build_data.py` currently applies overrides only to the eval set; to use these flags for the synthetic set, apply entries whose `action` is `drop` or `relabel` after `build(...)`, then rebuild.
